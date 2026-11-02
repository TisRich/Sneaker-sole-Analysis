# Rebuilds the README charts. Run from the repo root: python docs/tools/make_charts.py
# SolidWorks values were read from the legend maxima in results/solidworks/*.jpg
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from matplotlib.ticker import FuncFormatter
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"svg.fonttype":"path"})
SURF="#fcfcfb"; T1="#0b0b0b"; T2="#52514e"; GRID="#e4e3df"
C_M="#2a78d6"; C_S="#eb6834"
cases=["Flat sole\nheel strike","Flat sole\nmidfoot","Curved sole\nheel strike","Curved sole\nmidfoot"]
m_s=[1.2149,0.2947,1.2172,0.2531]; s_s=[0.4097,0.050489,0.02673,0.02673]
m_d=[0.8603,0.1774,0.8759,0.1451]; s_d=[0.3682,0.02659,0.01281,0.01325]
out="docs/charts/"
def style(ax):
    ax.set_facecolor(SURF)
    for s in ["top","right","left"]: ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=T2,length=0); ax.yaxis.grid(True,color=GRID,lw=0.8); ax.set_axisbelow(True)
def grouped(m,s,unit,title,fname,fmt):
    fig,ax=plt.subplots(figsize=(9,4.8),facecolor=SURF); style(ax)
    x=np.arange(4); w=0.36
    b1=ax.bar(x-w/2-0.01,m,w,color=C_M,label="MATLAB (PDE Toolbox)")
    b2=ax.bar(x+w/2+0.01,s,w,color=C_S,label="SolidWorks Simulation")
    ax.set_yscale("log")
    for bars,vals in ((b1,m),(b2,s)):
        for b,v in zip(bars,vals):
            ax.text(b.get_x()+b.get_width()/2,v*1.12,fmt(v),ha="center",va="bottom",fontsize=9.5,color=T1)
    ax.set_xticks(x); ax.set_xticklabels(cases,color=T1)
    ax.set_ylabel(f"{unit} (log scale)",color=T2)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_: f"{v:g}"))
    ax.set_ylim(min(s)*0.5,max(m)*3)
    ax.set_title(title,loc="left",color=T1,fontsize=14,fontweight="bold",pad=28)
    ax.legend(loc="upper left",bbox_to_anchor=(0,1.09),ncol=2,frameon=False,fontsize=10,labelcolor=T1,handlelength=1.2)
    fig.tight_layout(); fig.savefig(out+fname,facecolor=SURF); plt.close(fig)
grouped(m_s,s_s,"Peak von Mises stress (MPa)","Peak von Mises stress","stress_comparison.svg",lambda v:f"{v:.3f}")
grouped(m_d,s_d,"Peak displacement (mm)","Peak displacement","displacement_comparison.svg",lambda v:f"{v:.3f}" if v>=0.1 else f"{v:.4f}")
# ratio chart
rs=[a/b for a,b in zip(m_s,s_s)]; rd=[a/b for a,b in zip(m_d,s_d)]
fig,ax=plt.subplots(figsize=(9,4.2),facecolor=SURF); style(ax)
ax.yaxis.grid(False); ax.xaxis.grid(True,color=GRID,lw=0.8)
y=np.arange(4)[::-1]; h=0.36
lab=[c.replace("\n"," ") for c in cases]
b1=ax.barh(y+h/2+0.01,rs,h,color=C_M,label="Stress ratio")
b2=ax.barh(y-h/2-0.01,rd,h,color="#1baf7a",label="Displacement ratio")
ax.set_xscale("log"); ax.axvline(1,color=T2,lw=1,ls="--")
ax.text(1.05,3.62,"1× = tools agree",color=T2,fontsize=9,va="bottom")
for bars,vals in ((b1,rs),(b2,rd)):
    for b,v in zip(bars,vals): ax.text(v*1.08,b.get_y()+b.get_height()/2,f"{v:.1f}×",va="center",fontsize=9.5,color=T1)
ax.set_yticks(y); ax.set_yticklabels(lab,color=T1)
ax.xaxis.set_major_formatter(FuncFormatter(lambda v,_: f"{v:g}×"))
ax.set_xlim(0.8,200); ax.set_ylim(-0.7,3.9)
ax.set_title("How much larger the MATLAB result is than SolidWorks",loc="left",color=T1,fontsize=14,fontweight="bold",pad=28)
ax.legend(loc="upper left",bbox_to_anchor=(0,1.09),ncol=2,frameon=False,fontsize=10,labelcolor=T1,handlelength=1.2)
ax.spines["bottom"].set_visible(False)
fig.tight_layout(); fig.savefig(out+"matlab_vs_solidworks_ratio.svg",facecolor=SURF); plt.close(fig)
# loading chart (MATLAB)
area=[35.75,167.68,31.88,205.75]; trac=[0.5443,0.1161,0.6104,0.0946]
fig,axs=plt.subplots(1,2,figsize=(9,3.8),facecolor=SURF)
for ax,vals,t,f in ((axs[0],area,"Loaded area (cm²)",lambda v:f"{v:.0f}"),(axs[1],trac,"Applied pressure (MPa)",lambda v:f"{v:.3f}")):
    style(ax); ax.yaxis.grid(False); ax.xaxis.grid(True,color=GRID,lw=0.8); ax.spines["bottom"].set_visible(False)
    bb=ax.barh(y,vals,0.55,color=C_M)
    for b,v in zip(bb,vals): ax.text(v+max(vals)*0.02,b.get_y()+b.get_height()/2,f(v),va="center",fontsize=9.5,color=T1)
    ax.set_yticks(y); ax.set_yticklabels(lab if ax is axs[0] else [],color=T1)
    ax.set_xlim(0,max(vals)*1.22); ax.set_title(t,loc="left",color=T1,fontsize=12,fontweight="bold")
fig.suptitle("MATLAB load setup: same 1946 N force, very different contact areas",x=0.02,ha="left",color=T1,fontsize=14,fontweight="bold")
fig.tight_layout(); fig.savefig(out+"loading_setup.svg",facecolor=SURF); plt.close(fig)
