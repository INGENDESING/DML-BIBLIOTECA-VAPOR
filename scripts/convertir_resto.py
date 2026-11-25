"""Reconvierte los PDFs que no son del Libro del Vapor (manuales, TLV, trazadores, Colgate)
con pdf_a_md_paginas.py. Uso: python convertir_resto.py [filtro]"""
import os
import subprocess
import sys

B = r"C:\Users\72-MS754\OneDrive\1.0 PROYECTOS DML\ESTANDARES REFERENCIAS\0  Bases de datos Ingenieria\Estudio avanzado vapor"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = os.path.join(RAIZ, 'content')
AQUI = os.path.dirname(os.path.abspath(__file__))

# (pdf relativo, carpeta destino, nombre md, prefijo imagen, titulo, descripcion)
DOCS = [
    (r'Spirax Sarco\Manuales de Ingenieria\HookUp.pdf', '02_Manuales_Spirax', 'HookUp', 'hookup',
     'Manual Hook-Ups: Diseño de Sistemas de Fluidos (Spirax Sarco)',
     'Instalaciones típicas de vapor, condensado, aire y fluidos con diagramas de conexión. Spirax Sarco, 12.ª edición.'),
    (r'Spirax Sarco\Manuales de Ingenieria\Steam.pdf', '02_Manuales_Spirax', 'Steam', 'steam-utilization',
     'Curso de Utilización del Vapor (Spirax Sarco)',
     'Steam Utilization Course: trampas, controles de presión y temperatura, recuperación de condensado y tablas de vapor.'),
    (r'Spirax Sarco\Loop de Vapor & Condensado - 2015  Colgate.pdf', '08_Spirax_Sarco',
     'Loop de Vapor & Condensado - 2015  Colgate', 'loop-vapor-condensado-colgate',
     'Loop de Vapor y Condensado: presentación Colgate 2015',
     'Presentación técnica (diapositivas) del circuito de vapor y condensado, con diagramas de instalación típica.'),
    (r'TLV VALVULAS Y ACCESORIOS\65395-sa.pdf', '03_TLV_Valvulas', '65395-sa', 'tlv-65395-sa',
     'TLV: Trampas de Vapor de Flotador Libre SS1NL/SS1NH/SS1VL/SS1VH, Manual de Instrucciones',
     'Manual de instrucciones de trampas de vapor tipo flotador libre TLV.'),
    (r'TLV VALVULAS Y ACCESORIOS\e-ck3m0-hp.pdf', '03_TLV_Valvulas', 'e-ck3m0-hp', 'tlv-ck3m-check',
     'TLV: Válvulas Check CK3M / CK3T / CK3R (hoja de datos)',
     'Especificaciones, dimensiones y valores Cv de las válvulas de retención TLV CK3M, CK3T y CK3R.'),
    (r'TLV VALVULAS Y ACCESORIOS\e-pamphlet-080201-hp.pdf', '03_TLV_Valvulas', 'e-pamphlet-080201-hp', 'tlv-a3n-pamphlet',
     'TLV: Trampa Termodinámica A3N / AF3N (folleto)',
     'Folleto de la trampa de vapor termodinámica TLV A3N y AF3N: construcción, aplicación y capacidad de descarga.'),
    (r'TLV VALVULAS Y ACCESORIOS\e-ss1nh-hp.pdf', '03_TLV_Valvulas', 'e-ss1nh-hp', 'tlv-ss1-datasheet',
     'TLV: Trampa de Flotador Libre SS1 (hoja de datos)',
     'Trampa de vapor inoxidable reparable en línea para líneas principales, trazadores y procesos pequeños.'),
    (r'TLV VALVULAS Y ACCESORIOS\Trampa termodinamica para trazadores Manual.pdf', '03_TLV_Valvulas',
     'Trampa termodinamica para trazadores Manual', 'tlv-termodinamica-manual',
     'TLV: Trampa Termodinámica para Trazadores, Manual de Instrucciones',
     'Manual de instalación y mantenimiento de la trampa termodinámica TLV A3N para trazadores.'),
    (r'TLV VALVULAS Y ACCESORIOS\Trampa termodinamica para trazadores.pdf', '03_TLV_Valvulas',
     'Trampa termodinamica para trazadores', 'tlv-termodinamica-sds',
     'TLV: Trampa Termodinámica A3N con Venteo de Aire Termostático (hoja de datos)',
     'Hoja de datos SDS SA2004-00: trampa de disco con chaqueta de vapor para líneas principales, trazadores y serpentines.'),
    (r'TLV VALVULAS Y ACCESORIOS\Trampaflotador paraintercambiador 2.pdf', '03_TLV_Valvulas',
     'Trampaflotador paraintercambiador 2', 'tlv-flotador-j7x-sds',
     'TLV: Trampa de Flotador Libre J7X con Venteo de Aire Termostático (hoja de datos)',
     'Hoja de datos SDS SA2000-156: trampa de flotador libre para intercambiadores de calor y procesos.'),
    (r'TLV VALVULAS Y ACCESORIOS\Trampaflotador paraintercambiadormanual.pdf', '03_TLV_Valvulas',
     'Trampaflotador paraintercambiadormanual', 'tlv-flotador-manual',
     'TLV: Trampa de Flotador Libre para Intercambiadores, Manual de Instrucciones',
     'Manual de instrucciones de la trampa de flotador libre TLV para intercambiadores de calor.'),
    (r'Trazadores de vapor\Overview Tracing System.pdf', '04_Trazadores_Vapor', 'Overview Tracing System',
     'thermon-overview-tracing', 'Thermon: Visión General de Sistemas de Trazado de Vapor',
     'Aplicaciones del trazado con vapor, desde protección contra congelamiento hasta mantenimiento de temperatura.'),
    (r'Trazadores de vapor\Steam Tracing Guide Line.pdf', '04_Trazadores_Vapor', 'Steam Tracing Guide Line',
     'steam-tracing-guide-line', 'Guía de Diseño de Trazadores de Vapor (Steam Tracing Guide Line)',
     'Guía de diseño de trazado con vapor: cálculo de pérdidas de calor, número de trazadores, trampas y distribución.'),
    (r'Trazadores de vapor\Tracing Steam  for Vessel.pdf', '04_Trazadores_Vapor', 'Tracing Steam  for Vessel',
     'thermon-heetsheet-vessel', 'Thermon: HeetSheet, Calentamiento de Tanques y Recipientes con Vapor',
     'Unidades HeetSheet para calentamiento de tanques y recipientes: características y funcionamiento.'),
]

filtro = sys.argv[1].lower() if len(sys.argv) > 1 else ''
for rel, carp, nombre, base, titulo, desc in DOCS:
    if filtro and filtro not in nombre.lower():
        continue
    pdf = os.path.join(B, rel)
    md = os.path.join(C, carp, nombre + '.md')
    r = subprocess.run([sys.executable, os.path.join(AQUI, 'pdf_a_md_paginas.py'), pdf, md,
                        os.path.join(C, carp, '_figuras'), base, titulo, desc], capture_output=True, text=True)
    print((r.stdout or r.stderr).strip())
