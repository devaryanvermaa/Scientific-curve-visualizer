# ⚡ GraphiX — Scientific Function Visualizer (Single-Color Edition)

A minimalist, high-performance mathematical function and curve visualizer desktop application built in Python using **Tkinter**, **NumPy**, and **Matplotlib**. Designed with a unified **Electric Cyan (`#00f2fe`)** signature accent across all elements, real-time parameter sliders, glowing area fills, automated analytical calculus (roots, extrema, definite integrals), and custom formula parsing.

---

## 🌟 Key Features

### 1. 💎 Unified Single-Color Aesthetic
- **One Signature Accent**: Every visual element—from UI controls, header pills, active buttons, formula badges, to the plotted curve, glowing area fill, roots, and extrema—uses a cohesive **Electric Cyan (`#00f2fe`)** theme on deep dark neutrals.
- **Zero Distractions**: Removed all color theme dropdowns and clashing rainbow palettes for a clean, professional, instrument-grade interface.

### 2. 🎛️ Real-Time Interactive Curve Modeling
- **Live Parameter Sliders**: Drag coefficients $a, b, c$ to watch curves reshape instantaneously with zero lag.
- **Dynamic Equation Header**: Real-time formula title reflecting parameter changes (e.g. $f(x) = 1.50x^2 - 2.00x + 0.50$).
- **Function Models Included**:
  - **Quadratic Parabola**: $f(x) = ax^2 + bx + c$
  - **Cubic Polynomial**: $f(x) = ax^3 + bx^2 + cx + d$
  - **Harmonic Waves**: $f(x) = A \cdot \sin(\omega x + \phi)$ & $\cos$
  - **Damped Physical Wave**: $f(x) = A \cdot e^{-\lambda x} \cdot \cos(\omega x)$
  - **Gaussian Bell Curve**: $f(x) = A \cdot \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$
  - **Custom Expression**: Type arbitrary equations e.g. `sin(x) * x`, `x**3 - 4*x`, `exp(-0.2*x) * cos(3*x)`.

### 3. 🎯 Automated Analytical Calculus Card
- **Global Extrema**: Automatically calculates and marks Global Maximum and Global Minimum.
- **Exact Root Zero-Crossings**: Locates where $f(x) = 0$ and highlights them with distinct markers.
- **Definite Integral**: Computes area under curve ($\int_{x_{min}}^{x_{max}} f(x) dx$) using NumPy numerical integration.
- **Statistical Moments**: Computes Mean ($\mu$) and Standard Deviation ($\sigma$).

### 4. 🛠️ Interactive Exploration Controls
- Full Matplotlib Toolbar: Pan, Zoom, Reset axes, and Export high-resolution PNG graphs.
- Custom domain range settings ($X_{min}$, $X_{max}$) and resolution sampling ($N = 100$ to $1500$ points).

---

## 📁 Project Structure

```text
scientific_curve_visualizer/
│
├── plotter_model.py    # NumPy vectorized curve classes & mathematical analytics
├── gui_app.py          # Tkinter GUI (Unified Electric Cyan theme, sliders, embedded canvas)
├── main.py             # Application launcher
├── test_visualizer.py  # Automated unit tests
└── README.md           # Documentation & user guide
```

---

## 🚀 How to Run

### 1. Launch the Visualizer
```powershell
cd "C:\Users\Aryan\.gemini\antigravity\scratch\scientific_curve_visualizer"
python main.py
```

### 2. Run Automated Unit Tests
```powershell
python -m unittest test_visualizer.py
```
*(All 5 unit tests pass cleanly in ~0.3s).*
