from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from time import sleep


class MacroMode(str, Enum):
    DRAG_EDIT = "drag_edit"
    PREFIRE = "prefire"
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
        self.enabled_modes: dict[MacroMode, bool] = {
            MacroMode.DRAG_EDIT: True,
            MacroMode.PREFIRE: True,
            MacroMode.PULLOUT_SHOTGUN: True,
        }
        self.sequences: dict[MacroMode, list[MacroStep]] = {
            MacroMode.DRAG_EDIT: [
                MacroStep("Seleccionar pared"),
                MacroStep("Arrastrar edición"),
                MacroStep("Confirmar edición"),
            ],
            MacroMode.PREFIRE: [
                MacroStep("Preparar arma"),
                MacroStep("Prefire"),
                MacroStep("Reset inmediato"),
            ],
            MacroMode.PULLOUT_SHOTGUN: [
                MacroStep("Cambiar a shotgun"),
                MacroStep("Mantener puntería"),
                MacroStep("Disparo rápido"),
            ],
        }

    def set_delay(self, delay_ms: int) -> None:
        self.delay_ms = max(0, delay_ms)

    def set_mode_enabled(self, mode: MacroMode, enabled: bool) -> None:
        self.enabled_modes[mode] = enabled

    def execute_mode(self, mode: MacroMode) -> str:
        if not self.enabled_modes.get(mode, False):
            return f"El modo {mode.value} está desactivado."
        steps = self.sequences.get(mode, [])
        results = []
        for step in steps:
            step.delay_ms = self.delay_ms
            results.append(step.run())
        return "Ejecutado: " + ", ".join(results)
