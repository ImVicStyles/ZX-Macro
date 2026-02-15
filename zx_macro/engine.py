from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from time import sleep


class MacroMode(str, Enum):
    DRAG_EDIT = "drag_edit"
    PULLOUT_SHOTGUN = "pullout_shotgun"


@dataclass
class MacroStep:
    name: str
    delay_ms: int = 0

    def run(self) -> str:
        if self.delay_ms:
            sleep(self.delay_ms / 1000)
        return f"{self.name} (delay {self.delay_ms}ms)"


class MacroEngine:
    def __init__(self) -> None:
        self.delay_ms = 0
        self.drag_edit_key = "E"
        self.select_building_edit_key = "P"
        self.enabled_modes: dict[MacroMode, bool] = {
            MacroMode.DRAG_EDIT: True,
            MacroMode.PULLOUT_SHOTGUN: True,
        }
        self.sequences: dict[MacroMode, list[MacroStep]] = {
            MacroMode.PULLOUT_SHOTGUN: [
                MacroStep("Soltar click (mouse up)"),
                MacroStep("Pulsar tecla 2"),
            ],
        }

    def set_delay(self, delay_ms: int) -> None:
        self.delay_ms = max(0, delay_ms)

    def set_mode_enabled(self, mode: MacroMode, enabled: bool) -> None:
        self.enabled_modes[mode] = enabled

    def set_drag_edit_keys(self, edit_key: str, select_building_edit_key: str) -> None:
        if edit_key:
            self.drag_edit_key = edit_key
        if select_building_edit_key:
            self.select_building_edit_key = select_building_edit_key

    def execute_mode(self, mode: MacroMode) -> str:
        if not self.enabled_modes.get(mode, False):
            return f"El modo {mode.value} está desactivado."
        if mode == MacroMode.DRAG_EDIT:
            steps = [
                MacroStep(
                    f"Pulsar {self.drag_edit_key} para editar y seleccionar"
                    f" ({self.select_building_edit_key})"
                ),
                MacroStep(f"Soltar {self.drag_edit_key} para confirmar"),
            ]
        else:
            steps = self.sequences.get(mode, [])
        results = []
        for step in steps:
            step.delay_ms = self.delay_ms
            results.append(step.run())
        return "Ejecutado: " + ", ".join(results)
