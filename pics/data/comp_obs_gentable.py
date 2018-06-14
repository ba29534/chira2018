import numpy as np
from glob import glob

ddir  = '/Users/roxanachira/Dropbox/chira2018/'
ddata = ddir + 'pics/data/'
dout  = ddir

print('read data')

ifile = glob(('%s*comp_obs_vsf.csv') % ddata)[0]
description,p,zeta,err_zeta,z,err_z,ref = np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([])
description,p,zeta,err_zeta,z,err_z,ref = np.genfromtxt(ifile,dtype=None,unpack=True,delimiter=',',usecols=(2,3,4,5,6,7,8))

description[0] = 'Target Object(s)'
zeta[0] = '$\zeta$'
ref[0] = 'Reference'


print('start writing data')

fout = open(('%s%s' % (dout,'tab_comp_obs_summary.tex')),'w')

fout.write('\\begin{table*} \n')
fout.write('\\centering \n')

fout.write('\t\\begin{tabular}{l|l|ccc} \n')
fout.write('\t\\centering \n')

print('%s\t%s\t%s\t%s\t%s' % (ref[0],description[0],p[0],zeta[0],z[0] ))
fout.write('\t\t%s & %s & %s & %s & %s \\\\ \\hline \n' % (ref[0],description[0],p[0],zeta[0],z[0] ))

uref = np.unique(ref[1:])

for iref in uref:
    hobj = np.where(ref == iref)[0]
    uobj = np.unique(description[hobj])
    for iobj in uobj:
        h = np.where((ref == iref) & (description == iobj))
        up = p[h]
        uzeta = zeta[h]
        uerr_zeta = err_zeta[h]
        uz = z[h]
        uerr_z = err_z[h]
        for l in range(len(h)):
            if(l == 0):
                print('%s\t%s\t%i\t%5.2f $\\pm$ %5.2f \t%5.2f $\\pm$ %5.2f' % (iref,iobj,int(up[l]),float(uzeta[l]),float(uerr_zeta[l]),float(uz[l]),float(uerr_z[l])))
                fout.write('\t\t%s & %s & %i & %5.2f $\\pm$ %5.2f & %5.2f $\\pm$ %5.2f \\\\ \n' % (iref,iobj,int(up[l]),float(uzeta[l]),float(uerr_zeta[l]),float(uz[l]),float(uerr_z[l])))
            else:
                print('\t\t%i\t%5.2f $\\pm$ %5.2f \t%5.2f $\\pm$ %5.2f' % (int(up[l]),float(uzeta[l]),float(uerr_zeta[l]),float(uz[l]),float(uerr_z[l])))
                print('\t\t &  & %i & %5.2f $\\pm$ %5.2f & %5.2f $\\pm$ %5.2f \\\\ \n' % (int(up[l]),float(uzeta[l]),float(uerr_zeta[l]),float(uz[l]),float(uerr_z[l])))

fout.write('\t\\end{tabular} \n')
                
                
fout.write('\t\\caption{Summary of observed $\\zeta$ and Z in the literature.} \n')
fout.write('\t\\label{tab:discussion:summary_obs} \n')

fout.write('\\end{table*} \n')

fout.close()

print('finalised writing data')