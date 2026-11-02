"""
test_visualizer.py - Automated Unit Tests for the Function Visualizer.
"""

import math
import unittest
import numpy as np

from plotter_model import (
    QuadraticParabola,
    CubicPolynomial,
    HarmonicWave,
    DampedWave,
    GaussianCurve,
    CustomFormulaCurve
)


class TestFunctionVisualizer(unittest.TestCase):

    def test_parabola_computation(self):
        parabola = QuadraticParabola(a=1.0, b=0.0, c=0.0)  # f(x) = x^2
        x, y = parabola.compute(x_min=-3.0, x_max=3.0, points=7)

        np.testing.assert_allclose(x, np.array([-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0]))
        np.testing.assert_allclose(y, np.array([9.0, 4.0, 1.0, 0.0, 1.0, 4.0, 9.0]))

        analytics = parabola.get_curve_analytics()
        self.assertEqual(analytics["min_pt"], (0.0, 0.0))
        self.assertIn(0.0, analytics["roots"])

    def test_harmonic_wave(self):
        wave = HarmonicWave(amplitude=2.0, frequency=1.0, wave_type="sin")
        x, y = wave.compute(x_min=0, x_max=math.pi, points=100)
        self.assertAlmostEqual(np.amax(y), 2.0, places=2)

    def test_gaussian_curve(self):
        gauss = GaussianCurve(amplitude=3.0, mu=0.0, sigma=1.0)
        x, y = gauss.compute(x_min=-4.0, x_max=4.0, points=101)
        # Peak at x=0
        analytics = gauss.get_curve_analytics()
        self.assertAlmostEqual(analytics["max_pt"][1], 3.0, places=2)

    def test_custom_formula_and_roots(self):
        custom = CustomFormulaCurve("x**2 - 16")
        x, y = custom.compute(x_min=-6.0, x_max=6.0, points=150)
        analytics = custom.get_curve_analytics()
        self.assertIn("roots", analytics)
        # Roots should be near -4 and 4
        has_pos_4 = any(abs(r - 4.0) < 0.2 for r in analytics["roots"])
        has_neg_4 = any(abs(r - (-4.0)) < 0.2 for r in analytics["roots"])
        self.assertTrue(has_pos_4 and has_neg_4)

    def test_numerical_integral(self):
        parabola = QuadraticParabola(a=1.0, b=0.0, c=0.0)  # integral of x^2 from 0 to 3 is 3^3 / 3 = 9
        x, y = parabola.compute(x_min=0.0, x_max=3.0, points=1000)
        analytics = parabola.get_curve_analytics()
        self.assertAlmostEqual(analytics["integral"], 9.0, places=1)


if __name__ == "__main__":
    unittest.main()
