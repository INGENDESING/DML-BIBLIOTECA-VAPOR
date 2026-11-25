"""Repara PDFs de Spirax Sarco cuyas fuentes Type1/TrueType no traen /ToUnicode.

Los PDFs usan /Encoding << /Differences [1 /G83 /G111 ...] >> donde G<n> es el
codigo de caracter original (cp1252 para texto normal, codificacion Symbol para
fuentes de simbolos/griegas). Sin /ToUnicode la mayoria de extractores devuelve
basura (\x01\x02\x03...). Aqui se inyecta un /ToUnicode correcto en cada fuente.
"""
import re
import pymupdf

# Codificacion Adobe Symbol (subconjunto relevante para ingenieria)
SYMBOL = {
    65: 'Α', 66: 'Β', 67: 'Χ', 68: 'Δ', 69: 'Ε', 70: 'Φ', 71: 'Γ', 72: 'Η', 73: 'Ι', 74: 'ϑ',
    75: 'Κ', 76: 'Λ', 77: 'Μ', 78: 'Ν', 79: 'Ο', 80: 'Π', 81: 'Θ', 82: 'Ρ', 83: 'Σ', 84: 'Τ',
    85: 'Υ', 86: 'ς', 87: 'Ω', 88: 'Ξ', 89: 'Ψ', 90: 'Ζ',
    97: 'α', 98: 'β', 99: 'χ', 100: 'δ', 101: 'ε', 102: 'φ', 103: 'γ', 104: 'η', 105: 'ι', 106: 'ϕ',
    107: 'κ', 108: 'λ', 109: 'μ', 110: 'ν', 111: 'ο', 112: 'π', 113: 'θ', 114: 'ρ', 115: 'σ', 116: 'τ',
    117: 'υ', 118: 'ϖ', 119: 'ω', 120: 'ξ', 121: 'ψ', 122: 'ζ',
    45: '−', 176: '°', 177: '±', 178: '″', 179: '≥', 180: '×', 181: '∝', 182: '∂', 183: '•',
    184: '÷', 185: '≠', 186: '≡', 187: '≈', 188: '…', 163: '≤', 165: '∞', 171: '↔', 172: '←',
    173: '↑', 174: '→', 175: '↓', 214: '√', 215: '⋅', 217: '∧', 218: '∨', 229: '∑', 242: '∫',
    208: '∇', 198: '∅', 206: '∈', 199: '∩', 200: '∪', 193: 'ϒ', 162: '′', 164: '⁄',
}

_GNAME = re.compile(r'/G(\d+)\b')
_UNINAME = re.compile(r'/uni([0-9A-Fa-f]{4})\b')


def _is_symbolic(basefont: str) -> bool:
    b = basefont.lower()
    return 'symbol' in b or 'greek' in b or 'math' in b and 'text' not in b


def _cp1252(n: int) -> str:
    try:
        return bytes([n]).decode('cp1252')
    except Exception:
        return chr(n)


def _parse_differences(enc_obj: str):
    """Devuelve lista [(codigo, glyphname)] desde un objeto /Differences."""
    m = re.search(r'/Differences\s*\[(.*?)\]', enc_obj, re.S)
    if not m:
        return []
    out, code = [], 0
    for tok in re.findall(r'/[^\s/\[\]]+|\d+', m.group(1)):
        if tok.startswith('/'):
            out.append((code, tok))
            code += 1
        else:
            code = int(tok)
    return out


def _cmap_text(mapping: dict) -> bytes:
    lines = ['/CIDInit /ProcSet findresource begin 12 dict begin begincmap',
             '/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def',
             '/CMapName /Adobe-Identity-UCS def /CMapType 2 def',
             '1 begincodespacerange <00> <FF> endcodespacerange']
    items = sorted(mapping.items())
    for i in range(0, len(items), 100):
        chunk = items[i:i + 100]
        lines.append(f'{len(chunk)} beginbfchar')
        for code, uni in chunk:
            lines.append('<%02X> <%s>' % (code, ''.join('%04X' % ord(c) for c in uni)))
        lines.append('endbfchar')
    lines.append('endcmap CMapName currentdict /CMap defineresource pop end end')
    return '\n'.join(lines).encode('latin-1')


def _gid_to_uni(n: int, symbolic: bool):
    """Glifo por indice (orden estandar de TrueType/Mac: gid 3=space, 4='!', ... 97='~')."""
    if n == 3:
        return ' '
    if 4 <= n <= 97:
        code = n + 29
        return SYMBOL.get(code, chr(code)) if symbolic else chr(code)
    if 98 <= n < 258:
        try:
            from fontTools.ttLib.tables._p_o_s_t import standardGlyphOrder
            from fontTools.agl import toUnicode
            return toUnicode(standardGlyphOrder[n]) or ''
        except Exception:
            return ''
    return ''


def _glyph_to_uni(name: str, symbolic: bool, gid_scheme: bool = False):
    m = re.fullmatch(r'/(?:G|MT|c)(\d+)(?:[._].*)?', name)
    if m:
        n = int(m.group(1))
        if gid_scheme or name.startswith('/c') and not name.startswith('/MT'):
            return _gid_to_uni(n, symbolic)
        if symbolic and n in SYMBOL:
            return SYMBOL[n]
        if n < 32:
            return ''
        return _cp1252(n)
    m = _UNINAME.fullmatch(name)
    if m:
        return chr(int(m.group(1), 16))
    try:
        from fontTools.agl import toUnicode
        u = toUnicode(name[1:])
        return u or ''
    except Exception:
        return ''


def _uses_gid_scheme(diffs) -> bool:
    """Los nombres G<n> pueden ser codigo ASCII (G83='S') o indice de glifo (G3=espacio,
    G54='S'). Si hay numeros 3..31 (digitos/espacio en gid, controles en ASCII) es gid."""
    nums = []
    for _, g in diffs:
        m = re.fullmatch(r'/(?:G|c)(\d+)(?:[._].*)?', g)
        if m:
            nums.append(int(m.group(1)))
    if not nums:
        return False
    if any(g.startswith('/c') for _, g in diffs):
        return True
    return any(3 <= n < 32 for n in nums)


def fix_document(doc: pymupdf.Document) -> int:
    """Inyecta /ToUnicode en las fuentes sin mapa. Devuelve cuantas fuentes se repararon."""
    fixed = 0
    for xref in range(1, doc.xref_length()):
        try:
            obj = doc.xref_object(xref)
        except Exception:
            continue
        if '/Type /Font' not in obj and '/Type/Font' not in obj:
            continue
        if '/FontDescriptor' not in obj or '/Subtype /Type0' in obj or '/Subtype/Type0' in obj:
            continue
        if '/ToUnicode' in obj:
            continue
        m = re.search(r'/Encoding\s+(\d+) 0 R', obj)
        if not m:
            continue
        enc_obj = doc.xref_object(int(m.group(1)))
        diffs = _parse_differences(enc_obj)
        if not diffs:
            continue
        bf = re.search(r'/BaseFont\s*/(\S+)', obj)
        symbolic = _is_symbolic(bf.group(1) if bf else '')
        gid = _uses_gid_scheme(diffs)
        mapping = {}
        for code, gname in diffs:
            if 0 <= code <= 255:
                u = _glyph_to_uni(gname, symbolic, gid)
                if u:
                    mapping[code] = u
        if not mapping:
            continue
        new = doc.get_new_xref()
        doc.update_object(new, '<< >>')
        doc.update_stream(new, _cmap_text(mapping))
        doc.xref_set_key(xref, 'ToUnicode', f'{new} 0 R')
        fixed += 1
    return fixed


def open_fixed(path: str) -> pymupdf.Document:
    doc = pymupdf.open(path)
    fix_document(doc)
    # Re-abrir desde bytes para que MuPDF cargue las fuentes con el nuevo ToUnicode
    data = doc.tobytes()
    doc.close()
    return pymupdf.open('pdf', data)
