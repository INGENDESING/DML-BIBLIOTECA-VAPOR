"""Convierte los PDFs del Libro del Vapor (Spirax Sarco) a Markdown legible.

- Repara las fuentes (ver pdf_fontfix.py) para extraer texto correcto.
- Titulos / listas / negritas segun fuente y tamano.
- Tablas -> tablas Markdown (page.find_tables).
- Diagramas y ecuaciones (vectoriales, imagenes o fuentes Type3 ilegibles) -> PNG recortado.

Uso:  python pdf_a_md.py <carpeta_pdfs> <carpeta_content/01_Libro_del_Vapor> [filtro]
"""
import os
import re
import sys
import glob
import unicodedata

import pymupdf
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdf_fontfix as ff  # noqa: E402

HEAD_Y = 45          # por encima: cabecera de pagina
FOOT_Y = 795         # por debajo: pie de pagina
MATH_FONT = re.compile(r'symbol|greek|sclbq|^mt|math|equation|ming|dings.*math', re.I)
BAD = re.compile(r'[\x00-\x08\x0b-\x1f�]')


# --------------------------------------------------------------------------- utilidades
def slug(s: str) -> str:
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-').lower()
    return s[:60] or 'x'


def rect_union(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def rect_near(a, b, gx, gy=None):
    gy = gx if gy is None else gy
    return not (a[2] + gx < b[0] or b[2] + gx < a[0] or a[3] + gy < b[1] or b[3] + gy < a[1])


def inside(pt_rect, big, tol=1.5):
    cx, cy = (pt_rect[0] + pt_rect[2]) / 2, (pt_rect[1] + pt_rect[3]) / 2
    return big[0] - tol <= cx <= big[2] + tol and big[1] - tol <= cy <= big[3] + tol


class Line:
    __slots__ = ('bbox', 'spans', 'text', 'size', 'bold', 'font', 'kind', 'bullet', 'math', 'bad')

    def __init__(self, bbox, spans):
        self.bbox = tuple(bbox)
        self.spans = spans
        self.kind = 'text'
        self.bullet = False
        # Vineta Dings
        if spans and spans[0]['font'].lower().startswith('dings') and len(spans) > 1:
            self.bullet = True
            spans = spans[1:]
        spans = [s for s in spans if not s['font'].lower().startswith('dings')]
        self.spans = spans
        self.text = ''.join(s['text'] for s in spans)
        self.font = spans[0]['font'] if spans else ''
        sizes = [(len(s['text'].strip()), s['size']) for s in spans if s['text'].strip()]
        self.size = max(sizes)[1] if sizes else (spans[0]['size'] if spans else 10)
        self.bold = bool(spans) and all(
            (s['flags'] & 16) or 'bold' in s['font'].lower() for s in spans if s['text'].strip())
        self.bad = bool(BAD.search(self.text))
        chars_math = sum(len(s['text']) for s in spans if MATH_FONT.search(s['font']))
        self.math = chars_math
        # texto con tipografia Type3 (T1, T2, ...) = ecuacion rasterizada
        if any(re.fullmatch(r'T\d+', s['font']) for s in spans):
            self.bad = True

    @property
    def y0(self):
        return self.bbox[1]

    @property
    def y1(self):
        return self.bbox[3]


def md_inline(line: Line) -> str:
    out = []
    for s in line.spans:
        t = s['text'].replace(' ', ' ')
        if not t:
            continue
        if ((s['flags'] & 16) or 'bold' in s['font'].lower()) and not line.bold \
                and re.search(r'[A-Za-z0-9]', t) and not MATH_FONT.search(s['font']):
            lead = t[:len(t) - len(t.lstrip())]
            trail = t[len(t.rstrip()):]
            out.append(f"{lead}**{t.strip()}**{trail}")
        else:
            out.append(t)
    r = ''.join(out)
    r = r.replace('****', '').replace('** **', ' ')
    r = re.sub(r'\*\*\s*\*\*', '', r)
    return r.replace('|', '\\|') if False else r


# --------------------------------------------------------------------------- extraccion
def page_lines(page):
    lines = []
    for b in page.get_text('dict', sort=True)['blocks']:
        if b['type'] != 0:
            continue
        for l in b['lines']:
            sp = [s for s in l['spans'] if s['text'] != '']
            if not sp:
                continue
            ln = Line(l['bbox'], sp)
            if not ln.text.strip() and not ln.bad:
                continue
            if ln.y1 < HEAD_Y or ln.y0 > FOOT_Y:
                continue
            lines.append(ln)
    return lines


def figure_regions(page, tables):
    """Agrupa dibujos vectoriales / imagenes en regiones de figura."""
    rects = []
    for d in page.get_drawings():
        # un mismo "dibujo" puede unir trazos de cabecera y pie: se evalua por segmento
        boxes = []
        for it in d['items']:
            pts = []
            for e in it[1:]:
                if isinstance(e, pymupdf.Point):
                    pts.append((e.x, e.y))
                elif isinstance(e, (pymupdf.Rect, pymupdf.Quad)):
                    r = e.rect if isinstance(e, pymupdf.Quad) else e
                    pts += [(r.x0, r.y0), (r.x1, r.y1)]
            if pts:
                xs = [q[0] for q in pts]
                ys = [q[1] for q in pts]
                boxes.append((min(xs), min(ys), max(xs), max(ys)))
        for b in boxes:
            if b[3] < HEAD_Y or b[1] > FOOT_Y:
                continue
            if (b[2] - b[0]) > 450 and (b[3] - b[1]) < 4:      # regla horizontal decorativa
                continue
            if any(inside(b, t, 3) for t in tables):
                continue
            rects.append(b)
    for im in page.get_image_info():
        b = tuple(im['bbox'])
        if b[3] < HEAD_Y or b[1] > FOOT_Y or (b[2] - b[0]) < 8:
            continue
        if (b[2] - b[0]) > 560 and (b[3] - b[1]) > 780:      # imagen de fondo de pagina completa
            continue
        rects.append(b)
    clusters = []
    for r in rects:
        merged = r
        rest = []
        for c in clusters:
            if rect_near(c, merged, 9):
                merged = rect_union(c, merged)
            else:
                rest.append(c)
        clusters = rest + [merged]
    changed = True
    while changed:
        changed = False
        out = []
        for c in clusters:
            for i, o in enumerate(out):
                if rect_near(o, c, 9):
                    out[i] = rect_union(o, c)
                    changed = True
                    break
            else:
                out.append(c)
        clusters = out
    return [c for c in clusters if (c[2] - c[0]) >= 22 and (c[3] - c[1]) >= 14]


def is_label(l: Line) -> bool:
    f = l.font.lower()
    return ('light.condensed' in f or ('condensed' in f and 'bold' not in f and l.size <= 10.5)) \
        and l.size <= 10.5 and not l.bullet


def is_caption(l: Line) -> bool:
    return bool(re.match(r'(Fig\.|Figure|Table|Tabla)\s*\d', l.text.strip())) and l.size <= 10.6


def equation_seed(l: Line) -> bool:
    """Linea de ecuacion (no texto corriente con simbolos en linea)."""
    if l.bad:
        return True
    if l.math:
        body = sum(len(s['text'].strip()) for s in l.spans
                   if not MATH_FONT.search(s['font']) and re.match(r'(Zapf\.Humanist\.601\.(?!Bold)|Zapf)', s['font'])
                   and s['size'] >= 10.5)
        total = len(l.text.strip())
        if total == 0:
            return False
        return body < 28 or body / total < 0.55
    return False


def build_regions(page, lines, tables):
    """Devuelve [(kind, bbox)] con kind en {'fig','eq'} y marca las lineas absorbidas."""
    regions = []
    figs = figure_regions(page, tables)
    taken = set()
    # figuras: absorber etiquetas
    fig_boxes = []
    for f in figs:
        box = f
        grown = True
        while grown:
            grown = False
            for i, l in enumerate(lines):
                if i in taken or is_caption(l):
                    continue
                label_like = is_label(l) or l.size <= 9.5
                short_in = inside(l.bbox, f, 1) and len(l.text.strip()) <= 30 and l.size <= 10.6
                if (label_like and rect_near(box, l.bbox, 14)) or short_in:
                    box = rect_union(box, l.bbox)
                    taken.add(i)
                    grown = True
        fig_boxes.append(box)
    # figuras colindantes en la misma fila -> una sola imagen
    fig_boxes.sort(key=lambda b: b[1])
    merged = []
    for b in fig_boxes:
        for i, m in enumerate(merged):
            ov = min(m[3], b[3]) - max(m[1], b[1])
            if ov > 0.5 * min(m[3] - m[1], b[3] - b[1]) and rect_near(m, b, 40, 0):
                merged[i] = rect_union(m, b)
                break
        else:
            merged.append(b)
    for b in merged:
        regions.append(['fig', b])
    # ecuaciones
    seeds = [i for i, l in enumerate(lines) if i not in taken and equation_seed(l)]
    used = set()
    for i in seeds:
        if i in used:
            continue
        box = lines[i].bbox
        grp = {i}
        grown = True
        while grown:
            grown = False
            for j, l in enumerate(lines):
                if j in grp or j in taken:
                    continue
                short = len(l.text.strip()) <= 26 or l.size <= 9 or l.math or l.bad
                near = rect_near(box, l.bbox, 12, 3)
                if near and short and not is_caption(l) and not (l.bold and l.size >= 11.5):
                    box = rect_union(box, l.bbox)
                    grp.add(j)
                    grown = True
        # absorber etiqueta "Equation x.y.z" si queda adyacente
        used |= grp
        regions.append(['eq', box])
        taken |= grp
    # ecuaciones solapadas entre si o con figuras -> fusionar
    out = []
    for kind, b in sorted(regions, key=lambda r: r[1][1]):
        for o in out:
            if rect_near(o[1], b, 3):
                o[1] = rect_union(o[1], b)
                if kind == 'fig':
                    o[0] = 'fig'
                break
        else:
            out.append([kind, b])
    return out


def render_region(page, bbox, path, kind):
    r = pymupdf.Rect(*bbox)
    pad = 4
    r = pymupdf.Rect(max(0, r.x0 - pad), max(HEAD_Y, r.y0 - pad),
                     min(page.rect.x1, r.x1 + pad), min(FOOT_Y, r.y1 + pad))
    zoom = 2.0 if kind == 'eq' else 1.6
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=r, alpha=False)
    img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    img = img.quantize(colors=96, method=Image.Quantize.MEDIANCUT).convert('P')
    img.save(path, format='PNG', optimize=True)
    return pix.width, pix.height


def table_to_md(tab):
    rows = tab.extract()
    if not rows or len(rows) < 2:
        return None
    ncol = max(len(r) for r in rows)
    if ncol < 2:
        return None
    # celdas combinadas (rowspan) o multilinea: no representables fielmente en Markdown -> imagen
    if any((c or '').count('\n') >= 2 for r in rows for c in r):
        return None
    for r in rows:                      # celdas con varios valores numericos apilados = tabla irregular
        for c in r:
            parts = [x.strip() for x in (c or '').split('\n') if x.strip()]
            if len(parts) >= 2 and any(re.fullmatch(r'[\d\s.,£$€%°<>=+/\-–()]+', x) for x in parts):
                return None
    if any(not (c or '').strip() for c in rows[0][1:]):
        return None
    body_rows = rows[1:]
    if body_rows and sum(1 for r in body_rows if not (r[0] or '').strip()) > 0.3 * len(body_rows):
        return None
    clean = []
    for r in rows:
        cells = [(c or '').replace('\n', ' ').replace('|', '/').strip() for c in r]
        cells += [''] * (ncol - len(cells))
        clean.append(cells)
    filled = sum(1 for r in clean for c in r if c)
    if filled < 0.45 * len(clean) * ncol:
        return None
    if any(BAD.search(c) for r in clean for c in r):
        return None
    hdr = clean[0]
    lines = ['| ' + ' | '.join(h or ' ' for h in hdr) + ' |',
             '|' + '|'.join(' --- ' for _ in hdr) + '|']
    for r in clean[1:]:
        lines.append('| ' + ' | '.join(c or ' ' for c in r) + ' |')
    return '\n'.join(lines)


# --------------------------------------------------------------------------- documento
def convert(pdf_path, md_path, img_dir, img_prefix, chapter_key, title):
    doc = ff.open_fixed(pdf_path)
    os.makedirs(img_dir, exist_ok=True)
    out = [f'# {title}', '']
    para = []          # lineas del parrafo actual
    state = {'last': None, 'img': 0, 'h': None}

    def heading(level, txt):
        flush()
        h = state['h']
        if h and h[0] == level and h[1] == len(out) - 2 and out[-1] == '':
            out[h[1]] = out[h[1]] + ' ' + txt
        else:
            out.append(f"{'#' * level} {txt}")
            out.append('')
            state['h'] = (level, len(out) - 2)

    def flush():
        state['h'] = state['h'] if not para else None
        if para:
            txt = ' '.join(para)
            txt = re.sub(r'(\w)- (?=[a-z])', r'\1-', txt) if False else txt
            txt = re.sub(r'\s+', ' ', txt).strip().replace('** **', ' ')
            if txt:
                out.append(txt)
                out.append('')
            para.clear()

    first_content_page = 1 if len(doc) > 1 else 0
    prev = None
    for pno in range(len(doc)):
        page = doc[pno]
        lines = page_lines(page)
        if pno == 0 and len(doc) > 1 and len(lines) <= 8:
            continue                      # portada
        # tablas
        tables, tbl_md, tbl_img = [], [], []
        try:
            for t in page.find_tables().tables:
                if t.row_count >= 2 and t.col_count >= 2 and t.bbox[3] > HEAD_Y and t.bbox[1] < FOOT_Y:
                    md = table_to_md(t)
                    if md:
                        tables.append(tuple(t.bbox))
                        tbl_md.append((t.bbox[1], md))
                    else:
                        tbl_img.append(tuple(t.bbox))
        except Exception:
            pass
        lines = [l for l in lines if not any(inside(l.bbox, t, 1) for t in tables)]
        regions = build_regions(page, lines, tables)
        for tb in tbl_img:                      # tabla compleja: se conserva como imagen
            regions.append(['fig', tb])
        merged_regions = []
        for kind, b in sorted(regions, key=lambda r: r[1][1]):
            for o in merged_regions:
                if rect_near(o[1], b, 3):
                    o[1] = rect_union(o[1], b)
                    break
            else:
                merged_regions.append([kind, b])
        regions = merged_regions
        taken_boxes = [r[1] for r in regions]
        body = [l for l in lines
                if not any(inside(l.bbox, b, 1.5) for b in taken_boxes) or is_caption(l)]
        # evitar que la leyenda quede dentro de una region renderizada
        elems = []
        for l in body:
            elems.append((l.y0, 0, 'line', l))
        k = 0
        for kind, b in regions:
            k += 1
            elems.append((b[1], -1, 'region', (kind, b, k)))
        for y, md in tbl_md:
            elems.append((y, -1, 'table', md))
        elems.sort(key=lambda e: (e[0], e[1]))
        page_first = True
        for _, _, typ, obj in elems:
            if typ == 'region':
                kind, b, k = obj
                flush()
                state['img'] += 1
                fname = f'{chapter_key}_p{pno:02d}_{k}.png'
                try:
                    render_region(page, b, os.path.join(img_dir, fname), kind)
                    alt = 'Ecuación' if kind == 'eq' else 'Figura'
                    out.append(f'![[{fname}|{alt} (pág. {pno})]]')
                    out.append('')
                except Exception as e:  # pragma: no cover
                    print('   render error', fname, e)
                prev = None
                continue
            if typ == 'table':
                flush()
                out.append(obj)
                out.append('')
                prev = None
                continue
            l = obj
            txt = md_inline(l).strip()
            if not txt:
                continue
            # titulo de capitulo de pagina (se omite: ya esta el H1)
            if l.size >= 15 and pno <= first_content_page:
                continue
            if l.size >= 12.9 and not l.bullet:
                heading(2, txt)
                prev = None
                continue
            if l.bold and l.size >= 11.8 and len(txt) < 110 and not l.bullet:
                heading(3, txt)
                prev = None
                continue
            if is_caption(l):
                flush()
                out.append(f'*{txt}*')
                out.append('')
                prev = None
                continue
            bold_par = False
            if l.bold and not l.bullet:
                if len(txt) <= 75 and not txt.endswith(('.', ',', ';', ':'))                         and (prev is None or l.y0 - prev.y1 > 0.35 * l.size):
                    heading(4, txt)
                    prev = None
                    continue
                bold_par = True
                txt = f'**{txt}**'
            new_par = True
            if prev is not None and not l.bullet:
                if page_first:
                    if para and not re.search(r'[.:;?!]\**$', para[-1].strip()) and txt[:1].islower():
                        new_par = False
                else:
                    gap = l.y0 - prev.y1
                    if gap < 0.55 * l.size and abs(l.size - prev.size) < 1.5:
                        new_par = False
            page_first = False
            if l.bullet:
                flush()
                para.append('- ' + txt)
            elif new_par:
                flush()
                para.append(txt)
            else:
                if para and para[-1].endswith('-') and txt[:1].islower():
                    para[-1] = para[-1] + txt
                else:
                    para.append(txt)
            prev = l
        # continuacion de parrafo entre paginas: se conserva el buffer si no termina en puntuacion
        if para and re.search(r'[.:;?!]$', para[-1].strip()):
            flush()
        elif para and para[0].startswith('- '):
            flush()
    flush()
    text = '\n'.join(out)
    while True:                                                    # listas compactas
        new = re.sub(r'(\n- [^\n]*)\n\n(?=- )', r'\1\n', text)
        if new == text:
            break
        text = new
    text = re.sub(r'\n{3,}', '\n\n', text).rstrip() + '\n\n---\n🏠 Volver al [[000_Indice_Principal|Índice Principal]]\n'
    with open(md_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    return state['img']


def main():
    src, dst = sys.argv[1], sys.argv[2]
    filt = sys.argv[3] if len(sys.argv) > 3 else ''
    pdfs = sorted(glob.glob(os.path.join(src, '*', '*.pdf')),
                  key=lambda p: [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', os.path.basename(p))])
    img_dir = os.path.join(dst, '_figuras')
    for p in pdfs:
        stem = os.path.splitext(os.path.basename(p))[0]
        if filt and filt not in stem:
            continue
        sub = os.path.basename(os.path.dirname(p))
        md_path = os.path.join(dst, sub, stem + '.md')
        os.makedirs(os.path.dirname(md_path), exist_ok=True)
        key = slug(stem)[:48]
        n = convert(p, md_path, img_dir, '../_figuras', key, stem)
        print(f'OK {stem}  imgs={n}')


if __name__ == '__main__':
    main()
