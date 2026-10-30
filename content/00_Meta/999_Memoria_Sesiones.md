# Bitácora de Sesiones (Memoria Persistente)

> Registro append-only. Cada sesión de IA agrega al final una entrada breve (máx. 5 líneas): fecha, qué se hizo, decisiones clave y pendientes. Las entradas nuevas van **arriba**, justo debajo de esta línea.

---

## 2026-10-30 - Sesión: Portal Web Corporativo DML Ingenieros Consultores + Control de Acceso
- **Identidad y UI (`quartz.config.yaml`, `quartz/styles/custom.scss`)**: Rediseño visual corporativo de **DML Ingenieros Consultores** (paleta azul acero `#1b365d` y ámbar térmico `#d97706`, barra superior corporativa `.dml-topbar`, tarjetas `.dml-card`, métricas `.dml-stats` y tablas estilizadas).
- **Control de acceso común (`quartz/components/Body.tsx`)**: Implementado portal de ingreso corporativo (`#dml-access-gate`) para empleados y clientes de DML con código común (`DML2026` / `DML-VAPOR`), persistencia en `localStorage` y botón de bloqueo rápido.
- **Portada e Índice Maestro (`content/index.md`, `000_Indice_Principal.md`)**: Dashboard con diagrama Mermaid del ciclo de vapor, tarjetas interactivas por módulo (01–06), tabla de entregables/Data Sheets (`DS-CAL-001`, `DS-PRS-001`) y capítulos 1–16 ordenados lógicamente.
- **Verificación**: `npx quartz build` exitoso (`exit 0`, 141 notas procesadas, 431 archivos emitidos).

## 2025 - Sesión: sitio caído (404 total) por workflow en conflicto
- **Causa raíz**: `.github/workflows/static.yml` (plantilla default de GitHub Pages) subía el repo crudo (`path: '.'`) sin compilar Quartz, compitiendo con `deploy.yml` en el mismo concurrency group "pages". Cuando ganaba la carrera, el sitio quedaba sin `index.html` → 404 en todas las páginas.
- **Fix**: eliminado `static.yml`. Solo `deploy.yml` (compila Quartz y sube `public/`) debe existir. Si GitHub vuelve a sugerir "Static HTML" en Settings → Pages, no activarlo.
- Verificado tras push: raíz y enlaces a temas responden 200.
- `quartz.config.yaml`: `baseUrl` era el default `quartz.jzhao.xyz` → ahora `ingendesing.github.io/DML-BIBLIOTECA-VAPOR` (sitemap/canónicos correctos); `locale` de `en-US` → `es-ES` (interfaz en español).
- URL del sitio confirmada en línea: https://ingendesing.github.io/DML-BIBLIOTECA-VAPOR/
- El README.md era la plantilla por defecto de Quartz; se reescribió en español como mapa del repo: tabla de carpetas del proyecto (`content/00`-`08`, incluida `07_Hojas_de_Datos` con los data sheets), framework Quartz (no tocar) y comandos básicos.
- Motivo: el usuario no ubicaba la carpeta de hojas de datos desde la raíz (vive en `content/07_Hojas_de_Datos/`).
- `content/Spirax Sarco/` → `content/08_Spirax_Sarco/` (convención numerada, sin espacios); encabezado actualizado en el Índice Principal. La bóveda queda secuencial 00-08.
- Eliminada `docs/` (128 archivos de la plantilla Quartz, ajenos al proyecto; disponibles upstream).
- `contexto.md` actualizado: estructura real 00-08 (antes listaba 98_Attachments/99_Templates inexistentes). `.vs/` ya estaba en `.gitignore`.
- Build verde: 141 notas, exit 0, sin referencias rotas. Los wikilinks no se afectan porque resuelven por nombre de nota, no por carpeta.
- Se creó `content/07_Hojas_de_Datos/` con dos plantillas genéricas de data sheet en Excel: **DS-CAL-001** (calentador tipo EasiHeat) y **DS-PRS-001** (estación reductora PRS), una pestaña por equipo con columnas Campo|Valor|Unidad|Nota y valores del caso 150→25 psig marcados como ejemplo.
- Se generan con `scripts/generar_hojas_datos.py` (openpyxl) — reutilizable para nuevas plantillas. Sección "Identificación del documento" reservada para la **fase 2: formato corporativo (encabezado, portada, código)**.
- Nota [[HojasDeDatos]] enlazada en índice principal y en [[CalentadorAgua]] / [[EstacionesReductoras]]. Build OK: 141 notas; los .xlsx se emiten a `public/` como descargables.
- Pendiente: fase 2 de formato cuando el usuario entregue el encabezado/plantilla corporativa.
- **Sistema de memoria activo**: skill `memoria-boveda`, bootstrap `inicializar.md` (raíz), 4 MOCs temáticos en `00_Meta/`. Para la próxima sesión basta decir "ejecuta inicializar.md".
- **Investigaciones creadas**: [[CalentadorAgua]] (`05_Calentadores_Agua/`) y [[EstacionesReductoras]] (`06_Estaciones_Reductoras/`), ambas con fuentes web y portales CAD 3D. Formato de investigación: frontmatter + secciones numeradas + tablas + fuentes por sección + backlink.
- **Decisiones técnicas clave**: calentador de agua 25→65 °C → vapor recomendado 15 psig; caldera 150 psig → calentador 25 psig requiere PRS de una etapa (relación 6:1) con PRV pilotada (Spirax 25P o TLV COS-16) + safety en baja obligatoria.
- **Flujo de trabajo establecido**: el usuario pide investigación → tabla de instrucciones mejoradas → confirmación → ejecutar hasta el final (investigar, crear carpeta numerada 0X_, integrar en índice+MOC, build Quartz, bitácora, commit+push). Autonomía ALTA confirmada.
- **Estado repo**: último commit `3c9b4e4` en `main`, GitHub Pages despliega automático. Build Quartz verde: 140 notas.

## 2025 - Sesión: Investigación estaciones reductoras de vapor
- Se creó `content/06_Estaciones_Reductoras/EstacionesReductoras.md`: PRS completa (anatomía, tipos de PRV, Spirax 25P, TLV COSPECT, dimensionamiento, caso 150→25 psig, errores comunes, fuentes CAD 3D).
- Fuentes internas clave: manual [[HookUp]] págs. 19-20, Figs. II-13/II-14.
- Enlazada en índice, [[MOC_Control_y_Valvulas]] y cruzada con [[CalentadorAgua]]. Build OK: 140 notas.

## 2025 - Sesión: Fuentes CAD 3D calentadores
- Se agregó sección "Modelos 3D CAD / BIM descargables" a [[CalentadorAgua]]: TraceParts (EasiHeat), BIMobject (Armstrong, AERCO), 3Dfindit, Cemline 3D Drawings, portales genéricos.
- Build Quartz OK.

## 2025 - Sesión: Investigación calentadores de agua
- Se creó `content/05_Calentadores_Agua/CalentadorAgua.md`: investigación web de calentadores instantáneos vapor-agua (Spirax EasiHeat, TLV SteamAqua, Armstrong Digital-Flo/Flo-Rite, AERCO, Cemline, PVI) con capacidades, specs, tabla comparativa y fuentes.
- Enlazado en [[000_Indice_Principal]] y [[MOC_Generacion_y_Energia]]. Build Quartz OK: 139 notas.

## 2025 - Sesión: Sistema de memoria y enlazado
- Se creó el sistema de memoria persistente: skill `memoria-boveda`, `inicializar.md` en raíz y esta bitácora.
- Se agregaron backlinks al [[000_Indice_Principal]] en las 131 notas de contenido.
- Se crearon 4 MOCs temáticos: [[MOC_Generacion_y_Energia]], [[MOC_Ciclo_Condensado]], [[MOC_Trampas_y_Trazadores]], [[MOC_Control_y_Valvulas]].
- Build de Quartz verificado: 138 notas procesadas, 0 enlaces rotos.

🏠 Volver al [[000_Indice_Principal|Índice Principal]]
