##############################################################################
## This script reproduces Fig. 2e of Chira et al. (2019).                   ##
##############################################################################

# import required python packages 
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import itertools

# define function that return predicted values of zeta
# Boldyrev (2002)
def zboldyrev(p):
    return (p/9.+1.-(1./3.)**(p/3.))
# She & Leveque (1992)
def zshe(p):
    return (p/9.+2.-2.*(2./3.)**(p/3.))


# define source folder
dsrc = '../../src_data/vsf/zeta_fitted/'

# define target folder
dfig = '../../vsf_output/'

fcloud = ['M3','M4','M8']
fjeans = ['_lambda04','_lambda08','_lambda32']
ljeans = [4,8,32]
fdir   = ['x','y','z']

# define plot parameters
ncols    = 3
nrows    = 1
ms       = 10
lw       = 7
xlim     = [ 0.0,6.2]
ylimzeta = [-1.5,5.0]
color    = ['red','green','blue']
plt.rcParams['font.size'] = 22

# set dates of super-novae (sn) and begin and end of massive mass accretion 
# (mab and mae, respectively)
snM3 = np.array([ 0.7,1.2,1.8,2.6,3.8,4.3 ])
snM4 = np.array([ 0.4,2.1,3.8,5.3 ])
snM8 = np.array([ 0.6 ])

mabM3 = np.array([ 1.2,2.8 ])
maeM3 = np.array([ 2.4,3.9 ])
mabM4 = np.array([ 1.5 ])
maeM4 = np.array([ 2.8 ])
mabM8 = np.array([ 1.0,2.5 ])
maeM8 = np.array([ 2.0,3.2 ])


# draw plot
fig,ax = plt.subplots(ncols=ncols,nrows=nrows,sharex=True,sharey=True,figsize=(21,4.3))

for j,p in itertools.product(range(ncols),range(1,4)):
    # draw indicators for Boldyrev and She & Leveque values in each subplot
    ax[j].plot(xlim,np.zeros(2)+zboldyrev(p),ls='--',lw=lw-4,color=color[p-1])
    ax[j].plot(xlim,np.zeros(2)+zshe(p),ls='-.',lw=lw-4,color=color[p-1])
    # set plot parameters
    ax[j].plot(np.array(xlim),np.zeros(len(xlim))+1.0
                     ,color='grey',ls='-.',lw=lw)
    ax[j].set_xlim(xlim)
    ax[j].set_ylim(ylimzeta)
    # draw suuper-nova and mass accretion data 
    if(j == 0):
        ax[j].set_ylabel('$\zeta$(p)')
    sn  = snM3
    mab = mabM3
    mae = maeM3
        
    for k in range(len(sn)):            
        ax[j].plot(np.zeros(2)+sn[k]
                    ,np.array(ylimzeta),ls=':',color='black',lw=5)
    for k in range(len(mab)):
        ax[j].fill_between(np.array([mab[k],mae[k]])
                            ,np.zeros(2)+ylimzeta[0],np.zeros(2)+ylimzeta[1]
                            ,color='blue',alpha=0.1)


###############################################################################

print('(e) Jeans')

for ijeans in range(len(fjeans)):
    # read in data
    ifile = glob('%szeta_fitted_M3_vsf3d%s_weighted_ncloud100*dat' % (dsrc,fjeans[ijeans]))[0]
    time,zeta1,zeta2,zeta3 = np.array([]),np.array([]),np.array([]),np.array([])
    time,zeta1,zeta2,zeta3 = np.loadtxt(ifile,skiprows=2,usecols=(0,1,2,3),unpack=True)
    # plot data
    for p in range(1,4):
        if(p==1): zetap = zeta1
        if(p==2): zetap = zeta2
        if(p==3): zetap = zeta3
        ax[ijeans].plot(time,zetap
                       ,ms=ms,lw=lw,color=color[p-1],marker='o',ls='-'
                       ,markeredgecolor='black',label=('p = %i' % p))

    ax[ijeans].set_title('$\lambda_J$ = %i$\Delta$x' % (ljeans[ijeans] ))
    ax[ijeans].set_xlabel('time [Myr]')
    if(ijeans == 0): 
        txtstr = "(e) Jeans refinement analysis\n3D velocities, $n_{cloud}$=100 cm$^{-3}$, only M3!"
        ax[ijeans].text(0.15,4.65,txtstr,alpha=1.0,backgroundcolor="white",verticalalignment='top')
    if(ijeans == 2): 
        ax[ijeans].legend(loc=0,fontsize=16)

# adjust and save figure
fig.tight_layout(pad=0.8)
fig.subplots_adjust(wspace=0)
fig.subplots_adjust(hspace=0)
fig.savefig(dfig+'fig2e_zeta_all_part2.pdf')
