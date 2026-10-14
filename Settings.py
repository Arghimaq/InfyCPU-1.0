import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


DEFAULTS = {
    "ram_size": 192,
    "rom_size": 64,
    "window_width": 728,
    "window_length": 728,
    "screen_width": 32,
    "screen_length": 32,
}


class EmulatorSettingsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emulator Settings")
        self.root.geometry("900x680")
        self.root.minsize(760, 580)

        self.vars = {
            key: tk.IntVar(value=value)
            for key, value in DEFAULTS.items()
        }

        self._build_ui()
        self.update_preview()

    def _build_ui(self):
        outer = ttk.Frame(self.root, padding=16)
        outer.pack(fill="both", expand=True)

        ttk.Label(
            outer, text="Emulator Settings",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w")
        ttk.Label(
            outer,
            text="Adjust memory and display settings, preview one pixel, then save them to JSON."
        ).pack(anchor="w", pady=(2, 14))

        content = ttk.Frame(outer)
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        settings = ttk.LabelFrame(content, text="Configuration", padding=12)
        settings.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        preview = ttk.LabelFrame(content, text="Pixel scaling preview", padding=12)
        preview.grid(row=0, column=1, sticky="nsew")

        self._add_slider(settings, "RAM size (units)", "ram_size", 16, 16000, 16)
        self._add_slider(settings, "ROM size (instructions)", "rom_size", 8, 5333, 8)
        self._add_slider(settings, "Window width (px)", "window_width", 320, 1600, 8)
        self._add_slider(settings, "Window height (px)", "window_length", 320, 1200, 8)
        self._add_slider(settings, "Screen width (pixels)", "screen_width", 8, 128, 1)
        self._add_slider(settings, "Screen height (pixels)", "screen_length", 8, 128, 1)

        self.preview_canvas = tk.Canvas(
            preview, width=300, height=300, background="#161a22",
            highlightthickness=1, highlightbackground="#596273"
        )
        self.preview_canvas.pack(fill="both", expand=True, pady=(4, 8))
        self.preview_info = ttk.Label(preview, text="", justify="left")
        self.preview_info.pack(anchor="w")

        actions = ttk.Frame(outer)
        actions.pack(fill="x", pady=(14, 0))
        ttk.Button(actions, text="Save JSON…", command=self.save_json).pack(side="left")
        ttk.Button(actions, text="Load JSON…", command=self.load_json).pack(side="left", padx=8)
        ttk.Button(actions, text="Reset defaults", command=self.reset_defaults).pack(side="left")
        self.status = ttk.Label(actions, text="Ready", anchor="e")
        self.status.pack(side="right", fill="x", expand=True)

    def _add_slider(self, parent, label, key, minimum, maximum, step):
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=6)
        top = ttk.Frame(row)
        top.pack(fill="x")
        ttk.Label(top, text=label).pack(side="left")
        value_label = ttk.Label(top, width=8, anchor="e")
        value_label.pack(side="right")

        scale = tk.Scale(
            row, from_=minimum, to=maximum, resolution=step,
            orient="horizontal", showvalue=False, variable=self.vars[key],
            command=lambda _value: self.update_preview(),
            length=360, highlightthickness=0
        )
        scale.pack(fill="x")
        self.vars[key].trace_add(
            "write", lambda *_args, v=value_label, k=key: v.config(text=str(self.vars[k].get()))
        )
        value_label.config(text=str(self.vars[key].get()))

    def update_preview(self):
        if not hasattr(self, "preview_canvas"):
            return
        canvas = self.preview_canvas
        canvas.delete("all")

        sw = max(1, self.vars["screen_width"].get())
        sh = max(1, self.vars["screen_length"].get())
        ww = max(1, self.vars["window_width"].get())
        wh = max(1, self.vars["window_length"].get())

        canvas.update_idletasks()
        cw = max(1, canvas.winfo_width())
        ch = max(1, canvas.winfo_height())
        cell_w = cw / sw
        cell_h = ch / sh

        # Show a subtle grid only when it remains readable.
        if sw <= 64 and sh <= 64:
            for x in range(sw + 1):
                px = x * cell_w
                canvas.create_line(px, 0, px, ch, fill="#303846")
            for y in range(sh + 1):
                py = y * cell_h
                canvas.create_line(0, py, cw, py, fill="#303846")

        # Highlight the first pixel, scaled to the selected screen dimensions.
        canvas.create_rectangle(
            0, 0, cell_w, cell_h, fill="#ff4040", outline="#ffaaaa", width=1
        )

        self.preview_info.config(
            text=(
                f"Logical screen: {sw} × {sh} pixels\n"
                f"Window: {ww} × {wh} px\n"
                f"Pixel scale: {ww / sw:.2f} × {wh / sh:.2f} window px\n"
                f"RAM: {self.vars['ram_size'].get()} units   "
                f"ROM: {self.vars['rom_size'].get()} instructions"
            )
        )

    def current_settings(self):
        return {key: var.get() for key, var in self.vars.items()}

    def save_json(self):
        try:
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(self.current_settings(), f, indent=4)
            self.status.config(text=f"Saved: settings.json")
        except OSError as exc:
            messagebox.showerror("Save failed", str(exc))

    def load_json(self):
        path = filedialog.askopenfilename(
            title="Load emulator settings",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key, default in DEFAULTS.items():
                if key in data:
                    value = int(data[key])
                    if value <= 0:
                        raise ValueError(f"{key} must be greater than zero")
                    self.vars[key].set(value)
            self.update_preview()
            self.status.config(text=f"Loaded: {path}")
        except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
            messagebox.showerror("Load failed", f"Could not load settings:\n{exc}")

    def reset_defaults(self):
        for key, value in DEFAULTS.items():
            self.vars[key].set(value)
        self.update_preview()
        self.status.config(text="Defaults restored")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmulatorSettingsApp(root)
    root.mainloop()
