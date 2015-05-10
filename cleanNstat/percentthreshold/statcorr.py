import getopt,sys
from os.path import basename

opts, args = getopt.getopt(sys.argv[1:],"i:e:")
for opt, arg in opts:
    if opt=='-i':
        inf=str(arg)
    if opt=='-e':
        exp=str(arg)



fname = basename(inf)
expids = fname.split('-')
selectn = expids[0]
metricn = expids[1]

corrs={0.85, 0.9}
yearCorrPercents=dict()
yearpercent=dict()
for line in open(inf):
    cols = line.split()
    if len(cols) < 2:
        continue
    if line.startswith('#'):
        year = int(line.split()[1])
        yearCorrPercents[year] = dict()
        yearpercent[year] = dict()
        for corr in corrs:
            yearCorrPercents[year][corr] = [1]
        continue
    percent = float(cols[0])
    corr = float(cols[1])
    yearpercent[year][percent] = corr
    for mcorr in corrs:
        if corr >= mcorr:
            yearCorrPercents[year][mcorr].append(percent)

#for corr in sorted(corrs):
#    print "#",corr
#    for year in sorted(yearCorrPercents.keys()):
#        print year, corr, min(yearCorrPercents[year][corr])
#    print '\n\n\n'

for year in [11,12,13,14]:
    if year not in yearpercent:
        print exp, selectn, metricn, year, 0
    else:
        if len(yearpercent[year]) < 20:
            print exp, selectn, metricn, year, len(yearpercent[year])



