"""PDF con maquetacion compleja (diagramas, tablas, diapositivas) -> Markdown con imagen de cada pagina + texto.

Uso: python pdf_a_md_paginas.py <archivo.pdf> <salida.md> <carpeta_imagenes> <prefijo_imagen> <titulo> [descripcion]

- Cada pagina se muestra como imagen fiel al PDF (![[nombre.png|Pagina N]]) y debajo su texto
  extraido con pdftotext (xpdf, decodifica bien las fuentes), para busqueda y copia.
- Si el PDF trae marcadores (outline), se emiten como encabezados para navegar el documento.
- El archivo lleva frontmatter con titulo amigable (el nombre del .md no cambia: otros enlaces dependen de el).
"""
import os
import re
import subprocess
import sys

import pymupdf
from PIL import Image

ANCHO_OBJETIVO = 1100  # px de ancho de la imagen de pagina


def esc(p):
    """Escapa Markdown/HTML/LaTeX para que el texto del PDF se muestre literal ($ abriria matematicas)."""
    p = re.sub(r'([\\`*_\[\]<>$~|])', lambda m: '\\' + m.group(1), p)
    return re.sub(r'^([#>+\-]|\d+[.)])', lambda m: '\\' + m.group(1), p)


def main():
    pdf, md, img_dir, base, title = sys.argv[1:6]
    desc = sys.argv[6] if len(sys.argv) > 6 else ''
    os.makedirs(img_dir, exist_ok=True)
    doc = pymupdf.open(pdf)
    marcadores = {}
    for lvl, ttl, pg in doc.get_toc():
        if pg and pg > 0:
            marcadores.setdefault(pg, []).append((min(lvl, 3) + 1, ttl.strip()))
    fm = ['---', f'title: "{title}"']
    if desc:
        fm.append(f'description: "{desc}"')
    fm += ['---', '']
    out = fm + [f'# {title}', '',
                f'> Documento original de {len(doc)} páginas. Cada página se muestra como imagen fiel al PDF '
                'y, debajo, su texto extraído (para búsqueda y copia).', '']
    for i in range(len(doc)):
        page = doc[i]
        zoom = max(1.5, min(3.0, ANCHO_OBJETIVO / page.rect.width))
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
        img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        img = img.quantize(colors=128, method=Image.Quantize.MEDIANCUT).convert('P')
        name = f'{base}_p{i + 1:03d}.png'
        img.save(os.path.join(img_dir, name), format='PNG', optimize=True)
        txt = subprocess.run(['pdftotext', '-q', '-enc', 'UTF-8', '-f', str(i + 1), '-l', str(i + 1), pdf, '-'],
                             capture_output=True).stdout.decode('utf-8', 'ignore')
        txt = txt.replace('\f', '').replace('\r', '')
        txt = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', txt)
        paras = [re.sub(r'\s+', ' ', p).strip() for p in re.split(r'\n\s*\n', txt)]
        paras = [esc(p) for p in paras if p]
        for lvl, ttl in marcadores.get(i + 1, []):
            out += ['#' * lvl + ' ' + ttl, '']
        out += [f'##### Página {i + 1}', '', f'![[{name}|Página {i + 1} (de {len(doc)})]]', '']
        if paras:
            out += ['<details><summary>Texto de la página</summary>', '']
            out += [p + '\n' for p in paras]
            out += ['</details>', '']
    out += ['---', '🏠 Volver al [[000_Indice_Principal|Índice Principal]]', '']
    with open(md, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(out))
    print('OK', md, len(doc), 'paginas')


if __name__ == '__main__':
    main()
