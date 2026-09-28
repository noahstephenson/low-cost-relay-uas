"""Render the method and performed-analysis layers of the paper workflow."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


OUT = Path(__file__).resolve().parent / "figs"
fig, ax = plt.subplots(figsize=(3.35, 4.35))
fig.subplots_adjust(left=0.02, right=0.98, top=0.99, bottom=0.01)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

navy = "#16486b"
ink = "#172b39"
muted = "#5b6c78"
method_fill = "#f1f4f6"
study_fill = "#e8f2f8"
future_fill = "#fff8e9"


def panel(x, y, w, h, fill, edge=navy, dashed=False):
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.008,rounding_size=0.012",
            facecolor=fill,
            edgecolor=edge,
            linewidth=1.05,
            linestyle="--" if dashed else "-",
        )
    )


def arrow(start, end, dashed=False):
    ax.annotate(
        "", xy=end, xytext=start,
        arrowprops={
            "arrowstyle": "->", "color": navy, "linewidth": 1.1,
            "linestyle": "--" if dashed else "-",
            "shrinkA": 0, "shrinkB": 0,
        },
    )


# Gray: systems method used to frame the case study.
ax.text(0.5, 0.967, "METHOD FRAME", ha="center", va="center",
        fontsize=10.2, fontweight="bold", color=muted, fontfamily="DejaVu Sans")
panel(0.08, 0.681, 0.84, 0.243, method_fill, edge="#738794")
for y, number, label in (
    (0.868, "1", "Define outbound relay target"),
    (0.797, "2", "Allocate carrier and payload roles"),
    (0.726, "3", "Declare scenario and limits"),
):
    ax.text(0.15, y, number, ha="left", va="center", fontsize=9.8,
            fontweight="bold", color=navy, fontfamily="DejaVu Sans")
    ax.text(0.235, y, label, ha="left", va="center", fontsize=9.2,
            color=ink, fontfamily="DejaVu Sans")

arrow((0.5, 0.679), (0.5, 0.639))

# Blue: the calculations and comparison actually performed in the paper.
panel(0.08, 0.566, 0.84, 0.069, navy)
ax.text(0.5, 0.6, "ANALYSIS PERFORMED", ha="center", va="center",
        fontsize=9.7, fontweight="bold", color="white", fontfamily="DejaVu Sans")

panel(0.035, 0.351, 0.445, 0.171, study_fill)
panel(0.52, 0.351, 0.445, 0.171, study_fill)
for x, title, detail in (
    (0.2575, "LINK SCREEN", "obstruction + margin"),
    (0.7425, "CARRIER SCREEN", "hover power + mass"),
):
    ax.text(x, 0.456, title, ha="center", va="center", fontsize=9.4,
            fontweight="bold", color=navy, fontfamily="DejaVu Sans")
    ax.text(x, 0.406, detail, ha="center", va="center", fontsize=8.5,
            color=ink, fontfamily="DejaVu Sans")

arrow((0.2575, 0.348), (0.39, 0.3))
arrow((0.7425, 0.348), (0.61, 0.3))
panel(0.13, 0.208, 0.74, 0.091, study_fill)
ax.text(0.5, 0.267, "Choose placement + dwell", ha="center", va="center",
        fontsize=9.6, fontweight="bold", color=navy, fontfamily="DejaVu Sans")
ax.text(0.5, 0.229, "independent case check", ha="center", va="center",
        fontsize=8.6, color=ink, fontfamily="DejaVu Sans")

# Dashed amber: evidence explicitly outside this study.
arrow((0.5, 0.205), (0.5, 0.155), dashed=True)
panel(0.13, 0.04, 0.74, 0.111, future_fill, edge="#9b6c20", dashed=True)
ax.text(0.5, 0.113, "STILL TO TEST", ha="center", va="center",
        fontsize=9.1, fontweight="bold", color="#745019", fontfamily="DejaVu Sans")
ax.text(0.5, 0.072, "installed + operational tests", ha="center", va="center",
        fontsize=9.0, color=ink, fontfamily="DejaVu Sans")

for extension in ("pdf", "png"):
    fig.savefig(OUT / f"architecture_assessment_workflow.{extension}",
                dpi=300, bbox_inches="tight", pad_inches=0.02)
plt.close(fig)
