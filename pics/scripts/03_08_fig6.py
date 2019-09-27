##############################################################################
## This script reproduces Fig. 6 of Chira et al. (2019).                    ##
##############################################################################

# import required python packages 
import numpy as np
import csv
from glob import glob
import matplotlib.pyplot as plt

# define function that return predicted values of zeta
# Boldyrev (2002)
def zboldyrev(p):
    return (p/9.+1.-(1./3.)**(p/3.))
# She & Leveque (1992)
def zshe(p):
    return (p/9.+2.-2.*(2./3.)**(p/3.))

# define plot parameters
plt.rcParams['font.size'] = 18
ms          = 12
lw          = 3
ncols       = 3
nrows       = 1
xlim        = [ 0.0,6.2]
ylim        = [-0.9,2.2]
ccloud      = ['red','green','blue']
marker      = ['x','d','.']
meanprops   = dict(linestyle='--', linewidth=lw,color='steelblue')
medianprops = dict(linestyle='-', linewidth=lw)
boxprops    = dict(linestyle='-', linewidth=lw)
whiskprops  = boxprops
capprops    = boxprops
# define scenarios
fcloud = ['M3','M4','M8']

# define source folder
dsrc = '../../src_data/vsf/zeta_fitted/'
dobs = './'

# define target folder
dfig = '../../vsf_output/'

# read in observation data
header = True
ref,rlabel,rp,rzeta,rezeta,rz,rez = np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([])
ifile = glob(('%scomp_obs_vsf.csv' % dobs))[0]
with open(ifile,'r') as fin:
    tmp = csv.reader(fin, delimiter=',')
    for row in tmp:
        if(header==True): header = False
        else: 
            ref    = np.append(ref,row[0])
            rlabel = np.append(rlabel,row[3])
            rp      = np.append(rp,int(row[4]))
            rzeta   = np.append(rzeta,float(row[5]))
            rezeta  = np.append(rezeta,float(row[6]))
            rz      = np.append(rz,float(row[7]))
            rez     = np.append(rez,float(row[8]))

# plot data
fig,ax = plt.subplots(ncols=ncols,nrows=nrows,sharex=True,sharey=True,figsize=(21,7))

for p in range(3):
    h = np.where(rp == (p+1))[0]
    ax[p].fill_between(xlim,np.array(xlim)*0.+np.min(rzeta[h]),np.array(xlim)*0.+np.max(rzeta[h])
                       ,color='grey',alpha=0.25,label='area of observed values')

for icloud in range(len(fcloud)):
    cloud = fcloud[icloud]
    time,zeta1,zeta2,zeta3 = np.array([]),np.array([]),np.array([]),np.array([])
    
    ifile = glob(('%szeta_fitted_%s_vsf3d*lambda04*weighted_ncloud100.dat' % (dsrc,cloud)))[0]
    ttime,tzeta1,tzeta2,tzeta3 = np.loadtxt(ifile,skiprows=1,usecols=(0,1,2,3),unpack=True)
    time,zeta1,zeta2,zeta3 = np.append(time,ttime),np.append(zeta1,tzeta1),np.append(zeta2,tzeta2),np.append(zeta3,tzeta3)
    
    
    for p in range(3):
        zeta = np.array([])
        if(p == 0):
            title = '$p$ = 1'
            zeta  = zeta1
        elif(p == 1):
            title = '$p$ = 2'
            zeta = zeta2
        else:
            title = '$p$ = 3'
            zeta = zeta3
    
        ax[p].set_title(title)
        ax[p].plot(time,zeta,ls='-',marker='o',label=cloud,color=ccloud[icloud],lw=lw,ms=ms,markeredgecolor='black')
        ax[p].set_xlabel('time [Myr]')
        
ax[0].set_xlim(xlim)
ax[0].set_ylim(ylim)
ax[0].set_ylabel('$\zeta(p)$')
ax[0].legend(loc=3)

# adjust and save plot
fig.tight_layout(pad=0)
fig.subplots_adjust(wspace=0)
plt.savefig(dfig+'fig6_compare_observations.pdf')
