"""Plots of the simulation as SVG text for embedding in HTML."""

import io

import numpy as np
from matplotlib.figure import Figure

from buffon import SimulationResult, running_estimate

STRIPS = 6  # number of strips between lines in the picture
MAX_DRAWN_NEEDLES = 500
MAX_PLOT_POINTS = 2000

HIT_COLOR = "tab:red"
MISS_COLOR = "tab:blue"

def _to_svg(fig: Figure) -> str:
    buffer = io.StringIO()
    fig.savefig(buffer, format="svg", bbox_inches="tight")
    return buffer.getvalue()


def needles_image(result: SimulationResult) -> str:
    """Draw the first MAX_DRAWN_NEEDLES needles on lined paper.

    The needle centre is x away from its nearest line, needle drawn as a hit in red crosses a line.
    """
    t, l = result.line_spacing, result.needle_length
    count = min(result.n, MAX_DRAWN_NEEDLES)

    fig = Figure(figsize=(8, 8))
    ax = fig.add_subplot()
    for k in range(STRIPS + 1):
        ax.axhline(k * t, color="black", linewidth=1)

    rng = np.random.default_rng(0)  # fixed seed, so needle i is always drawn at the same place
    for i in range(count):
        strip = rng.integers(0, STRIPS)  # strip between lines strip * t and (strip + 1) * t
        if rng.random() < 0.5:
            center_y = strip * t + result.x[i]  # nearest line is below
        else:
            center_y = (strip + 1) * t - result.x[i]  # nearest line is above
        center_x = rng.uniform(0, STRIPS * t)
        angle = result.theta[i] if rng.random() < 0.5 else np.pi - result.theta[i]

        dx = l / 2 * np.cos(angle)
        dy = l / 2 * np.sin(angle)
        color = HIT_COLOR if result.hits[i] else MISS_COLOR
        ax.plot([center_x - dx, center_x + dx], [center_y - dy, center_y + dy], color=color, linewidth=1.5)
        ax.plot(center_x, center_y, "o", color=color, markersize=3, markeredgecolor="black", markeredgewidth=0.5)

    ax.set_xlim(-l / 2, STRIPS * t + l / 2)
    ax.set_ylim(-l / 2, STRIPS * t + l / 2)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Prvních {count} jehel (červené protínají čáru)")
    return _to_svg(fig)


def convergence_image(result: SimulationResult) -> str:
    """Running estimate of pi against the number of throws."""
    estimate = running_estimate(result)
    throws = np.arange(1, result.n + 1)
    every = max(1, result.n // MAX_PLOT_POINTS)  # plot only every k-th throw

    fig = Figure(figsize=(6, 3.8))
    ax = fig.add_subplot()
    ax.plot(throws[::every], estimate[::every], color=MISS_COLOR, label=r"odhad $\pi$")
    ax.axhline(np.pi, color=HIT_COLOR, linestyle="--", label=r"$\pi$")
    ax.set_xscale("log")
    ax.set_xlim(1, max(result.n, 10))  # estimate can be all NaN at the start
    ax.set_xlabel(r"počet hodů $N$")
    ax.set_ylabel(r"odhad $\pi$")
    ax.set_title("Konvergence odhadu")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return _to_svg(fig)


def phase_space_image(result: SimulationResult) -> str:
    """Points (theta, x) with the curve x = (l/2) sin(theta) separating hits."""
    count = min(result.n, MAX_PLOT_POINTS)
    theta, x, hits = result.theta[:count], result.x[:count], result.hits[:count]

    fig = Figure(figsize=(6, 3.8))
    ax = fig.add_subplot()
    ax.scatter(theta[hits], x[hits], s=4, color=HIT_COLOR, label="zásah")
    ax.scatter(theta[~hits], x[~hits], s=4, color=MISS_COLOR, label="bez zásahu")
    grid = np.linspace(0, np.pi / 2, 200)
    ax.plot(grid, result.needle_length / 2 * np.sin(grid), color="black", label=r"$x = \frac{l}{2} \sin\theta$")
    ax.set_xlim(0, np.pi / 2)
    ax.set_ylim(0, result.line_spacing / 2)
    ax.set_xlabel(r"$\theta$")
    ax.set_ylabel(r"$x$")
    ax.set_title(rf"Prostor $(\theta, x)$, prvních {count} hodů")
    ax.legend(loc="upper left", framealpha=1)
    return _to_svg(fig)
