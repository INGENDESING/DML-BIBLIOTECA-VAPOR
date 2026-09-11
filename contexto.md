# Contexto de la Biblioteca de Ingeniería de Vapor

## Historial del Proyecto
- **Autor**: Jonathan Arboleda
- **Objetivo**: Convertir una base de datos de ingeniería (manuales, libros) en una biblioteca web estática altamente eficiente y entrelazada.
- **Tecnología Base**: Obsidian (formato Markdown) y Quartz v5 (Generador de Sitios Estáticos).
- **Repositorio Remoto**: `https://github.com/INGENDESING/DML-BIBLIOTECA-VAPOR.git`

## Origen de los Datos
- Se procesaron 131 archivos PDF (manuales de Spirax Sarco, TLV Válvulas, Trazadores de vapor, etc.) transformándolos a formato Markdown (`.md`).
- Los PDFs originales fueron depurados para construir una base de datos de texto plano liviana, veloz y orientada a ahorrar tokens en procesamiento de IA.

## Estructura de Carpetas (Bóveda de Obsidian / `content/` de Quartz)
El contenido está indexado y estructurado de la siguiente forma:
- `00_Meta`: Índices globales y Mapas de Contenido (ej. `000_Indice_Principal.md`).
- `01_Libro_del_Vapor`: Capítulos del 1 al 16.
- `02_Manuales_Spirax`: Manuales técnicos generales.
- `03_TLV_Valvulas`: Documentación de válvulas TLV.
- `04_Trazadores_Vapor`: Información sobre trazado de tuberías.
- `98_Attachments`: Recursos multimedia (imágenes, adjuntos).
- `99_Templates`: Plantillas de notas estandarizadas.

## Autonomía e Independencia de la IA (Gemini)
El creador del proyecto (Jonathan Arboleda) ha otorgado **permisos de alta independencia** a la IA en este repositorio:
1. **Acción Directa**: No necesitas detenerte a pedir permisos para tareas de mantenimiento rutinarias (ej. formatear un markdown, corregir enlaces rotos, mover notas, hacer commits menores). Ejecuta el comando o herramienta y luego simplemente presenta el resultado.
2. **Proactividad**: Se espera que la IA optimice código (CSS/TS) en Quartz o mejore las estructuras de los documentos (Frontmatter, tags) de manera proactiva para mejorar la biblioteca.
3. **Cero burocracia técnica**: En tareas repetitivas, reduce el diálogo al mínimo, enfócate en ejecutar y notificar el éxito o fracaso, garantizando eficiencia total.
