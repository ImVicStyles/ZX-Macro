import json
import tkinter as tk
from dataclasses import dataclass, asdict
from pathlib import Path
from tkinter import ttk, messagebox

from zx_macro.engine import MacroEngine, MacroMode

CONFIG_PATH = Path("config.json")


@dataclass
class AppConfig:
    delay_ms: int = 0
    drag_edit_enabled: bool = True
    prefire_enabled: bool = True
    pullout_shotgun_enabled: bool = True
    drag_edit_hotkey: str = "F6"
    prefire_hotkey: str = "F7"
    pullout_shotgun_hotkey: str = "F8"


class ZXMacroApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("ZX Macro")
        self.geometry("540x420")
        self.resizable(False, False)

        self.engine = MacroEngine()
        self.config_data = self._load_config()

        self._build_ui()
        self._sync_ui_from_config()

    def _load_config(self) -> AppConfig:
        if not CONFIG_PATH.exists():
            return AppConfig()
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return AppConfig()
        return AppConfig(**{**asdict(AppConfig()), **data})

    def _save_config(self) -> None:
        data = asdict(self.config_data)
        CONFIG_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def _build_ui(self) -> None:
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#111827")
        self.style.configure("TLabel", background="#111827", foreground="#E5E7EB")
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"))

        container = ttk.Frame(self, padding=16)
        container.pack(fill="both", expand=True)

        header = ttk.Label(container, text="ZX Macro", style="Header.TLabel")
        header.pack(anchor="w")

        desc = ttk.Label(
            container,
            text="Configuraciones rápidas y modos listos para Fortnite.",
        )
        desc.pack(anchor="w", pady=(4, 16))

        settings_frame = ttk.Frame(container)
        settings_frame.pack(fill="x", pady=(0, 16))

        ttk.Label(settings_frame, text="Delay (ms)").grid(row=0, column=0, sticky="w")
        self.delay_var = tk.IntVar(value=0)
        delay_spin = ttk.Spinbox(
            settings_frame,
            from_=0,
            to=200,
            textvariable=self.delay_var,
            width=8,
        )
        delay_spin.grid(row=0, column=1, sticky="w", padx=(8, 16))

        ttk.Label(settings_frame, text="Perfil").grid(row=0, column=2, sticky="w")
        self.profile_var = tk.StringVar(value="Default")
        profile_entry = ttk.Entry(settings_frame, textvariable=self.profile_var, width=18)
        profile_entry.grid(row=0, column=3, sticky="w")

        modes_frame = ttk.Frame(container)
        modes_frame.pack(fill="x")

        ttk.Label(modes_frame, text="Modos").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 8)
        )

        self.drag_edit_enabled_var = tk.BooleanVar(value=True)
        self.prefire_enabled_var = tk.BooleanVar(value=True)
        self.pullout_shotgun_enabled_var = tk.BooleanVar(value=True)

        self.drag_edit_hotkey_var = tk.StringVar()
        self.prefire_hotkey_var = tk.StringVar()
        self.pullout_shotgun_hotkey_var = tk.StringVar()

        self._add_mode_row(
            modes_frame,
            row=1,
            name="Drag Edit",
            enabled_var=self.drag_edit_enabled_var,
            hotkey_var=self.drag_edit_hotkey_var,
            action=lambda: self._run_mode(MacroMode.DRAG_EDIT),
        )
        self._add_mode_row(
            modes_frame,
            row=2,
            name="Prefire Macro",
            enabled_var=self.prefire_enabled_var,
            hotkey_var=self.prefire_hotkey_var,
            action=lambda: self._run_mode(MacroMode.PREFIRE),
        )
        self._add_mode_row(
            modes_frame,
            row=3,
            name="Pullout Shotgun",
            enabled_var=self.pullout_shotgun_enabled_var,
            hotkey_var=self.pullout_shotgun_hotkey_var,
            action=lambda: self._run_mode(MacroMode.PULLOUT_SHOTGUN),
        )

        footer = ttk.Frame(container)
        footer.pack(fill="x", pady=(16, 0))

        save_button = ttk.Button(footer, text="Guardar configuración", command=self._save)
        save_button.pack(side="left")

        apply_button = ttk.Button(footer, text="Aplicar", command=self._apply)
        apply_button.pack(side="right")

    def _add_mode_row(
        self,
        parent: ttk.Frame,
        row: int,
        name: str,
        enabled_var: tk.BooleanVar,
        hotkey_var: tk.StringVar,
        action,
    ) -> None:
        check = ttk.Checkbutton(parent, text=name, variable=enabled_var)
        check.grid(row=row, column=0, sticky="w", pady=4)

        ttk.Label(parent, text="Hotkey").grid(row=row, column=1, sticky="e", padx=(16, 4))
        entry = ttk.Entry(parent, textvariable=hotkey_var, width=10)
        entry.grid(row=row, column=2, sticky="w")

        run_button = ttk.Button(parent, text="Probar", command=action)
        run_button.grid(row=row, column=3, sticky="e", padx=(12, 0))

    def _sync_ui_from_config(self) -> None:
        self.delay_var.set(self.config_data.delay_ms)
        self.drag_edit_enabled_var.set(self.config_data.drag_edit_enabled)
        self.prefire_enabled_var.set(self.config_data.prefire_enabled)
        self.pullout_shotgun_enabled_var.set(self.config_data.pullout_shotgun_enabled)
        self.drag_edit_hotkey_var.set(self.config_data.drag_edit_hotkey)
        self.prefire_hotkey_var.set(self.config_data.prefire_hotkey)
        self.pullout_shotgun_hotkey_var.set(self.config_data.pullout_shotgun_hotkey)

    def _update_config_from_ui(self) -> None:
        self.config_data.delay_ms = int(self.delay_var.get())
        self.config_data.drag_edit_enabled = self.drag_edit_enabled_var.get()
        self.config_data.prefire_enabled = self.prefire_enabled_var.get()
        self.config_data.pullout_shotgun_enabled = self.pullout_shotgun_enabled_var.get()
        self.config_data.drag_edit_hotkey = self.drag_edit_hotkey_var.get().strip()
        self.config_data.prefire_hotkey = self.prefire_hotkey_var.get().strip()
        self.config_data.pullout_shotgun_hotkey = (
            self.pullout_shotgun_hotkey_var.get().strip()
        )

    def _save(self) -> None:
        self._update_config_from_ui()
        self._save_config()
        messagebox.showinfo("ZX Macro", "Configuración guardada.")

    def _apply(self) -> None:
        self._update_config_from_ui()
        self.engine.set_delay(self.config_data.delay_ms)
        self.engine.set_mode_enabled(MacroMode.DRAG_EDIT, self.config_data.drag_edit_enabled)
        self.engine.set_mode_enabled(MacroMode.PREFIRE, self.config_data.prefire_enabled)
        self.engine.set_mode_enabled(
            MacroMode.PULLOUT_SHOTGUN, self.config_data.pullout_shotgun_enabled
        )
        messagebox.showinfo("ZX Macro", "Configuración aplicada.")

    def _run_mode(self, mode: MacroMode) -> None:
        self._apply()
        result = self.engine.execute_mode(mode)
        messagebox.showinfo("ZX Macro", result)


if __name__ == "__main__":
    app = ZXMacroApp()
    app.mainloop()
