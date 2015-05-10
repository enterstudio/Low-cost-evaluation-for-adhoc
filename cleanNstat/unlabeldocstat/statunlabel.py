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

def readtrecrun(runf):
    trf=open(runf,'r')
    cwidpos=dict()
    pos = 1
    lastrunname="start"
    for line in trf:
        linearray=line.split()
        runname = linearray[5]
        if pos > topk:
            if runname != lastrunname:
                lastrunname=runname
                pos = 1
            continue
        cwid=str(linearray[2])
        if cwid not in cwidpos:
            cwidpos[cwid]=list()
        cwidpos[cwid].append(pos)
        pos += 1
    trf.close()
    return cwidpos

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
cwidpos = readtrecrun(trecrunf)
qcwid = set(cwidjud.keys())
rcwid = set(cwidpos.keys())

diffcwid = rcwid - qcwid


missingrate = len(diffcwid) / float(len(rcwid))
print qid, len(diffcwid), len(rcwid), '%d%%'%(missingrate*100)
if qid > 50:
    outputf=open(outf,'a')
    for cwid in diffcwid:
        outputf.write(str(qid)+" "+cwid+"\n")
    outputf.close()
