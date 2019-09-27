##############################################################################
## This script reproduces Fig. 5 of Chira et al. (2019).                    ##
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
fjeans = ['_lambda04','_lambda08','_lambda32']
ljeans = [4,8,32]
# define plot parameters
color   = ['red','green','blue']
limzeta = [-0.75,3.5]
limz    = [-0.75,1.75]
ms      = 10
lw      = 7
plt.rcParams['font.size'] = 20
ncols,nrows = 3,2


fig,ax = plt.subplots(nrows=nrows,ncols=ncols,figsize=(21,15))
for ijeans in range(len(fjeans)):
    # read in data
    ifile  = glob(('%szeta_fitted_M3_vsf3d%s_weighted_ncloud100.dat') % (dsrc,fjeans[ijeans]))[0]
    zeta1,zeta2,zeta3 = np.loadtxt(ifile,skiprows=2,usecols=(1,2,3),unpack=True)
    ifile  = glob(('%szeta_fitted_M3_vsf3d%s_nonweighted_ncloud100.dat') % (dsrc,fjeans[ijeans]))[0]
    zeta1now,zeta2now,zeta3now = np.loadtxt(ifile,skiprows=2,usecols=(1,2,3),unpack=True)
    # plot data 
    for j in range(2):
        if(j==0): 
            tmp = limzeta
            xlabel = ('$\\zeta$(p), $\\lambda_J$ = %i$\\Delta$x, with' % (ljeans[ijeans]))
            ylabel = ('$\\zeta$(p), $\\lambda_J$ = %i$\\Delta$x, without' % (ljeans[ijeans]))
        else: 
            tmp = limz
            xlabel = ('$Z$(p), $\\lambda_J$ = %i$\\Delta$x, with' % (ljeans[ijeans]))
            ylabel = ('$Z$(p), $\\lambda_J$ = %i$\\Delta$x, without' % (ljeans[ijeans]))
            zeta1 = zeta1/zeta3
            zeta2 = zeta2/zeta3
            zeta3 = zeta3/zeta3
            zeta1now = zeta1now/zeta3now
            zeta2now = zeta2now/zeta3now
            zeta3now = zeta3now/zeta3now
            
        ax[j,ijeans].set_xlabel(xlabel)
        ax[j,ijeans].set_ylabel(ylabel)
        ax[j,ijeans].set_xlim(tmp)
        ax[j,ijeans].set_ylim(tmp)
        ax[j,ijeans].plot(np.array(tmp),np.array(tmp),color='grey',ls='-.',lw=lw)
    
        ax[j,ijeans].plot(zeta1,zeta1now
                         ,color=color[0],ls='',marker='o',ms=ms
                         ,markeredgecolor='black',label='p = 1')
        ax[j,ijeans].plot(zeta2,zeta2now
                         ,color=color[1],ls='',marker='o',ms=ms
                         ,markeredgecolor='black',label='p = 2')
        ax[j,ijeans].plot(zeta3,zeta3now
                         ,color=color[2],ls='',marker='o',ms=ms
                         ,markeredgecolor='black',label='p = 3')
ax[1,2].legend(loc=4)
# adjust and save figure
fig.tight_layout(pad=0.5)
fig.savefig(dfig+'fig5_comp_weighting.pdf')