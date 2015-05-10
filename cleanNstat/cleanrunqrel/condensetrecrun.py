import getopt,sys

topk=10
opts, args = getopt.getopt(sys.argv[1:],"j:f:q:r:o:")
for opt, arg in opts:
    if opt=='-q':
        qid=int(arg)
    if opt=='-j':
        qrelf=str(arg)
    if opt=='-r':
        trecrunf=str(arg)
    if opt=='-o':
        outf=str(arg)
    if opt=='-k':
        topk=int(arg)

def inouttrecrun(runf, outf, cwidjud):
    trf=open(runf,'r')
    pos = 1
    count =1
    first=True
    outqrel=list()
    for line in trf:
        linearray=line.split()
        cwid=str(linearray[2])
        if cwid not in cwidjud:
            #print pos, cwid, runname
            continue
        runname = linearray[5]
        if first:
            lastrunname = runname
            first = False
        if pos > topk or runname != lastrunname:
            if runname != lastrunname:
                lastrunname=runname
                pos = 1
                #exit(0)
            else:
                continue
        score = float(linearray[4])
        outqrel.append(' '.join([str(qid),'Q0',cwid,str(pos),'%.4f'%score, runname]))
        pos += 1
    trf.close()
    outF = open(outf, 'w')
    outF.write('\n'.join(outqrel))
    outF.close()

# {cwid:jud}
def readqrel(qrelf):
    qrelF=open(qrelf,'r')
    cwidjud=dict()
    for line in qrelF:
        linearray=line.split()
        jud=int(linearray[3])
        cwid=linearray[2]
        cwidjud[cwid]=jud
    qrelF.close()
    return cwidjud
######################################################
# read in the data
######################################################
# read in selected qrel qid-[cwids]
cwidjud = readqrel(qrelf)
# read in trecruns
cwidpos = inouttrecrun(trecrunf, outf, cwidjud)
