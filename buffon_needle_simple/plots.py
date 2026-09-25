"""Plots of the simulation as SVG text for embedding in HTML."""

import io

import matplotlib
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.figure import Figure

from buffon import SimulationResult, running_estimate

STRIPS = 6  # number of strips between lines in the picture
MAX_DRAWN_NEEDLES = 500
MAX_PLOT_POINTS = 2000

HIT_COLOR = "#d62728"
MISS_COLOR = "#1f77b4"

# Serif and Latex font for formulas
matplotlib.rcParams["font.family"] = "STIXGeneral"
matplotlib.rcParams["mathtext.fontset"] = "stix"
matplotlib.rcParams["font.size"] = 12


def _to_svg(fig: Figure) -> str:
    buffer = io.StringIO()
    fig.savefig(buffer, format="svg", bbox_inches="tight")
    return buffer.getvalue()


def needles_image(result: SimulationResult) -> str:
    """Draw the first MAX_DRAWN_NEEDLES needles on lined paper.

    Each needle is placed using its simulated x and theta, random strip is picked
    based the nearest line being below or above the centre and the angle.
    """
    t, l = result.line_spacing, result.needle_length
    count = min(result.n, MAX_DRAWN_NEEDLES)
    x, theta, hits = result.x[:count], result.theta[:count], result.hits[:count]

    # Fixed seed so needle i stays in the same place on every redraw
    layout = np.random.default_rng(0)
    strip = layout.integers(0, STRIPS, MAX_DRAWN_NEEDLES)[:count]
    line_below = layout.random(MAX_DRAWN_NEEDLES)[:count] < 0.5
    center_x = layout.uniform(0, STRIPS * t, MAX_DRAWN_NEEDLES)[:count]
    mirrored = layout.random(MAX_DRAWN_NEEDLES)[:count] < 0.5

    center_y = np.where(line_below, strip * t + x, (strip + 1) * t - x)
    angle = np.where(mirrored, np.pi - theta, theta)
    dx = l / 2 * np.cos(angle)
    dy = l / 2 * np.sin(angle)
    segments = np.stack([
        np.column_stack([center_x - dx, center_y - dy]),
        np.column_stack([center_x + dx, center_y + dy]),
    ], axis=1)

    fig = Figure(figsize=(8, 8))
    ax = fig.add_subplot()
    for k in range(STRIPS + 1):
        ax.axhline(k * t, color="black", linewidth=1)
    colors = np.where(hits, HIT_COLOR, MISS_COLOR)
    ax.add_collection(LineCollection(segments, colors=colors, linewidths=1.5))
    ax.scatter(center_x, center_y, s=10, c=colors, edgecolors="black", linewidths=0.5, zorder=3)

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
    indices = np.unique(np.geomspace(1, result.n, MAX_PLOT_POINTS).astype(int)) - 1

    fig = Figure(figsize=(6, 3.8))
    ax = fig.add_subplot()
    ax.plot(indices + 1, estimate[indices], color=MISS_COLOR, label=r"odhad $\pi$")
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
    ax.plot(grid, result.needle_length / 2 * np.sin(grid), color="black", label=r"$x = \frac{l}{2}\,\sin\theta$")
    ax.set_xlim(0, np.pi / 2)
    ax.set_ylim(0, result.line_spacing / 2)
    ax.set_xlabel(r"$\theta$")
    ax.set_ylabel(r"$x$")
    ax.set_title(rf"Prostor $(\theta, x)$, prvních {count} hodů")
    ax.legend(loc="upper left", framealpha=1)
    return _to_svg(fig)
