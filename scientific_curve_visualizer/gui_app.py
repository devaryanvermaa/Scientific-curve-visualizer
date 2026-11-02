"""
gui_app.py - Minimalist Single-Color Scientific Function Visualizer.
Features:
- Single Unified Signature Accent: Electric Cyan (#00f2fe)
- Real-time vectorized NumPy evaluations
- Dynamic parameter sliders with live re-plotting
- Soft glowing area fill
- Automated analytical calculus: Extrema (Min/Max), Zero-Crossing Roots, Definite Integrals
"""

import sys
import tkinter as tk
from tkinter import ttk
import numpy as np

# Matplotlib integration
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from plotter_model import (
    SIGNATURE_COLOR,
    QuadraticParabola,
    CubicPolynomial,
    HarmonicWave,
    DampedWave,
    GaussianCurve,
    CustomFormulaCurve
)

# Unified Single-Color Palette (Electric Cyan Accent on Dark Neutrals)
THEME = {
    "accent": SIGNATURE_COLOR,   # Single signature color (#00f2fe)
    "bg_window": "#090d16",      # Deep space black
    "bg_panel": "#111827",       # Dark navy card
    "bg_input": "#1f293d",       # Input and control widget background
    "border": "#2e3b52",         # Clean subtle border
    "fg_text": "#f9fafb",        # Crisp bright white
    "fg_muted": "#9ca3af",       # Silver gray
    "plot_bg": "#0d1322",        # Canvas background
    "grid_color": "#1e293b"      # Matrix gridline
}

FONT_NAME = "Segoe UI" if sys.platform.startswith("win") else "Helvetica"


class FunctionVisualizerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("GraphiX — Scientific Function Visualizer")
        self.root.geometry("1180x760")
        self.root.minsize(980, 640)
        self.root.configure(bg=THEME["bg_window"])

        # Active Curve Model
        self.current_curve = QuadraticParabola(a=1.0, b=0.0, c=0.0)
        self.line_width = 2.4

        self._configure_styles()
        self._build_ui()
        self.update_plot()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Dark.TCombobox",
            fieldbackground=THEME["bg_input"],
            background=THEME["bg_panel"],
            foreground=THEME["fg_text"],
            arrowcolor=THEME["accent"],
            borderwidth=1
        )
        style.map(
            "Dark.TCombobox",
            fieldbackground=[("readonly", THEME["bg_input"])],
            foreground=[("readonly", THEME["fg_text"])]
        )

    def _build_ui(self):
        # Top Header Bar
        top_bar = tk.Frame(self.root, bg=THEME["bg_panel"], height=56, padx=20, pady=10)
        top_bar.pack(fill="x", side="top")

        brand_frame = tk.Frame(top_bar, bg=THEME["bg_panel"])
        brand_frame.pack(side="left")

        tk.Label(
            brand_frame,
            text="⚡ GraphiX",
            font=(FONT_NAME, 15, "bold"),
            bg=THEME["bg_panel"],
            fg=THEME["accent"]
        ).pack(side="left")

        tk.Label(
            brand_frame,
            text="Scientific Function & Curve Visualizer",
            font=(FONT_NAME, 10),
            bg=THEME["bg_panel"],
            fg=THEME["fg_muted"]
        ).pack(side="left", padx=12)

        # Quick Preset Buttons in Header
        pills_frame = tk.Frame(top_bar, bg=THEME["bg_panel"])
        pills_frame.pack(side="right")

        def make_pill(text: str, preset_name: str):
            btn = tk.Button(
                pills_frame,
                text=text,
                font=(FONT_NAME, 8, "bold"),
                bg=THEME["bg_input"],
                fg=THEME["fg_text"],
                activebackground=THEME["border"],
                activeforeground=THEME["accent"],
                bd=0,
                padx=10,
                pady=4,
                cursor="hand2",
                command=lambda: self._quick_set(preset_name)
            )
            btn.pack(side="left", padx=3)

        make_pill("Parabola", "Quadratic Parabola")
        make_pill("Sine Wave", "Harmonic Sine Wave")
        make_pill("Damped Wave", "Damped Physical Wave")
        make_pill("Gaussian", "Gaussian Bell Curve")

        # Main Workspace Container
        workspace = tk.Frame(self.root, bg=THEME["bg_window"], padx=10, pady=10)
        workspace.pack(fill="both", expand=True)

        # --- Left Control Sidebar (Scrollable) ---
        sidebar = tk.Frame(workspace, bg=THEME["bg_panel"], width=350, padx=14, pady=12)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)

        side_canvas = tk.Canvas(sidebar, bg=THEME["bg_panel"], highlightthickness=0)
        side_scroll = ttk.Scrollbar(sidebar, orient="vertical", command=side_canvas.yview)
        self.inner_panel = tk.Frame(side_canvas, bg=THEME["bg_panel"])

        self.inner_panel.bind("<Configure>", lambda e: side_canvas.configure(scrollregion=side_canvas.bbox("all")))
        side_win = side_canvas.create_window((0, 0), window=self.inner_panel, anchor="nw")
        side_canvas.configure(yscrollcommand=side_scroll.set)

        side_canvas.pack(side="left", fill="both", expand=True)
        side_scroll.pack(side="right", fill="y")
        side_canvas.bind("<Configure>", lambda e: side_canvas.itemconfig(side_win, width=e.width))

        self._build_sidebar_controls()

        # --- Right Plot Area ---
        plot_container = tk.Frame(workspace, bg=THEME["bg_window"])
        plot_container.pack(side="right", fill="both", expand=True)

        self.fig = Figure(figsize=(7.5, 5.5), dpi=100, facecolor=THEME["bg_window"])
        self.ax = self.fig.add_subplot(111)

        self.canvas_widget = FigureCanvasTkAgg(self.fig, master=plot_container)
        self.canvas_widget.get_tk_widget().pack(fill="both", expand=True)

        # Dark Matplotlib Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas_widget, plot_container)
        self.toolbar.config(background=THEME["bg_panel"])
        self.toolbar.update()

    def _build_sidebar_controls(self):
        # Section 1: Function Model Selector
        tk.Label(
            self.inner_panel,
            text="FUNCTION MODEL",
            font=(FONT_NAME, 8, "bold"),
            bg=THEME["bg_panel"],
            fg=THEME["accent"]
        ).pack(anchor="w", pady=(0, 4))

        self.preset_var = tk.StringVar(value="Quadratic Parabola")
        models = [
            "Quadratic Parabola",
            "Cubic Polynomial",
            "Harmonic Sine Wave",
            "Harmonic Cosine Wave",
            "Damped Physical Wave",
            "Gaussian Bell Curve",
            "Custom Mathematical Formula"
        ]
        self.combo_model = ttk.Combobox(
            self.inner_panel,
            textvariable=self.preset_var,
            values=models,
            state="readonly",
            style="Dark.TCombobox",
            font=(FONT_NAME, 9)
        )
        self.combo_model.pack(fill="x", pady=(0, 8))
        self.combo_model.bind("<<ComboboxSelected>>", self._on_model_changed)

        # Dynamic Formula Display Card
        self.lbl_formula_display = tk.Label(
            self.inner_panel,
            text="f(x) = 1.00x² + 0.00x + 0.00",
            font=(FONT_NAME, 10, "bold"),
            bg=THEME["bg_input"],
            fg=THEME["accent"],
            padx=8,
            pady=6,
            relief="solid",
            bd=1
        )
        self.lbl_formula_display.pack(fill="x", pady=(0, 10))

        # Custom Formula Input (Hidden unless Custom is selected)
        self.frame_custom = tk.Frame(self.inner_panel, bg=THEME["bg_panel"])
        tk.Label(
            self.frame_custom,
            text="Type Expression (use x, sin, cos, exp, etc.):",
            font=(FONT_NAME, 8),
            bg=THEME["bg_panel"],
            fg=THEME["fg_muted"]
        ).pack(anchor="w")
        self.entry_custom = tk.Entry(
            self.frame_custom,
            font=(FONT_NAME, 10),
            bg=THEME["bg_input"],
            fg=THEME["fg_text"],
            insertbackground=THEME["accent"],
            bd=1
        )
        self.entry_custom.insert(0, "sin(x) * x")
        self.entry_custom.pack(fill="x", pady=3, ipady=4)
        self.entry_custom.bind("<Return>", lambda e: self.update_plot())

        # Section 2: Real-time Parameter Sliders
        self.frame_sliders = tk.Frame(self.inner_panel, bg=THEME["bg_panel"])
        self.frame_sliders.pack(fill="x", pady=(0, 10))

        tk.Label(
            self.frame_sliders,
            text="INTERACTIVE PARAMETERS",
            font=(FONT_NAME, 8, "bold"),
            bg=THEME["bg_panel"],
            fg=THEME["accent"]
        ).pack(anchor="w", pady=(0, 4))

        # Slider A
        self.lbl_param_a = tk.Label(self.frame_sliders, text="Leading Coefficient a: 1.00", font=(FONT_NAME, 8), bg=THEME["bg_panel"], fg=THEME["fg_text"])
        self.lbl_param_a.pack(anchor="w")
        self.scale_a = tk.Scale(
            self.frame_sliders,
            from_=-5.0,
            to=5.0,
            resolution=0.05,
            orient="horizontal",
            bg=THEME["bg_panel"],
            fg=THEME["fg_text"],
            troughcolor=THEME["bg_input"],
            highlightthickness=0,
            command=self._on_slider_moved
        )
        self.scale_a.set(1.0)
        self.scale_a.pack(fill="x", pady=(0, 4))

        # Slider B
        self.lbl_param_b = tk.Label(self.frame_sliders, text="Linear Coefficient b: 0.00", font=(FONT_NAME, 8), bg=THEME["bg_panel"], fg=THEME["fg_text"])
        self.lbl_param_b.pack(anchor="w")
        self.scale_b = tk.Scale(
            self.frame_sliders,
            from_=-5.0,
            to=5.0,
            resolution=0.05,
            orient="horizontal",
            bg=THEME["bg_panel"],
            fg=THEME["fg_text"],
            troughcolor=THEME["bg_input"],
            highlightthickness=0,
            command=self._on_slider_moved
        )
        self.scale_b.set(0.0)
        self.scale_b.pack(fill="x", pady=(0, 4))

        # Slider C
        self.lbl_param_c = tk.Label(self.frame_sliders, text="Constant Offset c: 0.00", font=(FONT_NAME, 8), bg=THEME["bg_panel"], fg=THEME["fg_text"])
        self.lbl_param_c.pack(anchor="w")
        self.scale_c = tk.Scale(
            self.frame_sliders,
            from_=-10.0,
            to=10.0,
            resolution=0.1,
            orient="horizontal",
            bg=THEME["bg_panel"],
            fg=THEME["fg_text"],
            troughcolor=THEME["bg_input"],
            highlightthickness=0,
            command=self._on_slider_moved
        )
        self.scale_c.set(0.0)
        self.scale_c.pack(fill="x", pady=(0, 4))

        # Section 3: Domain & Sampling
        tk.Label(
            self.inner_panel,
            text="DOMAIN RANGE",
            font=(FONT_NAME, 8, "bold"),
            bg=THEME["bg_panel"],
            fg=THEME["accent"]
        ).pack(anchor="w", pady=(6, 4))

        domain_grid = tk.Frame(self.inner_panel, bg=THEME["bg_panel"])
        domain_grid.pack(fill="x", pady=(0, 6))

        tk.Label(domain_grid, text="X Min:", font=(FONT_NAME, 8), bg=THEME["bg_panel"], fg=THEME["fg_muted"]).grid(row=0, column=0, sticky="w")
        self.ent_xmin = tk.Entry(domain_grid, width=7, bg=THEME["bg_input"], fg=THEME["fg_text"], insertbackground=THEME["accent"], bd=1)
        self.ent_xmin.insert(0, "-8.0")
        self.ent_xmin.grid(row=0, column=1, padx=4, pady=2)
        self.ent_xmin.bind("<Return>", lambda e: self.update_plot())

        tk.Label(domain_grid, text="X Max:", font=(FONT_NAME, 8), bg=THEME["bg_panel"], fg=THEME["fg_muted"]).grid(row=0, column=2, sticky="w")
        self.ent_xmax = tk.Entry(domain_grid, width=7, bg=THEME["bg_input"], fg=THEME["fg_text"], insertbackground=THEME["accent"], bd=1)
        self.ent_xmax.insert(0, "8.0")
        self.ent_xmax.grid(row=0, column=3, padx=4, pady=2)
        self.ent_xmax.bind("<Return>", lambda e: self.update_plot())

        # Points Slider
        tk.Label(self.inner_panel, text="NumPy Resolution (Sample Points):", font=(FONT_NAME, 8), bg=THEME["bg_panel"], fg=THEME["fg_muted"]).pack(anchor="w")
        self.scale_density = tk.Scale(
            self.inner_panel,
            from_=100,
            to=1500,
            resolution=100,
            orient="horizontal",
            bg=THEME["bg_panel"],
            fg=THEME["fg_text"],
            troughcolor=THEME["bg_input"],
            highlightthickness=0,
            command=lambda v: self.update_plot()
        )
        self.scale_density.set(500)
        self.scale_density.pack(fill="x", pady=(0, 10))

        # Section 4: Display Options (Toggles)
        tk.Label(
            self.inner_panel,
            text="DISPLAY OPTIONS",
            font=(FONT_NAME, 8, "bold"),
            bg=THEME["bg_panel"],
            fg=THEME["accent"]
        ).pack(anchor="w", pady=(4, 4))

        self.var_fill = tk.BooleanVar(value=True)
        chk_fill = tk.Checkbutton(
            self.inner_panel,
            text="Glow Gradient Area Fill",
            variable=self.var_fill,
            bg=THEME["bg_panel"],
            fg=THEME["fg_text"],
            selectcolor=THEME["bg_input"],
            activebackground=THEME["bg_panel"],
            command=self.update_plot
        )
        chk_fill.pack(anchor="w", pady=1)

        self.var_extrema = tk.BooleanVar(value=True)
        chk_extrema = tk.Checkbutton(
            self.inner_panel,
            text="Highlight Roots & Extrema",
            variable=self.var_extrema,
            bg=THEME["bg_panel"],
            fg=THEME["fg_text"],
            selectcolor=THEME["bg_input"],
            activebackground=THEME["bg_panel"],
            command=self.update_plot
        )
        chk_extrema.pack(anchor="w", pady=1)

        self.var_grid = tk.BooleanVar(value=True)
        chk_grid = tk.Checkbutton(
            self.inner_panel,
            text="Show Coordinate Grid",
            variable=self.var_grid,
            bg=THEME["bg_panel"],
            fg=THEME["fg_text"],
            selectcolor=THEME["bg_input"],
            activebackground=THEME["bg_panel"],
            command=self.update_plot
        )
        chk_grid.pack(anchor="w", pady=(1, 10))

        # Section 5: Real-time Analytics Card
        tk.Label(
            self.inner_panel,
            text="ANALYTICAL CALCULUS",
            font=(FONT_NAME, 8, "bold"),
            bg=THEME["bg_panel"],
            fg=THEME["accent"]
        ).pack(anchor="w", pady=(4, 4))

        self.card_analytics = tk.Label(
            self.inner_panel,
            text="Computing analytics...",
            font=("Consolas", 8),
            bg=THEME["bg_input"],
            fg=THEME["fg_text"],
            justify="left",
            padx=10,
            pady=10,
            relief="solid",
            bd=1
        )
        self.card_analytics.pack(fill="x", pady=(0, 10))

    def _quick_set(self, preset_name: str):
        self.preset_var.set(preset_name)
        self._on_model_changed()

    def _on_model_changed(self, event=None):
        choice = self.preset_var.get()

        if choice == "Quadratic Parabola":
            self.frame_custom.pack_forget()
            self.frame_sliders.pack(fill="x", pady=(0, 10))
            self.lbl_param_a.config(text="Leading Coefficient a:")
            self.lbl_param_b.config(text="Linear Coefficient b:")
            self.lbl_param_c.config(text="Constant Offset c:")
            self.scale_a.set(1.0)
            self.scale_b.set(0.0)
            self.scale_c.set(0.0)
            self.current_curve = QuadraticParabola(1.0, 0.0, 0.0)

        elif choice == "Cubic Polynomial":
            self.frame_custom.pack_forget()
            self.frame_sliders.pack(fill="x", pady=(0, 10))
            self.lbl_param_a.config(text="Cubic Coefficient a:")
            self.lbl_param_b.config(text="Quadratic Coeff b:")
            self.lbl_param_c.config(text="Linear Coeff c:")
            self.scale_a.set(1.0)
            self.scale_b.set(0.0)
            self.scale_c.set(-3.0)
            self.current_curve = CubicPolynomial(1.0, 0.0, -3.0)

        elif "Harmonic" in choice:
            self.frame_custom.pack_forget()
            self.frame_sliders.pack(fill="x", pady=(0, 10))
            self.lbl_param_a.config(text="Amplitude A:")
            self.lbl_param_b.config(text="Frequency ω:")
            self.lbl_param_c.config(text="Phase Shift φ:")
            self.scale_a.set(1.5)
            self.scale_b.set(1.0)
            self.scale_c.set(0.0)
            wave = "cos" if "Cosine" in choice else "sin"
            self.current_curve = HarmonicWave(1.5, 1.0, 0.0, wave_type=wave)

        elif choice == "Damped Physical Wave":
            self.frame_custom.pack_forget()
            self.frame_sliders.pack(fill="x", pady=(0, 10))
            self.lbl_param_a.config(text="Amplitude A:")
            self.lbl_param_b.config(text="Decay Factor λ:")
            self.lbl_param_c.config(text="Angular Frequency ω:")
            self.scale_a.set(2.0)
            self.scale_b.set(0.25)
            self.scale_c.set(3.0)
            self.current_curve = DampedWave(2.0, 0.25, 3.0)

        elif choice == "Gaussian Bell Curve":
            self.frame_custom.pack_forget()
            self.frame_sliders.pack(fill="x", pady=(0, 10))
            self.lbl_param_a.config(text="Peak Height A:")
            self.lbl_param_b.config(text="Center Mean μ:")
            self.lbl_param_c.config(text="Standard Deviation σ:")
            self.scale_a.set(2.5)
            self.scale_b.set(0.0)
            self.scale_c.set(1.5)
            self.current_curve = GaussianCurve(2.5, 0.0, 1.5)

        elif choice == "Custom Mathematical Formula":
            self.frame_sliders.pack_forget()
            self.frame_custom.pack(fill="x", pady=(0, 10))
            formula = self.entry_custom.get().strip() or "sin(x) * x"
            self.current_curve = CustomFormulaCurve(formula)

        self.update_plot()

    def _on_slider_moved(self, val=None):
        choice = self.preset_var.get()
        a = float(self.scale_a.get())
        b = float(self.scale_b.get())
        c = float(self.scale_c.get())

        if choice == "Quadratic Parabola" and isinstance(self.current_curve, QuadraticParabola):
            self.current_curve.update_params(a, b, c)
        elif choice == "Cubic Polynomial" and isinstance(self.current_curve, CubicPolynomial):
            self.current_curve.update_params(a, b, c)
        elif "Harmonic" in choice and isinstance(self.current_curve, HarmonicWave):
            self.current_curve.update_params(max(0.1, abs(a)), max(0.1, abs(b)), c)
        elif choice == "Damped Physical Wave" and isinstance(self.current_curve, DampedWave):
            self.current_curve.update_params(a, max(0.01, abs(b)), c)
        elif choice == "Gaussian Bell Curve" and isinstance(self.current_curve, GaussianCurve):
            self.current_curve.update_params(a, b, max(0.2, abs(c)))

        self.update_plot()

    def update_plot(self):
        """Recalculates NumPy arrays and renders in single-color Electric Cyan theme."""
        try:
            x_min = float(self.ent_xmin.get())
            x_max = float(self.ent_xmax.get())
            if x_min >= x_max:
                return
        except ValueError:
            return

        points = int(self.scale_density.get())

        if self.preset_var.get() == "Custom Mathematical Formula":
            formula = self.entry_custom.get().strip() or "x**2"
            self.current_curve = CustomFormulaCurve(formula)

        try:
            x, y = self.current_curve.compute(x_min, x_max, points)
        except Exception as e:
            self.card_analytics.config(text=f"Expression Error:\n{e}")
            return

        # Update Formula Header Label
        self.lbl_formula_display.config(text=self.current_curve.name)

        # Clear and configure Axes
        self.ax.clear()
        self.ax.set_facecolor(THEME["plot_bg"])

        # 1. Glowing Area Fill (with alpha transparency)
        if self.var_fill.get():
            self.ax.fill_between(x, y, 0, color=THEME["accent"], alpha=0.16)

        # 2. Main Curve Line
        self.ax.plot(
            x, y,
            color=THEME["accent"],
            linewidth=self.line_width,
            label=self.current_curve.name
        )

        # 3. Origin Crosshairs (x=0, y=0)
        self.ax.axhline(0, color="#475569", linestyle="--", linewidth=0.9, alpha=0.7)
        self.ax.axvline(0, color="#475569", linestyle="--", linewidth=0.9, alpha=0.7)

        # 4. Roots & Extrema Markers (Using single matching accent and bright white)
        analytics = self.current_curve.get_curve_analytics()

        if self.var_extrema.get() and analytics:
            # Global Maximum
            max_x, max_y = analytics["max_pt"]
            self.ax.plot(max_x, max_y, marker="o", markersize=7, color="#ffffff", markeredgecolor=THEME["accent"], markeredgewidth=1.5, label=f"Max ({max_x}, {max_y})")

            # Global Minimum
            min_x, min_y = analytics["min_pt"]
            self.ax.plot(min_x, min_y, marker="s", markersize=6, color="#ffffff", markeredgecolor=THEME["accent"], markeredgewidth=1.5, label=f"Min ({min_x}, {min_y})")

            # Roots
            for r_x in analytics.get("roots", []):
                self.ax.plot(r_x, 0, marker="x", markersize=8, color=THEME["accent"], markeredgewidth=2, label=f"Root x={r_x}")

        # Grid and Aesthetics
        if self.var_grid.get():
            self.ax.grid(True, linestyle=":", alpha=0.35, color=THEME["grid_color"])

        self.ax.set_title(self.current_curve.name, color=THEME["fg_text"], fontsize=12, fontweight="bold", pad=12)
        self.ax.set_xlabel("x (Domain)", color=THEME["fg_muted"], fontsize=9)
        self.ax.set_ylabel("f(x) (Range)", color=THEME["fg_muted"], fontsize=9)
        self.ax.tick_params(colors=THEME["fg_muted"], labelsize=8)

        for spine in self.ax.spines.values():
            spine.set_color(THEME["border"])

        # Styled Dark Legend
        self.ax.legend(
            facecolor=THEME["bg_panel"],
            edgecolor=THEME["border"],
            labelcolor=THEME["fg_text"],
            fontsize=8,
            loc="upper right"
        )

        self.fig.tight_layout()
        self.canvas_widget.draw()

        # Update Analytics Card
        roots_display = ", ".join(map(str, analytics.get("roots", []))) if analytics.get("roots") else "None in range"
        self.card_analytics.config(
            text=(
                f"Peak  (Max):   {analytics.get('max_pt', 'N/A')}\n"
                f"Valley (Min):   {analytics.get('min_pt', 'N/A')}\n"
                f"Mean Value μ:   {analytics.get('mean', 'N/A')}\n"
                f"Std Deviation:  {analytics.get('std', 'N/A')}\n"
                f"Integral ∫f(x): {analytics.get('integral', 'N/A')}\n"
                f"Roots (f(x)=0): {roots_display}"
            )
        )


def main():
    root = tk.Tk()
    app = FunctionVisualizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
