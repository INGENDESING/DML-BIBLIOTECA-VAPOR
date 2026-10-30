# INICIALIZAR — Bootstrap de sesión (léeme completo, soy corto)

**Proyecto**: Biblioteca de Ingeniería de Vapor | **Autor**: Jonathan Arboleda
**Stack**: Obsidian (bóveda = `content/`) + Quartz v5 (sitio estático) | Repo: github.com/INGENDESING/DML-BIBLIOTECA-VAPOR
**Autonomía**: ALTA — ejecuta mantenimiento directo, sin pedir permiso en pasos intermedios.

## Paso 1 — Memoria reciente (obligatorio)
Lee solo las primeras 2-3 entradas de `content/00_Meta/999_Memoria_Sesiones.md`.

## Paso 2 — Contexto bajo demanda (NO leas todo)
| Si la tarea trata de... | Lee esto |
|---|---|
| Historial, origen de datos, troubleshooting (build, despliegue) | `contexto.md` |
| Contenido técnico de vapor | Entra por `content/00_Meta/000_Indice_Principal.md` y abre solo las notas necesarias |
| Trampas/trazadores | `content/00_Meta/MOC_Trampas_y_Trazadores.md` |
| Control/válvulas | `content/00_Meta/MOC_Control_y_Valvulas.md` |
| Condensado/distribución | `content/00_Meta/MOC_Ciclo_Condensado.md` |
| Calderas/energía | `content/00_Meta/MOC_Generacion_y_Energia.md` |
| Config del sitio Quartz | `quartz.config.yaml`, `quartz/` |

## Paso 3 — Al terminar
Agrega una entrada breve (máx. 5 líneas, arriba del todo) en `999_Memoria_Sesiones.md`.

## Alertas históricas
- Build de Quartz puede crashear por caracteres ocultos (`\x0C`) en notas nuevas desde PDF → sanitizar.
- Despliegue usa `.github/workflows/deploy.yml` (custom), no el de Quartz por defecto.
