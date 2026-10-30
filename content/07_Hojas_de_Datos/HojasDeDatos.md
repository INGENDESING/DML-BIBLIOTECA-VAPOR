---
title: Hojas de Datos (Data Sheets) de Ingeniería
tags:
  - hojas-de-datos
  - plantillas
  - ingenieria
---

# Hojas de Datos (Data Sheets) de Ingeniería

Plantillas genéricas de hojas de datos en formato Excel para los equipos del proyecto. **Fase 1: sin formato corporativo** — solo estructura de campos. En la fase 2 se agregará encabezado, portada y código de documento con formato (la sección "Identificación del documento" ya está reservada en cada hoja para eso).

## Archivos

| Código | Documento | Archivo Excel |
|---|---|---|
| DS-CAL-001 | Calentador Instantáneo de Agua a Vapor (tipo EasiHeat) | [DS-CAL-001_Calentador_EasiHeat_Plantilla.xlsx](DS-CAL-001_Calentador_EasiHeat_Plantilla.xlsx) |
| DS-PRS-001 | Estación Reductora de Presión de Vapor (PRS) | [DS-PRS-001_Estacion_Reductora_Plantilla.xlsx](DS-PRS-001_Estacion_Reductora_Plantilla.xlsx) |

## Estructura de cada plantilla

Una sola pestaña por equipo (imprimible en una página), con columnas **Campo | Valor | Unidad | Nota/Referencia** y secciones:

- **DS-CAL-001 (EasiHeat)**: identificación del equipo, condiciones de diseño lado agua y lado vapor, construcción y materiales, control e instrumentación, conexiones y suministros, notas.
- **DS-PRS-001 (PRS)**: identificación de la estación, condiciones de diseño (presiones y flujos), válvula reductora (tipo, tamaño, Cv), válvula de seguridad (obligatoria en baja), componentes de la estación en orden de flujo, notas.

Las celdas con valores del **caso 150→25 psig** están marcadas como "(ejemplo)" y sirven de guía; la plantilla se reutiliza reemplazando valores.

## Regenerar / crear nuevas plantillas

Las hojas se generan con el script `scripts/generar_hojas_datos.py` (raíz del repo, requiere `openpyxl`). Para agregar una plantilla nueva, definir sus secciones en el script y ejecutar:

```bash
python scripts/generar_hojas_datos.py
```

## Relación con la bóveda

- Investigación del calentador: [[CalentadorAgua]]
- Investigación de la estación reductora: [[EstacionesReductoras]]

🏠 Volver al [[000_Indice_Principal|Índice Principal]]
