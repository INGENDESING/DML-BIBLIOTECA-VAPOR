---
title: Estaciones Reductoras de Presión de Vapor (PRS)
tags:
  - vapor
  - estaciones-reductoras
  - valvulas
  - investigacion
---

# Estaciones Reductoras de Presión de Vapor (PRS)

Investigación de fuentes internas (bóveda) y web (comercial y técnica) sobre estaciones reductoras de presión de vapor: componentes, tipos de válvulas, selección, dimensionamiento e instalación.

## 1. Introducción: por qué reducir presión

Reducir la presión del vapor entre la caldera y los equipos de proceso es una práctica estándar por cuatro razones (ver [[10.1 Introduction]] y [[8.1 Pressure control applications]]):

1. **Energía**: a menor presión, el vapor tiene **mayor calor latente por kg** → mejor aprovechamiento en intercambiadores.
2. **Seguridad y costo**: los equipos y tuberías de baja presión son más baratos y seguros (ej. calentadores con PMA de 145 psig no pueden recibir 150 psig directo).
3. **Control**: la temperatura del vapor saturado es función directa de su presión → controlar presión es controlar temperatura.
4. **Regulación**: códigos como ASME B31.1 y la PED exigen protección contra sobrepresión del lado de baja.

> Principio clave del manual [[HookUp]] (pág. 19): *"Es un error instalar incluso la mejor válvula reductora en una tubería sin pensar en cómo ayudarla a dar un desempeño óptimo"* — la estación completa importa tanto como la válvula.

## 2. Anatomía de una PRS (componentes en orden)

Basado en el esquema "Typical Pressure Reducing Valve Station" del manual [[HookUp]] (Fig. II-13):

```
VAPOR DE CALDERA (alta presión)
 │
 ├─ 1. Válvula de aislamiento (entrada)
 ├─ 2. Separador de humedad + trampa flotador-termostática  → vapor seco
 ├─ 3. Filtro Y (strainer) — protege el asiento de la PRV
 ├─ 4. Manómetro (lado alta)
 ├─ 5. VÁLVULA REDUCTORA (PRV) — pilotada, directa o neumática
 │      └─ línea de sensado de presión al lado de baja (si es pilotada)
 ├─ 6. Manómetro (lado baja)
 ├─ 7. VÁLVULA DE SEGURIDAD — dimensionada para el 100% del flujo 
 │      con la PRV fallada abierta (obligatoria)
 └─ 8. Válvula de aislamiento (salida) → VAPOR REDUCIDO al proceso
```

Opcionales según aplicación: bypass con globo manual, Spira-tec (detector de pérdidas de la safety valve), check valve en la salida, drip pan elbow en la descarga de la safety.

**Fuentes:** manual [[HookUp]] secciones "Pressure Reducing Stations" (pág. 19) y "Typical Pressure Reducing Valve Station" (Fig. II-13).

## 3. Tipos de válvulas reductoras

Según [[HookUp]] se dividen en tres grupos de operación; se agrega la variante motorizada moderna:

| Tipo | Principio | Precisión | Capacidad | Aplicación típica |
|---|---|---|---|---|
| **Directa (auto-actuada)** | Resorte contra diafragma/pistón, sensa presión aguas abajo directamente | ±10-20% del setpoint | Baja para su tamaño | Punto de uso, cargas pequeñas y constantes ([[7.3 SA pressure controls and applications]]) |
| **Pilotada** | Piloto externo sensa presión de baja por línea de sensado y modula la válvula principal | Alta, estable ante cambios de carga y de presión de entrada | Alta | Procesos industriales, la más usada en PRS |
| **Neumática / motorizada** | Válvula de control con actuador + controlador (PID) | Muy alta, remota | Alta | Cargas muy variables, setpoints remotos, alta turndown |
| **Pilotada multi-piloto** | Varios pilotos intercambiables en el mismo cuerpo (presión, temperatura, on/off) | Alta + funciones combinadas | Alta | Reducción + control de temperatura en un solo cuerpo (Spirax 25-series) |

Desventajas de la directa según HookUp: mayor fluctuación de presión aguas abajo con cargas inestables y baja capacidad relativa — aceptable en aplicaciones simples.

**Fuentes:** [[HookUp]] "Types of Pressure Reducing Valves"; [Spirax Sarco pressure regulators brochure (PDF)](https://bayportvalve.com/pdffiles/spirax%20sarco/spiraxpressureregulatorsbrochure.pdf)

## 4. Productos comerciales por fabricante

### 4.1 Spirax Sarco

| Modelo | Tipo | Tamaños | Notas |
|---|---|---|---|
| **25P / 25PA** | Pilotada auto-actuada | ½" a 4" (25P hasta 5" según variante) | Cierre ANSI/FCI 70-2 Clase IV; pilotos intercambiables en el mismo cuerpo (presión, temperatura, on/off remoto); cuerpo hierro dúctil o acero, obturador con Stellite; ANSI 150/300 |
| **DP17 / DP25** | Pilotada (mercado europeo) | DN15-DN100+ | Equivalente EN de la serie 25 |
| **BRV2 / BRV71 / BRV73** | Directa | roscada / bridada | Compacta, punto de uso; internos inoxidables |
| **SRV66 / DEP** | Directa, vapor limpio | sanitario | Vapor limpio/puro farmacéutico |

- [IOM oficial 25P/25PA/26P/26PA — Spirax Sarco (PDF)](https://content.spiraxsarco.com/-/media/spiraxsarco/international/documents/us/im/type_25p_25pa_26p_26pa--im-p717-06-us.ashx?rev=9c6b86c843204349a5119178ef551065)
- [Operación de la 25P — MSEC Inc.](https://msecinc.com/blog/operation-of-the-spirax-sarco-25p-pressure-reducing-valve/)
- [25P datasheet — Ohio Pipe (PDF)](https://www.ohpipe.com/wp-content/uploads/2021/04/25P-pressure-regulator-.5-to-4-inches.pdf)

### 4.2 TLV — COSPECT® (COS-3 / COS-16 / COS-21)

PRV pilotada "todo en uno": integra **filtro, separador ciclónico SCE (98% eficiencia) y trampa Free Float®** en el cuerpo de la válvula.

| Característica | Especificación |
|---|---|
| Calidad de vapor entregado | Hasta 99.8% de sequedad (separador SCE) |
| Pistón | Esférico autoalineante con absorción de choque → precisión de presión secundaria aun en condiciones adversas |
| Ruido | Silenciador integrado en tamaños ≥65 mm |
| Presiones | PN25/40, modelos 3/16/21 bar |
| Variantes | M-COS (motorizada, setpoint remoto), PN-COS (neumática con posicionador) |
| Vida útil reportada | 70% de las COSPECT instaladas con +10 años de servicio ([caso: 22 años, 8→5 barg](https://seditesa.es/valvula-reductora-de-presion-de-tlv-cospect/)) |

- [Datasheet COS-3/COS-16 — TLV (PDF)](https://www.tlv.com/sites/default/files/tlv_assets/product_v2/pdf/e-cos3x-hp.pdf)
- [M-COS motorizada — TLV (PDF)](https://www3.tlv.com/global_pdf/tii/e-mcs3x-hp.pdf)
- [PN-COS-16 neumática — TLV manual (PDF)](https://www3.tlv.com/global_pdf/mana4/65588-ma.pdf)
- [PRVs TLV — Energeia Tech](https://www.energeiatech.com/pressure-reducing-valves)

### 4.3 Otros fabricantes

- **Watson McDaniel**: línea completa de reguladoras pilotadas y directas + guía de ingeniería con prácticas de arranque de PRS ([Engineering Data PDF](https://www.watsonmcdaniel.com/Downloads/Literatures/Engineering-Data.pdf))
- **Armstrong International**: reguladoras de presión serie GP-2000 (pilotadas) — ver su [portal de recursos CAD](https://armstrongfluidtechnology.com/en/resources-and-tools/all-resources-and-tools)

## 5. Selección y dimensionamiento

Del manual [[HookUp]] ("Pressure Reducing Valve Sizing") y [[6.4 Control valve sizing for steam systems]]:

1. **Calcular la carga mássica** de vapor (kg/h o lb/h) que demanda el proceso — nunca dimensionar por diámetro de tubería.
2. **La PRV suele ser más pequeña que la tubería** (1-2 tamaños menos): las altas velocidades de la caída de presión ocurren dentro de la válvula. Sobredimensionar causa *hunting* (oscilación) y desgaste prematuro del asiento.
3. **Relación de reducción**: una sola etapa maneja hasta ~10:1 (ej. 150→15 psig). Relaciones mayores → **dos etapas en serie** con toma intermedia y safety adicional (HookUp Fig. "Two-Stage Pressure Reducing Valve Station").
4. **Turndown alto** (carga mínima << máxima): usar **dos PRV en paralelo** (lead/lag): la lead se tara 2 psi sobre el setpoint y la lag 2 psi debajo (HookUp Fig. II-14). Cada válvula trabaja en su rango de buen control.
5. **Capacidad**: seleccionar por Cv/Kv del fabricante con las presiones reales de entrada/salida — no por tabla genérica.
6. **Safety valve**: dimensionada para el flujo máximo de la PRV fallada abierta con presión de entrada máxima; tarada 10% o ~3-5 psi sobre el setpoint de baja ([[9.3 Safety valve selection]], [[9.4 Safety valve sizing]]).

## 6. Caso aplicado: estación 150 → 25 psig (calentador de agua)

Caso real del proyecto (alimentar un calentador instantáneo de agua, ver [[CalentadorAgua]]):

| Parámetro | Valor |
|---|---|
| Presión de caldera (entrada) | 150 psig (~10.3 barG) |
| Presión requerida | 25 psig (~1.7 barG) → condensación ~130 °C |
| Relación de reducción | 6:1 → **una sola etapa** (límite típico 10:1) |
| Válvula recomendada | Pilotada (Spirax 25P o TLV COS-16) — estabilidad ante la carga variable del calentador |
| Safety en baja | **Obligatoria** (primaria >87 psig exige safety secundaria según TLV); dimensionada a 100% del flujo de la PRV abierta |
| Extras recomendados | Separador + trampa antes de la PRV (vapor húmedo erosiona el asiento), filtro Y, manómetros ambos lados, Spira-tec en la safety |
| Control posterior | La válvula modulante de temperatura del calentador va **después** de la PRS, sobre los 25 psig ya reducidos |

## 7. Errores comunes de instalación

1. **Instalar la PRV sin filtro ni separador**: la escala y el condensado dañan el asiento en meses (la COSPECT existe justamente para resolver esto).
2. **Sobredimensionar la válvula** por diámetro de tubería → oscilación y golpeteo del obturador.
3. **Omitir la válvula de seguridad** del lado de baja — ilegal (ASME/PED) y peligroso.
4. **Línea de sensado mal ubicada**: debe tomarse en tubería recta, a ≥10 diámetros de la PRV y lejos de codos/válvulas que distorsionen la presión.
5. **Arranque rápido**: abrir el vapor de golpe causa golpe de ariete; seguir procedimiento de arranque lento ([[10.3 Steam mains and drainage]], guía Watson McDaniel).
6. **Sin drenaje en la entrada**: todo punto bajo aguas arriba requiere estación de trampa ([[11.11 Selecting steam traps (steam mains, tanks and vats, pressure reducing valves)]]).

## 8. Modelos 3D CAD / BIM descargables

| Fabricante / Equipo | Portal | Formatos | Enlace |
|---|---|---|---|
| TLV (PRVs COSPECT, trampas, control) | **Portal oficial TLV 3D CAD** | STEP gratis | [tlv.com/en-us/download/3dcad](https://www.tlv.com/en-us/download/3dcad) |
| TLV | 3Dfindit | CAD nativo y neutro | [3dfindit.com — TLV](https://www.3dfindit.com/en/cad-bim-library/manufacturer/tlv?path=tlv) |
| TLV | TraceParts | 60+ formatos | [traceparts.com — TLV](https://www.traceparts.com/en/search/tlv?CatalogPath=TLV%3AF_TLV) |
| Spirax Sarco (BRV71/73, SRV66, DRV, DEP, EasiHeat) | TraceParts | STEP, DWG, SOLIDWORKS, Revit, etc. | [traceparts.com — Spirax Sarco](https://www.traceparts.com/en/search/spirax-sarco?CatalogPath=SPIRAX_SARCO%3AF_SPIRAX_SARCO) |
| Spirax Sarco BRV71/73 | TraceParts (ficha directa) | 3D bajo solicitud | [Ficha BRV71/73](https://www.traceparts.com/en/product/spirax-sarco-brv71-and-brv73-pressure-valves?Product=90-22022022-036477) |
| Spirax Sarco | 3D ContentCentral | SOLIDWORKS, STEP, IGES | [3dcontentcentral.com](https://www.3dcontentcentral.com) |
| Armstrong (reguladoras, estaciones) | Generador CAD propio + BIMobject | DWG, STEP, Revit | [armstrongfluidtechnology.com/resources](https://armstrongfluidtechnology.com/en/resources-and-tools/all-resources-and-tools) |
| Genéricos (PRV, estaciones) | GrabCAD, 3Dfindit, BIMobject | STEP, STL, Revit | [grabcad.com](https://grabcad.com), [bimobject.com](https://www.bimobject.com) |

**Notas:** los portales requieren cuenta gratuita. Para el layout de una PRS completa conviene descargar componente por componente (PRV, separador, trampa, safety) del mismo fabricante y ensamblar según el esquema de la sección 2.

## 9. Relación con la bóveda

- Esquemas de instalación PRS (el documento más completo de la bóveda): [[HookUp]] — págs. 19-20, Figs. II-13, II-14, estaciones en serie, paralelo y espacios reducidos
- Teoría de control de presión: [[7.3 SA pressure controls and applications]], [[8.1 Pressure control applications]]
- Válvulas de seguridad: [[9.1 Introduction to safety valves]] a [[9.5 Safety valve installation]]
- Componentes de la estación: [[12.4 Strainers]], [[12.5 Separators]], [[12.1 Isolation valves (linear movement)]]
- Drenaje y trampas: [[10.3 Steam mains and drainage]], [[MOC_Trampas_y_Trazadores]]
- Aplicación real: [[CalentadorAgua]] (estación 150→25 psig)
- Hoja de datos en Excel (DS-PRS-001): [[HojasDeDatos]]
- Ejemplo de trampa para PRV: [[11.11 Selecting steam traps (steam mains, tanks and vats, pressure reducing valves)]]

## 10. Fuentes generales

1. Manual Spirax Sarco HookUp (bóveda interna) — secciones Pressure Reducing Stations
2. Spirax Sarco — IOM 25P/25PA/26P/26PA y brochure de reguladoras
3. TLV — Datasheets COS-3/COS-16, M-COS, PN-COS; portal oficial 3D CAD
4. Watson McDaniel — Engineering Data (arranque y mantenimiento de PRS)
5. MSEC Inc. — "Operation of the Spirax-Sarco 25P"
6. SEDITESA — caso de éxito COSPECT (22 años de servicio)

🏠 Volver al [[000_Indice_Principal|Índice Principal]]
