##############################################################################
## This script reproduces Fig. 4 of Chira et al. (2019).                    ##
##############################################################################

# import required python packages 
import numpy as np
import matplotlib.pyplot as plt
from glob import glob


# define source folder
dsrc = '../../src_data/vsf/zeta_fitted/'

# define target folder
dfig = '../../vsf_output/'

# define scenarios
cloud  = 'M3'
fjeans = ['_lambda04','_lambda08','_lambda32']
ljeans = [4,8,32]

# define plot parameters
ncols    = 2
nrows    = 2
ms       = 10
lw       = 7
color    = ['red','green','blue']
ylimzeta = [-0.5,3.5]
ylimz    = [ 0.0,1.2]
plt.rcParams['font.size'] = 22

# read in data
ifile = glob(('%szeta_fitted_%s_vsf3d%s_weighted_ncloud100.dat' % (dsrc,cloud,fjeans[0])) )[0]
t04,zeta104,zeta204,zeta304 = np.array([]),np.array([]),np.array([]),np.array([])
t04,zeta104,zeta204,zeta304 = np.loadtxt(ifile,skiprows=2,usecols=(0,1,2,3),unpack=True)


fig,ax = plt.subplots(ncols=ncols,nrows=nrows,figsize=(21,10))
for ijeans in range(len(fjeans)-1):
    # read in data
    ifile = glob(('%szeta_fitted_%s_vsf3d%s_weighted_ncloud100.dat' % (dsrc,cloud,fjeans[ijeans+1])) )[0]
    t,zeta1,zeta2,zeta3 = np.array([]),np.array([]),np.array([]),np.array([])
    t,zeta1,zeta2,zeta3 = np.loadtxt(ifile,skiprows=2,usecols=(0,1,2,3),unpack=True)
    
    # plot data
    ax[ijeans,0].plot(ylimzeta,ylimzeta,ls='-.',lw=lw,color='grey')
    ax[ijeans,1].plot(ylimz,ylimz,ls='-.',lw=lw,color='grey')
    
    span = len(t)
    for p in range(1,4):
        if(p==1): 
            zetax = zeta104[0:span]
            zetay = zeta1
        if(p==2): 
            zetax = zeta204[0:span]
            zetay = zeta2
        if(p==3): 
            zetax = zeta304[0:span]
            zetay = zeta3
            
        ax[ijeans,0].plot(zetax,zetay
                         ,marker='o',ls='',markeredgecolor='black',ms=ms
                         ,lw=lw,color=color[p-1])
        ax[ijeans,1].plot(zetax/zeta304[0:span],zetay/zeta3
                         ,marker='o',ls='',markeredgecolor='black',ms=ms
                         ,lw=lw,color=color[p-1],label=("p = %i" % p))
        
    ax[ijeans,0].set_xlim(ylimzeta)
    ax[ijeans,0].set_ylim(ylimzeta)
    ax[ijeans,1].set_xlim(ylimz)
    ax[ijeans,1].set_ylim(ylimz)
    ax[ijeans,0].set_xlabel('$\zeta$(p), $\lambda_J$ = 4$\Delta$x')
    ax[ijeans,1].set_xlabel('$Z$(p), $\lambda_J$ = 4$\Delta$x')
    ax[ijeans,0].set_ylabel(('$\zeta$(p), $\lambda_J$ = %i$\Delta$x' % (ljeans[ijeans+1])))
    ax[ijeans,1].set_ylabel(('$Z$(p), $\lambda_J$ = %i$\Delta$x' % (ljeans[ijeans+1])))
    
# plot legend
ax[1,1].legend(loc=4)

# adjust and save figure
fig.tight_layout(pad=0.2)
fig.savefig(dfig+'fig4_comp_jeans.pdf')