---
name: memoria-boveda
description: Memoria persistente entre sesiones usando la bóveda Obsidian del proyecto. Usar al iniciar una sesión en este repo, cuando el usuario diga "ejecuta inicializar.md", o al terminar trabajo que deba quedar registrado en la bitácora.
---

# Skill: Memoria Infinita con la Bóveda Obsidian

Este proyecto usa la bóveda Obsidian (`content/`) como memoria persistente entre sesiones de IA. El objetivo es recuperar contexto gastando el **mínimo de tokens**.

## Arranque de sesión (recuperar contexto)

1. Lee `inicializar.md` (raíz del repo). Es el bootstrap: indica qué leer según la tarea.
2. Lee `content/00_Meta/999_Memoria_Sesiones.md` — solo las **primeras 2-3 entradas** (las más recientes están arriba).
3. **NO** leas `contexto.md` ni las notas de la bóveda salvo que la tarea lo exija. Lee bajo demanda:
   - Arquitectura/origen de datos/historial → `contexto.md`
   - Contenido técnico → entra por `content/00_Meta/000_Indice_Principal.md` o el MOC temático correspondiente, y abre solo las notas necesarias.

## Mapas de contenido (MOCs) — navegación rápida

- `content/00_Meta/000_Indice_Principal.md` — índice global de las 131 notas
- `content/00_Meta/MOC_Generacion_y_Energia.md` — calderas, principios, consumo
- `content/00_Meta/MOC_Ciclo_Condensado.md` — loop vapor/condensado
- `content/00_Meta/MOC_Trampas_y_Trazadores.md` — steam traps y tracing
- `content/00_Meta/MOC_Control_y_Valvulas.md` — control e instrumentación

## Cierre de sesión (guardar memoria)

Al terminar trabajo significativo, **sin que te lo pidan**, agrega una entrada en `content/00_Meta/999_Memoria_Sesiones.md`:
- Inserta la entrada nueva **debajo de la línea horizontal superior** (las recientes van primero).
- Máximo 5 líneas: fecha, qué se hizo, decisiones clave, pendientes.
- Si creaste o renombraste notas, verifica que los MOCs afectados sigan correctos.

## Reglas

- Autonomía alta (ver `contexto.md` sección "Autonomía"): ejecuta mantenimiento directo, reporta al final.
- Nunca dupliques contenido de notas dentro de la bitácora; la bitácora guarda **punteros**, no datos.
- Si agregas una nota nueva a la bóveda, enlázala en su MOC correspondiente y agrega el backlink `🏠 Volver al [[000_Indice_Principal|Índice Principal]]` al final.
