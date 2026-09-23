"""Narrow Word rendering of the two panels in fig1_architecture_geometry."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

out=Path(__file__).resolve().parent/'figs'/'fig1_architecture_geometry_word.png'
fig=plt.figure(figsize=(3.35,4.5))
fig.subplots_adjust(left=.01,right=.99,top=.99,bottom=.03)
ax=fig.add_axes([.02,.49,.96,.48]);ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
blue='#235476'
def box(x,y,w,h,label,shade='white'):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.01',edgecolor=blue,facecolor=shade,lw=.9))
 ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=8,fontfamily='DejaVu Serif')
def arrow(a,b):
 ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':blue,'lw':1})
ax.text(0,1,'(a) Aircraft responsibilities',va='top',fontfamily='DejaVu Serif',fontsize=9,weight='bold')
box(.20,.69,.60,.16,'Carrier aircraft\nstructure | power | avionics','#eef3f6')
box(.27,.30,.46,.16,'Relay payload\n0.20 kg | 14 W')
box(.02,.03,.30,.13,'Ground G')
box(.68,.03,.30,.13,'Remote U')
arrow((.36,.69),(.36,.46));arrow((.64,.69),(.64,.46))
ax.text(.14,.57,'mount',fontsize=7);ax.text(.68,.57,'power',fontsize=7)
arrow((.32,.10),(.36,.30));arrow((.64,.30),(.68,.10))
ax.text(.02,.86,'Command',fontsize=7);arrow((.18,.80),(.20,.80))
ax=fig.add_axes([.17,.10,.77,.34]);ax.set(xlim=(0,10.5),ylim=(0,160),xlabel='Horizontal position (km)',ylabel='Height (m)')
ax.plot([0,10],[0,100],'--',color='#963e3e',lw=1)
ax.plot([0,5,10],[0,120,100],color=blue,lw=1.5)
ax.plot([4,4],[0,80],color='black',lw=3)
ax.scatter([0,5,10],[0,120,100],color=blue,s=10)
ax.text(4.15,50,'80 m screen',fontsize=7)
ax.text(5.25,126,'R (120 m)',fontsize=7)
ax.text(.1,9,'G',fontsize=7);ax.text(9.8,105,'U',fontsize=7)
ax.tick_params(labelsize=7)
ax.xaxis.label.set_size(8);ax.yaxis.label.set_size(8)
fig.text(.02,.46,'(b) Worked geometry at 10 km separation',fontsize=9,fontfamily='DejaVu Serif',weight='bold')
fig.savefig(out,dpi=300,bbox_inches='tight',pad_inches=.02)
plt.close(fig)
