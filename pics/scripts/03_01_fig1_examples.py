##############################################################################
## This script reproduces Fig. 1 of Chira et al. (2019).                    ##
##############################################################################


# import required python packages
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from scipy.optimize import curve_fit

# define fitting function
def vsffit(lag,lna,p):
    return (lna+p*lag)

# define source folder
dsrc = '../../src_data/vsf/vsf3d/'

# define target folder
dfig = '../../vsf_output/'

# define sample for Fig. 1
cloud = ['M4','M3','M3']
time  = ['0010','0030','0042']
color = ['red','green','blue']
title = ['decaying turbulence','SN shocked','gravitationally collapsing']

# define plot parameters
xlim  = [0.6,41]
ylim  = [4e-2,7e1]
posx  = [5,11.5,3]
ms    = 15
lw    = 5
plt.rcParams['font.size'] = 21

# draw plot
fig,ax = plt.subplots(nrows=nrow,ncols=ncol,sharex=True,sharey=True,figsize=(21,23))

for ex,itime in itertools.product(range(len(dcloud)),range(len(dtime))):
for ex in range(3):
    ifile = glob('%s%s*%s*lambda04*weighted*ncloud100*out' % (dsrc,cloud[ex],time[itime]))[0]
    lag,s1,s2,s3 = np.array([]),np.array([]),np.array([]),np.array([])
    lag,s1,s2,s3 = np.loadtxt(ifile,skiprows=2,usecols=(0,1,2,3),unpack=True)
    
    for p in range(1,4):
        if(p==1): vsf = s1
        if(p==2): vsf = s2
        if(p==3): vsf = s3
        
        # fit current data
        h = np.where(lag <= 8.)[0]
        popt, pcov = curve_fit(vsffit,np.log10(lag[h]),np.log10(vsf[h]))
        # plot fit as solid line
        ax[itime,ex].plot(lag[h],10.**vsffit(np.log10(ltot[h]),*popt)
                   ,ls='-',color=color[p-1],ms=ms,lw=lw
                   ,markeredgecolor='black')
        # plot data as dots
        ax[itime,ex].plot(lag,vsf,marker='o',ls='--'
                   ,label=('p = %i' % p),color=color[p-1],ms=ms,lw=lw
                   ,markeredgecolor='black')
   
        
        
    # print labels and legend
    
    ax[ex].text(8,8e-2,('%s, t = %3.1f Myr' % (cloud[ex],0.1*float(time[ex]))))
    ax[ex].text(posx[ex],5e-2,('%s' % title[ex]))
    
    if(ex==0): 
        ax[itime,ex].set_ylabel('S$_{\ell}$(${\ell}$) [(km s$^{-1}$)$^p$]') 
        if(itime=0): ax[itime,ex].legend(loc=0)
    ax[itime,ex].set_xscale('log')
    ax[itime,ex].set_yscale('log')
    ax[itime,ex].set_xlim(xlim)
    ax[itime,ex].set_ylim(ylim)
    if(itime == len(dtime)-1): ax[itime,ex].set_xlabel('${\ell}$ [pc]')
    if(itime == 0): ax[itime,ex].set_title('%s' % (cloud))
    ax[itime,ex].text(0.7,45,'t = %3.1f Myr' % (float(time)*0.1))
    
# adjust paper to plot and save figure
fig.tight_layout(pad=0.5)
fig.subplots_adjust(wspace=0)
fig.subplots_adjust(hspace=0)
fig.savefig(dfig+'fig1_vsf_example.pdf')