"""Buffon's needle, short needle case (l <= t)

Throw:
x ~ U(0, t/2): distance from the needle centre to the nearest line
theta ~ U(0, pi/2): angle between the needle and the lines

needle crosses a line: x <= (l/2) * sin(theta)
crossing probability: P = 2l / (pi * t) => pi ≈ 2 * l * N / (t * H)
"""

from dataclasses import dataclass

import numpy as np

MAX_SIMULATIONS = 5_000_000


@dataclass
class SimulationResult:
    needle_length: float
    line_spacing: float
    x: np.ndarray
    theta: np.ndarray
    hits: np.ndarray

    @property
    def n(self) -> int:
        return len(self.x)

    @property
    def hit_count(self) -> int:
        return int(self.hits.sum())

    @property
    def hit_ratio(self) -> float:
        return self.hit_count / self.n

    @property
    def theoretical_probability(self) -> float:
        return 2 * self.needle_length / (np.pi * self.line_spacing)

    @property
    def pi_estimate(self) -> float | None:
        """Estimate of pi, or None if no needle crossed a line."""
        if self.hit_count == 0:
            return None
        return 2 * self.needle_length * self.n / (self.line_spacing * self.hit_count)

    @property
    def pi_error(self) -> float:
        return abs(self.pi_estimate - np.pi)


def validate_parameters(n: int, needle_length: float, line_spacing: float) -> None:
    if n < 1:
        raise ValueError("Počet simulací musí být alespoň 1.")
    if n > MAX_SIMULATIONS:
        raise ValueError(f"Počet simulací může být nejvýše {MAX_SIMULATIONS}.")
    if not np.isfinite(needle_length) or not np.isfinite(line_spacing):
        raise ValueError("Délka jehly a čar musí být konečná čísla.")
    if needle_length <= 0:
        raise ValueError("Délka jehly musí být kladná.")
    if line_spacing <= 0:
        raise ValueError("Rozteč čar musí být kladná.")
    if needle_length > line_spacing:
        raise ValueError("Pro krátkou jehlu musí platit l <= t.")


def simulate(n: int, needle_length: float, line_spacing: float) -> SimulationResult:
    rng = np.random.default_rng()

    x = rng.uniform(0, line_spacing / 2, n)
    theta = rng.uniform(0, np.pi / 2, n)
    hits = x <= (needle_length / 2) * np.sin(theta)

    return SimulationResult(needle_length, line_spacing, x, theta, hits)


def add_throws(result: SimulationResult, n: int) -> SimulationResult:
    """Return a new result extended by n more throws with the same l and t."""
    new = simulate(n, result.needle_length, result.line_spacing)
    return SimulationResult(
        result.needle_length,
        result.line_spacing,
        np.concatenate([result.x, new.x]),
        np.concatenate([result.theta, new.theta]),
        np.concatenate([result.hits, new.hits]),
    )


def running_estimate(result: SimulationResult) -> np.ndarray:
    """Estimate of pi after each throw: 2 * l * N / (t * H)."""
    l, t = result.needle_length, result.line_spacing
    throws = np.arange(1, result.n + 1)  # N after each throw
    hits_so_far = np.cumsum(result.hits).astype(float)  # H after each throw
    hits_so_far[hits_so_far == 0] = np.nan  # no hit yet = no estimate, guard against division by zero
    return 2 * l * throws / (t * hits_so_far)
