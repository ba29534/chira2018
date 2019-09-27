##############################################################################
## This script reproduces Fig. 3a-d of Chira et al. (2019).                 ##
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

# define sample tags
fcloud = ['M3','M4','M8']
fjeans = ['04','08','32']
fdir   = ['x','y','z']

# define plot parameters
ncols    = 3
nrows    = 4
ms       = 10
lw       = 7
xlim     = [ 0.0,6.2]
ylimzeta = [-0.5,1.8]
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
fig,ax = plt.subplots(ncols=ncols,nrows=nrows,sharex=True,sharey=True,figsize=(21,18))

for i,j,p in itertools.product(range(nrows),range(ncols),range(1,4)):
    # draw indicators for Boldyrev and She & Leveque values in each subplot
    ax[i,j].plot(xlim,np.zeros(2)+zboldyrev(p),ls='--',lw=lw-4,color=color[p-1])
    ax[i,j].plot(xlim,np.zeros(2)+zshe(p),ls='-.',lw=lw-4,color=color[p-1])
    # set plot parameters
    ax[i,j].plot(np.array(xlim),np.zeros(len(xlim))+1.0
                     ,color='grey',ls='-.',lw=lw)
    ax[i,j].set_xlim(xlim)
    ax[i,j].set_ylim(ylimzeta)
    # draw suuper-nova and mass accretion data 
    if(j == 0):
        ax[i,j].set_ylabel('$Z$(p)')
        sn  = snM3
        mab = mabM3
        mae = maeM3
    elif(j == 1):
        sn  = snM4
        mab = mabM4
        mae = maeM4
    elif(j == 2):
        sn = snM8
        mab = mabM8
        mae = maeM8

    for k in range(len(sn)):            
        ax[i,j].plot(np.zeros(2)+sn[k]
                    ,np.array(ylimzeta),ls=':',color='black',lw=5)
    for k in range(len(mab)):
        ax[i,j].fill_between(np.array([mab[k],mae[k]])
                            ,np.zeros(2)+ylimzeta[0],np.zeros(2)+ylimzeta[1]
                            ,color='blue',alpha=0.1)


###############################################################################
print("(a) normal")
for icloud in range(len(fcloud)):
    cloud = fcloud[icloud]
    # read in data
    ifile = glob(('%szeta_fitted_%s_vsf3d*lambda04*weighted_ncloud100.dat' % (dsrc,cloud)))[0]
    time,zeta1,zeta2,zeta3 = np.array([]),np.array([]),np.array([]),np.array([])
    time,zeta1,zeta2,zeta3 = np.loadtxt(ifile,skiprows=2,usecols=(0,1,2,3),unpack=True)
    # plot data
    for p in range(1,4):
        if(p==1): zetap = zeta1
        if(p==2): zetap = zeta2
        if(p==3): zetap = zeta3
        zetap = zetap/zeta3
        ax[0,icloud].plot(time,zetap,ms=ms
                         ,lw=lw,color=color[p-1],marker='o',ls='-'
                         ,markeredgecolor='black',label=('p = %i' % p))

    ax[0,icloud].set_title(cloud)
    if(icloud == 0): 
        txtstr = "(a) standard 3D analysis\n3D velocities, $n_{cloud}$=100 cm$^{-3}$, $\lambda_{J}$=4$\Delta$x"
        ax[0,icloud].text(0.15,1.7,txtstr,alpha=1.0,backgroundcolor="white",verticalalignment='top')
    if(icloud == 2): 
        ax[0,icloud].legend(loc=0,fontsize=16)
        
        
###############################################################################
print("(b) 1D")
for icloud in range(len(fcloud)):
    cloud = fcloud[icloud]
 
    for idir in fdir:
        # read in data
        ifile = glob(('%szeta_fitted_%s_vsf1d_%s*lambda04*weighted_ncloud100.dat' % (dsrc,cloud,idir)))[0]
        time,zeta1,zeta2,zeta3 = np.array([]),np.array([]),np.array([]),np.array([])
        time,zeta1,zeta2,zeta3 = np.loadtxt(ifile,skiprows=2,usecols=(0,1,2,3),unpack=True)
        
        if(idir == fdir[0]): marker = 's'
        elif(idir == fdir[1]): marker = 'D'
        elif(idir == fdir[2]): marker = 'p'
        
        # plot data
        ax[1,icloud].plot(time[0]-5,ylimzeta[0]-5
                         ,ms=ms-2,lw=lw-4,color=color[p-1],marker=marker
                         ,ls='-.',markeredgecolor='black'
                         ,label=('los = %s axis' % (idir)))

        for p in range(1,4):
            if(p==1): zetap = zeta1
            if(p==2): zetap = zeta2
            if(p==3): zetap = zeta3
            zetap = zetap/zeta3
            ax[1,icloud].plot(time,zetap
                             ,ms=ms-2,lw=lw-4,color=color[p-1],marker=marker
                             ,ls='-.',markeredgecolor='black')
        
    if(icloud == 0): 
        txtstr = "(b) 1D analysis\n1D velocities, $n_{cloud}$=100 cm$^{-3}$, $\lambda_{J}$=4$\Delta$x"
        ax[1,icloud].text(0.15,1.7,txtstr,alpha=1.0,backgroundcolor="white",verticalalignment='top')
    if(icloud == 2): 
        ax[1,icloud].legend(loc=0,fontsize=16)

        
##############################################################################
print("(c) density threshold")

for icloud in range(len(fcloud)):
    cloud = fcloud[icloud]
    ifile = glob(('%szeta_fitted_%s_vsf3d*lambda04*weighted.dat' % (dsrc,cloud)))[0]
    time,zeta1,zeta2,zeta3 = np.array([]),np.array([]),np.array([]),np.array([])
    time,zeta1,zeta2,zeta3 = np.loadtxt(ifile,skiprows=2,usecols=(0,1,2,3),unpack=True)
    
    for p in range(1,4):
        if(p==1): zetap = zeta1
        if(p==2): zetap = zeta2
        if(p==3): zetap = zeta3
        zetap = zetap/zeta3
        ax[2,icloud].plot(time,zetap
                         ,ms=ms,lw=lw,color=color[p-1],marker='o',ls='-'
                         ,markeredgecolor='black',label=('p = %i' % p))
        
    if(icloud == 0): 
        txtstr = "(c) density threshold analysis\n3D velocities, $n_{cloud}$=0 cm$^{-3}$, $\lambda_{J}$=4$\Delta$x"
        ax[2,icloud].text(0.15,1.7,txtstr,alpha=1.0,backgroundcolor="white",verticalalignment='top')
    if(icloud == 2): 
        ax[2,icloud].legend(loc=0,fontsize=16)

        
##############################################################################
print("(d) density weighting")


for icloud in range(len(fcloud)):
    cloud = fcloud[icloud]
    ifile = glob(('%szeta_fitted_%s_vsf3d*lambda04*nonweighted_ncloud100.dat' % (dsrc,cloud)))[0]
    time,zeta1,zeta2,zeta3 = np.array([]),np.array([]),np.array([]),np.array([])
    time,zeta1,zeta2,zeta3 = np.loadtxt(ifile,skiprows=2,usecols=(0,1,2,3),unpack=True)
    
    for p in range(1,4):
        if(p==1): zetap = zeta1
        if(p==2): zetap = zeta2
        if(p==3): zetap = zeta3
        zetap = zetap/zeta3
        ax[3,icloud].plot(time,zetap
                         ,ms=ms,lw=lw,color=color[p-1],marker='o',ls='-'
                         ,markeredgecolor='black',label=('p = %i' % p))
        
    ax[3,icloud].set_xlabel('time [Myr]')
    if(icloud == 0): 
        txtstr = "(d) density weighting analysis\n3D velocities, $n_{cloud}$=100 cm$^{-3}$, $\lambda_{J}$=4$\Delta$x\nVSF calculated without density weighting"
        ax[3,icloud].text(0.15,1.7,txtstr,alpha=1.0,backgroundcolor="white",verticalalignment='top')
    if(icloud == 2): ax[3,icloud].legend(loc=0,fontsize=16)
        
##############################################################################

# adjust and save plot
fig.tight_layout(pad=0.9)
fig.subplots_adjust(wspace=0)
fig.subplots_adjust(hspace=0)
fig.savefig(dfig+'fig3a-d_z_all_part1.pdf')