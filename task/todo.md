# Plan de Trabajo: Portal Web Técnico de Ingeniería de Vapor — DML INGENIEROS CONSULTORES

## 1. Análisis del Problema y Archivos Relevantes
El objetivo es transformar la actual bóveda publicada en Quartz v5 en un **portal web técnico, corporativo, visualmente atractivo, coherente y lógico** para **DML INGENIEROS CONSULTORES**, protegido mediante un **código de ingreso común** para empleados y clientes de DML, manteniendo la simplicidad y sin alterar las 141 notas técnicas existentes.

### Archivos relevantes identificados:
- [`quartz.config.yaml`](../quartz.config.yaml): Configuración del título corporativo (`DML INGENIEROS CONSULTORES | Biblioteca de Vapor`), tipografía técnica, paleta de colores industrial (modo claro y oscuro) y enlaces de pie de página.
- [`quartz/components/Body.tsx`](../quartz/components/Body.tsx) y [`quartz/components/renderPage.tsx`](../quartz/components/renderPage.tsx): Contenedor global del sitio donde se inyectará de forma simple y limpia la barra superior corporativa DML y el **Portal de Acceso con Código de Ingreso Común** (validado en cliente con `localStorage` para no alterar las notas Markdown de Obsidian).
- [`quartz/styles/custom.scss`](../quartz/styles/custom.scss): Hoja de estilos personalizada para la identidad visual de DML (tarjetas/cards de módulos técnicos, hero banner corporativo, pantalla de login/acceso DML, tablas de ingeniería estilizadas, badges técnicos y diseño responsivo).
- [`content/index.md`](../content/index.md): Portada principal del sitio web, que pasará de ser un texto simple a un **Dashboard Técnico Visual** con Hero Corporativo DML, diagrama interactivo Mermaid del Ciclo Completo de Vapor y Condensado, tarjetas visuales de acceso rápido por especialidad y acceso directo a Hojas de Datos (`DS-CAL-001`, `DS-PRS-001`) y modelos CAD 3D.
- [`content/00_Meta/000_Indice_Principal.md`](../content/00_Meta/000_Indice_Principal.md): Mejora visual y estructural del Índice Principal para que la navegación por los 8 módulos (`01` a `08`) y los 4 Mapas Temáticos (MOCs) sea lógica, clara y coherente con la portada.

---

## 2. Lista de Tareas Pendientes (Checklist)

- [x] **Tarea 1 — Identidad Corporativa y Paleta Técnica en `quartz.config.yaml`**
  - Actualizar `pageTitle` y `pageTitleSuffix` con la marca **DML INGENIEROS CONSULTORES**.
  - Configurar paleta de colores técnica industrial (azul acero profundo `#1b365d`, acento térmico/vapor `#d97706` / `#284b63`, grises neutros de alta legibilidad en modo claro y oscuro).
  - Actualizar los enlaces del `footer` con la identidad de DML Ingenieros Consultores.

- [x] **Tarea 2 — Sistema de Control de Acceso con Código Común DML (`quartz/components/Body.tsx`)**
  - Implementar en `Body.tsx` una pantalla de bloqueo corporativa (**Acceso Exclusivo — Empleados y Clientes DML INGENIEROS CONSULTORES**) con validación de código de ingreso común y persistencia en `localStorage`, más botón de "Salir / Bloquear" en la cabecera corporativa.
  - Mantener el cambio mínimo y autocontenido en un solo componente sin modificar las 141 notas de la bóveda.

- [x] **Tarea 3 — Diseño Visual y Componentes UI en `quartz/styles/custom.scss`**
  - Diseñar los estilos del **Portal de Acceso DML** (fondo técnico, tarjeta de ingreso, estados de error y transición suave).
  - Crear clases utilitarias limpias para herramientas visuales en Markdown: `.dml-hero` (encabezado principal), `.dml-grid` y `.dml-card` (tarjetas de navegación por especialidad), `.dml-badge` (etiquetas de presión/norma/fabricante) y mejoras visuales en tablas técnicas y diagramas Mermaid.

- [x] **Tarea 4 — Rediseño del Portal de Inicio (`content/index.md`) con Herramientas Visuales**
  - Incorporar Hero Banner de **DML INGENIEROS CONSULTORES — Biblioteca Técnica de Ingeniería de Vapor**.
  - Añadir **Diagrama de Flujo Lógico del Ciclo de Vapor y Condensado (Mermaid)** que conecte visualmente: *Generación (Calderas) → Distribución y PRS → Control e Instrumentación → Usuarios Térmicos (Calentadores/Trazado) → Trampas y Retorno de Condensado*.
  - Estructurar cuadrícula de **Tarjetas Visuales por Especialidad** (Mapas Temáticos MOC, Manuales Spirax Sarco y TLV, Investigaciones de Ingeniería DML, Hojas de Datos Excel descargables y Portales CAD 3D).

- [x] **Tarea 5 — Organización Lógica y Visual del Índice Principal (`content/00_Meta/000_Indice_Principal.md`)**
  - Mejorar la presentación del Índice Principal con bloques de navegación rápida, resumen estadístico del acervo técnico (131 manuales base + investigaciones DML + hojas de datos) y clasificación clara por flujo de proceso.

- [x] **Tarea 6 — Verificación de Compilación Quartz y Registro en Bitácora**
  - Ejecutar `npx quartz build` para verificar que las 141 notas, estilos SCSS, diagramas Mermaid y el portal de acceso compilen sin errores (`exit 0`).
  - Registrar la sesión en `content/00_Meta/999_Memoria_Sesiones.md` y documentar la sección de revisión final en este archivo `task/todo.md`.

---

## 3. Sección de Revisión (Resumen de Cambios Realizados)

### Resumen Ejecutivo
Se transformó la biblioteca en el **Portal Técnico de Ingeniería de Vapor de DML INGENIEROS CONSULTORES**, manteniendo el principio de máxima simplicidad y sin alterar las 141 notas técnicas de la bóveda:

1. **Configuración y Marca Corporativa (`quartz.config.yaml`)**:
   - Se actualizó `pageTitle` a `DML Biblioteca de Vapor` con sufijo ` | DML Ingenieros Consultores`.
   - Se aplicó una paleta técnica industrial (azul acero `#1b365d`, acento térmico `#d97706` y fondos de alto contraste en modo claro y oscuro).
   - Se ocultó la tabla cruda de propiedades YAML (`hidePropertiesView: true`) para una presentación limpia.

2. **Portal de Ingreso con Código Común (`quartz/components/Body.tsx`)**:
   - Se incorporó el modal corporativo `#dml-access-gate` y la barra superior `.dml-topbar` como hermanos previos a `#quartz-body` (preservando intacto el CSS Grid nativo de Quartz).
   - Códigos de ingreso habilitados (insensibles a mayúsculas/minúsculas): **`DML2026`**, **`DML-VAPOR`** (y **`DML`**).
   - El estado de sesión se guarda en `localStorage` (`dml_vapor_access_v1`) para que empleados y clientes naveguen fluidamente entre las 141 notas sin volver a pedir clave, e incluye el botón **`🔒 Bloquear`** en la esquina superior derecha.

3. **Herramientas Visuales y Estilos (`quartz/styles/custom.scss`)**:
   - Se crearon componentes visuales reutilizables: `.dml-hero` (encabezado corporativo), `.dml-stats` (indicadores clave), `.dml-grid` y `.dml-card` (tarjetas interactivas con elevación hover), `.dml-badge` (etiquetas de especialidad) y mejoras en tablas y diagramas Mermaid.

4. **Dashboard de Inicio e Índice Maestro (`content/index.md` y `content/00_Meta/000_Indice_Principal.md`)**:
   - Se diseñó el dashboard principal con un **diagrama interactivo Mermaid del Ciclo Completo de Vapor y Condensado**, 6 tarjetas de módulos técnicos, y tabla de acceso directo a **Hojas de Datos Excel (`DS-CAL-001`, `DS-PRS-001`)**, **Modelos 3D CAD/BIM** y manuales Spirax Sarco / TLV.
   - Se reordenó el Índice Maestro (`000_Indice_Principal.md`) de forma numérica y lógica (Capítulos 1 al 16) conservando todos los wikilinks existentes.

5. **Verificación**:
   - Compilación validada con `npx quartz build` (`exit 0`, 141 archivos Markdown procesados y 431 archivos estáticos generados en `public/`).
