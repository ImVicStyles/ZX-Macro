# ZX-Macro

Macro con interfaz y modos configurables para Fortnite.

## Iniciar

```bash
python main.py
```

## Requisitos

- Python 3.10+ (incluye Tkinter en la instalación estándar).
- No requiere plugins adicionales; usa únicamente librerías estándar.

## Modos incluidos

- Drag Edit
- Pullout Shotgun

## Configuración

Los ajustes se guardan en `config.json`, con delay configurable (0ms por defecto) y
hotkeys por modo desde la UI.

### Drag Edit

El modo Drag Edit simula: pulsar la tecla de edición para iniciar/seleccionar el edit
(usando la tecla de select building edit) y confirmar al soltar la tecla de edición.

### Pullout Shotgun

Al soltar el click del ratón, dispara la tecla `2` para sacar la escopeta.
