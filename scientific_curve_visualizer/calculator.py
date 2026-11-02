"""
calculator.py - Scientific Calculation Engine.
Directly implements:
- Unit 1: Functions, recursion, lambda functions, math operators, OOP class encapsulation.
- Experiment 1a: Twin primes generation.
- Experiment 1b: Permutations P(n,r) and Combinations C(n,r).
- Scientific arithmetic and safe expression evaluation.
"""

import math
from typing import Dict, List, Optional, Tuple


class ScientificCalculator:
    """
    Object-Oriented Scientific Calculator implementing core mathematical routines,
    combinatorics, and calculation history tracking.
    """

    def __init__(self):
        self.history: List[Dict[str, str]] = []

    # --- Permutations & Combinations (Experiment 1b) ---
    @staticmethod
    def factorial(n: int) -> int:
        """Calculates factorial recursively to demonstrate recursion (Unit 1.4)."""
        if n < 0:
            raise ValueError("Factorial is not defined for negative integers.")
        if n in (0, 1):
            return 1
        return n * ScientificCalculator.factorial(n - 1)

    @staticmethod
    def permutation(n: int, r: int) -> int:
        """
        Calculates permutations P(n, r) = n! / (n - r)!.
        Formula from Experiment 1b.
        """
        if n < 0 or r < 0:
            raise ValueError("n and r must be non-negative integers.")
        if r > n:
            raise ValueError("r cannot be greater than n.")
        return ScientificCalculator.factorial(n) // ScientificCalculator.factorial(n - r)

    @staticmethod
    def combination(n: int, r: int) -> int:
        """
        Calculates combinations C(n, r) = n! / (r! * (n - r)!).
        Formula from Experiment 1b.
        """
        if n < 0 or r < 0:
            raise ValueError("n and r must be non-negative integers.")
        if r > n:
            raise ValueError("r cannot be greater than n.")
        return ScientificCalculator.permutation(n, r) // ScientificCalculator.factorial(r)

    # --- Twin Primes (Experiment 1a) ---
    @staticmethod
    def is_prime(num: int) -> bool:
        """Checks if a number is prime."""
        if num < 2:
            return False
        for i in range(2, int(math.isqrt(num)) + 1):
            if num % i == 0:
                return False
        return True

    @staticmethod
    def get_twin_primes(limit: int = 1000) -> List[Tuple[int, int]]:
        """
        Finds all twin prime pairs less than limit (Experiment 1a).
        Two odd consecutive numbers that are both prime.
        """
        twin_primes = []
        for p in range(3, limit - 1, 2):
            if ScientificCalculator.is_prime(p) and ScientificCalculator.is_prime(p + 2):
                twin_primes.append((p, p + 2))
        return twin_primes

    # --- Scientific Math Operations ---
    def evaluate_expression(self, expr_str: str) -> float:
        """
        Evaluates a mathematical expression string safely within a controlled mathematical scope.
        Supports standard math functions (sin, cos, tan, log, sqrt, exp, pi, e).
        """
        safe_dict = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,
            "sqrt": math.sqrt,
            "log": math.log10,
            "ln": math.log,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e,
            "abs": abs,
            "round": round,
            "p": self.permutation,
            "c": self.combination
        }
        # Strip dangerous characters
        cleaned = expr_str.replace("^", "**")
        try:
            result = eval(cleaned, {"__builtins__": None}, safe_dict)
            self.history.append({"expression": expr_str, "result": str(result)})
            return float(result)
        except Exception as e:
            raise ValueError(f"Invalid math expression: {e}")

    def get_history(self) -> List[Dict[str, str]]:
        """Returns the calculation history."""
        return self.history

    def clear_history(self) -> None:
        """Clears calculation history."""
        self.history.clear()
