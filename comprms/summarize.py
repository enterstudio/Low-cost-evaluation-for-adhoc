from basicfunc import *
import numpy as np
from os.path import basename,join
from os import listdir,walk
import sys, getopt

opts, args = getopt.getopt(sys.argv[1:],"f:s:m:")
for opt, arg in opts:
    if opt=='-f':
        corrf=str(arg)
    if opt=='-s':
        samplen=str(arg)

#yearmap={9:'09',10:'10',11:'11',12:'12'}
yearmap={11:'11',12:'12',13:'13',14:'14'}

def corr(expcorr):
    yearperccorr=dict()
    for expname in expcorr:
        cols = expname.split('-')
        year = int(cols[0])
        perc = float(cols[1])
        if year not in yearmap:
            continue
        if year not in yearperccorr:
            yearperccorr[year]=dict()
        yearperccorr[year][perc]=expcorr[expname]
    outstrs=list()
    for year in sorted(yearperccorr):
        outstrs.append('# ' + yearmap[year])
        for perc in sorted(yearperccorr[year]):
            outstrs.append('%.2f'%perc + " " + '%.4f'%yearperccorr[year][perc])
        outstrs.append('\n\n')
    return outstrs

def rndcorr(expcorr):
    yearperccorr=dict()
    for expname in expcorr:
        cols = expname.split('-')
        year = int(cols[0])
        perc = float(cols[1])
        sid = int(cols[2])
        if year not in yearmap:
            continue
        if year not in yearperccorr:
            yearperccorr[year]=dict()
        if perc not in yearperccorr[year]:
            yearperccorr[year][perc]=dict()
        yearperccorr[year][perc][sid]=expcorr[expname]
    outstrs=list()
    for year in sorted(yearperccorr):
        outstrs.append('# ' + yearmap[year])
        for perc in sorted(yearperccorr[year]):
            corrs = yearperccorr[year][perc].values()
            length = len(corrs)
            n, min_max, mean, var, skew, kurt = stats.describe(corrs)
            left_right = stats.t.interval(0.95,length-1 ,loc=mean, scale=math.sqrt(var/length))
            outstr = ['%.2f'%perc, '%.4f'%mean, '%.4f'%min_max[0], '%.4f'%min_max[1], '%.4f'%left_right[0], '%.4f'%left_right[1]]
            outstrs.append(' '.join(outstr))
        outstrs.append('\n\n')
    return outstrs


corrf=open(corrf, 'r')
expcorr=dict()
for line in corrf:
    cols=line.split('\t')
    if len(cols[1].rstrip())<1:
        continue
    expname = cols[0]
    corrv = float(cols[1])
    expcorr[expname]=corrv

# rnd ipool tpool mtc
if samplen.startswith('rnd') or samplen.startswith('stat'):
    outstrs = rndcorr(expcorr)
else:
    outstrs = corr(expcorr)
print '\n'.join(outstrs)
