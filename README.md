# Biblioteca de Ingeniería de Vapor

Base de conocimiento técnico de ingeniería de vapor (manuales, investigaciones y hojas de datos) publicada como sitio web estático.

- **Autor**: Jonathan Arboleda
- **Stack**: Obsidian (bóveda Markdown) + Quartz v5 (generador de sitio estático)
- **Sitio**: se despliega automáticamente en GitHub Pages al hacer push a `main`

## Dónde está cada cosa

La raíz del repo mezcla el **proyecto** con el **framework Quartz**. Esta es la guía:

### Carpetas del proyecto (lo que te interesa)

| Ruta | Contenido |
|---|---|
| `content/00_Meta/` | Índice principal, mapas temáticos (MOCs) y bitácora de sesiones |
| `content/01_Libro_del_Vapor/` | Libro de Spirax Sarco, capítulos 1-16 |
| `content/02_Manuales_Spirax/` | Manuales técnicos Spirax (HookUp, Steam) |
| `content/03_TLV_Valvulas/` | Documentación de válvulas y trampas TLV |
| `content/04_Trazadores_Vapor/` | Steam tracing |
| `content/05_Calentadores_Agua/` | Investigación: calentadores instantáneos (EasiHeat y similares) |
| `content/06_Estaciones_Reductoras/` | Investigación: estaciones reductoras de presión (PRS) |
| **`content/07_Hojas_de_Datos/`** | **Hojas de datos / data sheets en Excel (DS-CAL-001 EasiHeat, DS-PRS-001 PRS)** |
| `content/08_Spirax_Sarco/` | Casos de aplicación (loop vapor/condensado) |
| `scripts/` | Generador de data sheets Excel (`generar_hojas_datos.py`) |
| `inicializar.md` | Bootstrap de sesión para IA (léelo primero) |
| `contexto.md` | Historial, origen de datos y troubleshooting del proyecto |

### Framework Quartz (no tocar salvo configuración del sitio)

| Ruta | Contenido |
|---|---|
| `quartz/` | Código fuente del generador |
| `quartz.config.yaml` / `quartz.ts` | Configuración del sitio |
| `package.json` / `package-lock.json` | Dependencias Node |
| `public/` | Salida del build (generada, está en `.gitignore`) |
| `node_modules/` | Dependencias instaladas (`.gitignore`) |
| `.github/workflows/` | Despliegue automático a GitHub Pages |

## Comandos

```bash
npx quartz build          # compila el sitio a public/
npx quartz build --serve  # compila y sirve en local (localhost:8080)
python scripts/generar_hojas_datos.py   # regenera los data sheets Excel
```
