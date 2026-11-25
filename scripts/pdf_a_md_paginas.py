"""PDF con maquetacion compleja (2 columnas, tablas) -> Markdown con imagen de cada pagina + texto.

Uso: python pdf_a_md_paginas.py <archivo.pdf> <salida.md> <carpeta_imagenes> <prefijo_relativo> <titulo> [volver]
El texto sale de pdftotext (xpdf), que decodifica bien las fuentes MS TrueType.
"""
import os
import re
import subprocess
import sys

import pymupdf
from PIL import Image


def main():
    pdf, md, img_dir, rel, title = sys.argv[1:6]
    os.makedirs(img_dir, exist_ok=True)
    doc = pymupdf.open(pdf)
    base = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    out = [f'# {title}', '',
           f'> Documento original de {len(doc)} páginas. Cada página se muestra como imagen fiel al PDF '
           'y, debajo, su texto extraído (para búsqueda y copia).', '']
    for i in range(len(doc)):
        pix = doc[i].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5), alpha=False)
        img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        img = img.quantize(colors=128, method=Image.Quantize.MEDIANCUT).convert('P')
        name = f'{base}_p{i + 1:02d}.png'
        img.save(os.path.join(img_dir, name), format='PNG', optimize=True)
        txt = subprocess.run(['pdftotext', '-q', '-enc', 'UTF-8', '-f', str(i + 1), '-l', str(i + 1), pdf, '-'],
                             capture_output=True).stdout.decode('utf-8', 'ignore')
        txt = txt.replace('\f', '').replace('\r', '')
        paras = [re.sub(r'\s+', ' ', p).strip() for p in re.split(r'\n\s*\n', txt)]
        paras = [p for p in paras if p]
        out += [f'## Página {i + 1}', '', f'![[{name}|Página {i + 1}]]', '']
        if paras:
            out += ['**Texto de la página**', '']
            out += [p + '\n' for p in paras]
    out += ['---', '🏠 Volver al [[000_Indice_Principal|Índice Principal]]', '']
    with open(md, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(out))
    print('OK', md, len(doc), 'paginas')


if __name__ == '__main__':
    main()
