"""
plotter_model.py - Mathematical Modeling and Vectorized Curve Computations.
Unified single-color mathematical curve explorer with vectorized NumPy evaluations,
numerical calculus, and curve analytics.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
import numpy as np

# Single Unified Signature Accent Color
SIGNATURE_COLOR = "#00f2fe"


class MathematicalCurve(ABC):
    """
    Abstract Base Class for mathematical curves.
    Encapsulates domain generation, vectorized evaluation, and statistical analysis.
    """

    def __init__(self, name: str, line_color: str = SIGNATURE_COLOR, line_style: str = "-"):
        self.name: str = name
        self.line_color: str = line_color
        self.line_style: str = line_style
        self.x_data: Optional[np.ndarray] = None
        self.y_data: Optional[np.ndarray] = None

    def generate_domain(self, x_min: float = -10.0, x_max: float = 10.0, points: int = 500) -> np.ndarray:
        """Generates continuous domain x array using NumPy linspace."""
        if x_min >= x_max:
            raise ValueError("X Min must be strictly less than X Max.")
        self.x_data = np.linspace(x_min, x_max, max(2, points))
        return self.x_data

    @abstractmethod
    def evaluate(self, x: np.ndarray) -> np.ndarray:
        """Vectorized formula evaluation."""
        pass

    def compute(self, x_min: float = -10.0, x_max: float = 10.0, points: int = 500) -> Tuple[np.ndarray, np.ndarray]:
        """Generates domain and evaluates corresponding range values."""
        x = self.generate_domain(x_min, x_max, points)
        y = self.evaluate(x)
        # Sanitize non-finite values (infinities, divide-by-zero)
        self.y_data = np.nan_to_num(y, nan=0.0, posinf=1e4, neginf=-1e4)
        return self.x_data, self.y_data

    def get_curve_analytics(self) -> Dict[str, any]:
        """
        Calculates mathematical characteristics using NumPy:
        - Global Min & Max points (coordinates)
        - Mean and Standard Deviation
        - Zero-crossings (approximate roots)
        - Definite Integral over domain
        """
        if self.y_data is None or len(self.y_data) == 0 or self.x_data is None:
            return {}

        min_idx = int(np.argmin(self.y_data))
        max_idx = int(np.argmax(self.y_data))

        min_pt = (round(float(self.x_data[min_idx]), 3), round(float(self.y_data[min_idx]), 3))
        max_pt = (round(float(self.x_data[max_idx]), 3), round(float(self.y_data[max_idx]), 3))

        y_mean = float(np.mean(self.y_data))
        y_std = float(np.std(self.y_data))

        # Numerical integration (Area under curve)
        if hasattr(np, "trapezoid"):
            integral_val = float(np.trapezoid(self.y_data, self.x_data))
        else:
            integral_val = float(np.trapz(self.y_data, self.x_data))

        # Detect roots (zero-crossings)
        signs = np.sign(self.y_data)
        zero_crossings = np.where(np.diff(signs))[0]
        roots = []
        for idx in zero_crossings[:6]:
            x0 = self.x_data[idx]
            x1 = self.x_data[idx + 1]
            y0 = self.y_data[idx]
            y1 = self.y_data[idx + 1]
            if (y1 - y0) != 0:
                root_x = float(x0 - y0 * (x1 - x0) / (y1 - y0))
            else:
                root_x = float(x0)
            roots.append(round(root_x, 3))

        return {
            "min_pt": min_pt,
            "max_pt": max_pt,
            "mean": round(y_mean, 3),
            "std": round(y_std, 3),
            "integral": round(integral_val, 3),
            "roots": roots
        }


class QuadraticParabola(MathematicalCurve):
    """Quadratic function: f(x) = a*x^2 + b*x + c."""

    def __init__(self, a: float = 1.0, b: float = 0.0, c: float = 0.0):
        super().__init__(name="f(x) = x²", line_color=SIGNATURE_COLOR)
        self.a = a
        self.b = b
        self.c = c
        self._update_name()

    def _update_name(self):
        self.name = f"f(x) = {self.a:.2f}x² + {self.b:.2f}x + {self.c:.2f}"

    def update_params(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c
        self._update_name()

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        return self.a * np.power(x, 2) + self.b * x + self.c


class CubicPolynomial(MathematicalCurve):
    """Cubic polynomial: f(x) = a*x^3 + b*x^2 + c*x + d."""

    def __init__(self, a: float = 1.0, b: float = 0.0, c: float = -3.0, d: float = 0.0):
        super().__init__(name="f(x) = x³ - 3x", line_color=SIGNATURE_COLOR)
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self._update_name()

    def _update_name(self):
        self.name = f"f(x) = {self.a:.2f}x³ + {self.b:.2f}x² + {self.c:.2f}x + {self.d:.2f}"

    def update_params(self, a: float, b: float, c: float, d: float = 0.0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self._update_name()

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        return self.a * np.power(x, 3) + self.b * np.power(x, 2) + self.c * x + self.d


class HarmonicWave(MathematicalCurve):
    """Harmonic wave: f(x) = A * sin(omega*x + phi) or cos."""

    def __init__(self, amplitude: float = 1.5, frequency: float = 1.0, phase: float = 0.0, wave_type: str = "sin"):
        super().__init__(name=f"f(x) = {amplitude:.2f}·{wave_type}({frequency:.2f}x)", line_color=SIGNATURE_COLOR)
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.wave_type = wave_type
        self._update_name()

    def _update_name(self):
        self.name = f"f(x) = {self.amplitude:.2f}·{self.wave_type}({self.frequency:.2f}x + {self.phase:.2f})"

    def update_params(self, amplitude: float, frequency: float, phase: float):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self._update_name()

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        arg = self.frequency * x + self.phase
        if self.wave_type == "cos":
            return self.amplitude * np.cos(arg)
        elif self.wave_type == "tan":
            y = self.amplitude * np.tan(arg)
            y[np.abs(y) > 25] = np.nan
            return y
        return self.amplitude * np.sin(arg)


class DampedWave(MathematicalCurve):
    """Damped physical oscillation: f(x) = A * exp(-lambda*x) * cos(omega*x)."""

    def __init__(self, amplitude: float = 2.0, decay: float = 0.25, frequency: float = 3.0):
        super().__init__(name="f(x) = 2.0·e^(-0.25x)·cos(3.0x)", line_color=SIGNATURE_COLOR)
        self.amplitude = amplitude
        self.decay = decay
        self.frequency = frequency
        self._update_name()

    def _update_name(self):
        self.name = f"f(x) = {self.amplitude:.2f}·e^(-{self.decay:.2f}x)·cos({self.frequency:.2f}x)"

    def update_params(self, amplitude: float, decay: float, frequency: float):
        self.amplitude = amplitude
        self.decay = decay
        self.frequency = frequency
        self._update_name()

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        safe_x = np.clip(x, -5, 30)
        return self.amplitude * np.exp(-self.decay * safe_x) * np.cos(self.frequency * safe_x)


class GaussianCurve(MathematicalCurve):
    """Gaussian bell curve: f(x) = A * exp(-((x - mu)^2) / (2 * sigma^2))."""

    def __init__(self, amplitude: float = 2.5, mu: float = 0.0, sigma: float = 1.5):
        super().__init__(name="f(x) = Gaussian Bell Curve", line_color=SIGNATURE_COLOR)
        self.amplitude = amplitude
        self.mu = mu
        self.sigma = max(0.1, sigma)
        self._update_name()

    def _update_name(self):
        self.name = f"f(x) = {self.amplitude:.2f}·exp(-((x - {self.mu:.1f})²)/(2·{self.sigma:.1f}²))"

    def update_params(self, amplitude: float, mu: float, sigma: float):
        self.amplitude = amplitude
        self.mu = mu
        self.sigma = max(0.1, sigma)
        self._update_name()

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        return self.amplitude * np.exp(-((x - self.mu) ** 2) / (2 * (self.sigma ** 2)))


class CustomFormulaCurve(MathematicalCurve):
    """Evaluates arbitrary user mathematical expressions using NumPy functions."""

    def __init__(self, formula_str: str = "x**2"):
        super().__init__(name=f"f(x) = {formula_str}", line_color=SIGNATURE_COLOR)
        self.formula_str = formula_str

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        safe_env = {
            "x": x,
            "np": np,
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "exp": np.exp,
            "log": np.log,
            "sqrt": np.sqrt,
            "abs": np.abs,
            "pi": np.pi,
            "e": np.e
        }
        cleaned = self.formula_str.replace("^", "**")
        try:
            result = eval(cleaned, {"__builtins__": None}, safe_env)
            if isinstance(result, (int, float)):
                result = np.full_like(x, float(result))
            return np.asarray(result, dtype=float)
        except Exception as e:
            raise ValueError(f"Invalid mathematical expression '{self.formula_str}': {e}")
