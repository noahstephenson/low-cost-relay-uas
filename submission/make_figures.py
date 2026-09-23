"""Publication figures from the retained computational baseline."""
from pathlib import Path
import sys, csv, json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'tmp/paper-review/packages'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from analysis.feasibility import load_inputs, parameters_for_case, solve_point
OUT=ROOT/'submission/figs'; OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'serif','font.serif':['Times New Roman'],'font.size':10,
 'axes.labelsize':10,'xtick.labelsize':10,'ytick.labelsize':10,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
blue='#235476'; green='#25715e'; orange='#ad6621'; red='#963e3e'
def save(fig,name):
    fig.savefig(OUT/(name+'.pdf'),bbox_inches='tight',pad_inches=.03)
    fig.savefig(OUT/(name+'.png'),dpi=300,bbox_inches='tight',pad_inches=.03)
    plt.close(fig)
def box(ax,x,y,w,h,text,color='white'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.012',facecolor=color,edgecolor=blue,lw=1))
    ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=10)
def arrow(ax,a,b):
    ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','lw':1.2,'color':blue})

fig=plt.figure(figsize=(7,4.8)); ax=fig.add_axes([.01,.48,.98,.49]); ax.set(xlim=(-.02,1.02),ylim=(0,1)); ax.axis('off')
ax.text(0,.98,'(a) Aircraft responsibilities',va='top',weight='bold')
box(ax,.25,.58,.49,.24,'Carrier aircraft\nStructure  |  power  |  avionics','#eef3f6')
box(ax,.32,.08,.35,.20,'Relay payload\n0.20 kg  |  14 W')
box(ax,.005,.08,.20,.20,'Ground\nendpoint G');box(ax,.79,.08,.20,.20,'Remote\naircraft U')
arrow(ax,(.205,.18),(.32,.18));arrow(ax,(.67,.18),(.79,.18))
arrow(ax,(.40,.58),(.40,.28));arrow(ax,(.60,.58),(.60,.28))
ax.text(.385,.43,'Retention',ha='right');ax.text(.615,.43,'Regulated power',ha='left')
ax.text(.01,.70,'Carrier\ncommand',ha='left',va='center');arrow(ax,(.17,.70),(.25,.70))
ax=fig.add_axes([.10,.09,.84,.30]);ax.set(xlim=(-.3,10.4),ylim=(0,160),xlabel='Horizontal position (km)',ylabel='Height (m)')
ax.plot([0,10],[0,100],'--',c=red);ax.plot([0,5,10],[0,120,100],c=blue,lw=1.6)
ax.plot([4,4],[0,80],c='black',lw=4);ax.scatter([0,5,10],[0,120,100],c=blue)
ax.text(4.1,56,'80 m screen',fontsize=10);ax.annotate('R (120 m)',(5,120),xytext=(6,142),arrowprops={'arrowstyle':'-'})
ax.text(.1,17,'G');ax.text(9.8,113,'U');ax.text(.02,1.12,'(b) Worked geometry at 10 km separation',transform=ax.transAxes,weight='bold')
save(fig,'fig1_architecture_geometry')

rows=list(csv.DictReader((ROOT/'analysis/calibration/calibration-results.csv').open()))
fig,axes=plt.subplots(1,2,figsize=(7,2.8));fig.subplots_adjust(wspace=.38,bottom=.22,top=.86)
for ax,role,title,unit in zip(axes,['fit','check'],['(a) Five-point hover fit','(b) Three-aircraft comparison'],['power (W)','hover time (min)']):
    subset=[r for r in rows if r['split']==role];x=[float(r['published_value']) for r in subset];y=[float(r['model_value']) for r in subset]
    lo=0 if role=='fit' else 30;hi=900 if role=='fit' else 45
    ax.plot([lo,hi],[lo,hi],c='#777777',lw=.8);ax.scatter(x,y,c=blue,s=30)
    ax.set(xlim=(lo,hi),ylim=(lo,hi),xlabel='Published '+unit,ylabel='Calculated '+unit,title=title)
    ax.grid(alpha=.15)
save(fig,'fig2_calibration')

rows=list(csv.DictReader((ROOT/'analysis/results/integrated-tradespace.csv').open()))
print('CSV fields',list(rows[0]))
primary=[r for r in rows if r['payload_id']=='PAY-MESH-OEM' and r['scenario']=='obstructed_reference']
states={'RELAY_BENEFICIAL_AND_FEASIBLE':('Pass','#dceee5'),'MASS_CLOSED_PRACTICAL_CONSTRAINT_FAILURE':('Size','#f3e2cc'),'RELAY_FUNCTIONAL_VEHICLE_RESOURCE_FAILURE':('NC','#ebd7d7'),'RELAY_CONNECTIVITY_INFEASIBLE':('Link','#eeeeee')}
fig,axes=plt.subplots(1,3,figsize=(7,3.1));fig.subplots_adjust(wspace=.12,bottom=.20,top=.82,left=.08,right=.99)
for ax,h in zip(axes,[60,120,240]):
    for row in primary:
        if float(row['relay_altitude_m'])!=h:continue
        x=[5,10,20,30,40,60].index(int(float(row['separation_km'])));y=[10,20,30,45,60].index(int(float(row['dwell_min'])))
        state=row.get('classification',row.get('state',row.get('mission_class')))
        if state is None:
            state=next(v for v in row.values() if v in states)
        label,color=states[state]
        ax.add_patch(Rectangle((x,y),1,1,facecolor=color,edgecolor='white',linewidth=1))
        ax.text(x+.5,y+.5,label,ha='center',va='center',rotation=90 if label=='No close' else 0,fontsize=10)
    ax.set(xlim=(0,6),ylim=(5,0),xticks=[i+.5 for i in range(6)],xticklabels=[5,10,20,30,40,60],yticks=[i+.5 for i in range(5)],yticklabels=[10,20,30,45,60],title=f'Relay height {h} m',xlabel='Separation (km)')
    if h==60:ax.set_ylabel('Dwell (min)')
    else:ax.set_yticklabels([])
    ax.tick_params(length=0)
save(fig,'fig3_service_map')

fig,ax=plt.subplots(figsize=(3.35,2.8));fig.subplots_adjust(left=.38,bottom=.2,top=.95,right=.95)
labels=['80 m at 0.40D','60 m at 0.40D','100 m at 0.40D','80 m at 0.30D','80 m at 0.45D'];vals=[100,75,125,133.333,88.889]
ax.scatter(vals,range(5),color=blue,zorder=3);ax.axvline(120,c=orange,ls='--',lw=1)
ax.set(yticks=range(5),yticklabels=labels,xlim=(55,145),xlabel='Threshold height (m)',ylim=(4.5,-.5));ax.grid(axis='x',alpha=.2)
save(fig,'fig4_thresholds')

inp=load_inputs();p=parameters_for_case(inp,'reference');ts=[i/4 for i in range(210)];ms=[]
for t in ts:
    r=solve_point(inp,p,{'payload_mass_kg':.2,'payload_power_w':14,'endurance_min':t});ms.append(r['gross_mass_kg'])
fig,ax=plt.subplots(figsize=(3.35,2.75));fig.subplots_adjust(left=.18,bottom=.20,top=.95,right=.96)
ax.plot(ts,ms,c=blue,lw=1.5);ax.axhline(10.8119,c=orange,ls='--',lw=1);ax.axvline(52.4426,c=red,ls=':',lw=1)
ax.scatter([30,45],[4.7747,15.1456],c=blue,s=20)
ax.text(2,11.6,'Rotor-size limit',fontsize=10);ax.text(50,23,'52.4 min',ha='right',fontsize=10)
ax.set(xlim=(0,60),ylim=(0,25),xlabel='Dwell (min)',ylabel='Closed gross mass (kg)');ax.grid(alpha=.15)
save(fig,'fig5_closure')
print('Wrote five figures')

