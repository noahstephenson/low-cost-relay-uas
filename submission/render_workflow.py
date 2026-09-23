"""Render the paper workflow from the labels and connections in figs/architecture_assessment_workflow.mmd."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent / "figs"
fig, ax = plt.subplots(figsize=(3.35, 4.35))
fig.subplots_adjust(left=.02, right=.98, top=.99, bottom=.01)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
edge = "#235476"
fill = "#f2f6f8"

def box(x, y, w, h, label, shade=fill, size=8.5):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.008",
                 edgecolor=edge,facecolor=shade,linewidth=.9))
    ax.text(x+w/2,y+h/2,label,ha="center",va="center",fontsize=size,
            fontfamily="DejaVu Serif",linespacing=1.2)
def arrow(a,b,dashed=False):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="->",color=edge,
                linewidth=1,linestyle="--" if dashed else "-",
                shrinkA=0,shrinkB=0))
box(.15,.91,.70,.07,"Operational need\noutbound relay dwell")
box(.15,.81,.70,.07,"System boundary\ncarrier and payload")
box(.15,.71,.70,.07,"Four flows\ntraffic, command, power, support")
box(.15,.61,.70,.07,"Declared inputs\ngeometry, radio, payload, carrier")
box(.03,.46,.44,.10,"Link check\nvisibility and level")
box(.53,.46,.44,.10,"Carrier check\nenergy and mass")
box(.15,.34,.70,.07,"Independent model checks")
box(.15,.24,.70,.07,"Decision\nlink, size, closure, or pass")
box(.15,.08,.70,.10,"Pending: installed-payload tests\nand operational validation",
    shade="#fffaf0",size=8)
for a,b in [((.5,.91),(.5,.88)),((.5,.81),(.5,.78)),
            ((.5,.71),(.5,.68)),((.5,.61),(.25,.56)),
            ((.5,.61),(.75,.56)),((.25,.46),(.38,.41)),
            ((.75,.46),(.62,.41)),((.5,.34),(.5,.31))]:
    arrow(a,b)
arrow((.5,.24),(.5,.18),True)
for ext in ("pdf","png"):
    fig.savefig(OUT/("architecture_assessment_workflow."+ext),dpi=300,
                bbox_inches="tight",pad_inches=.02)
plt.close(fig)
