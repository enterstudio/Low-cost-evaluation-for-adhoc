def bqrel(qid, L, cwidjud, docs):
    qrel=list()
    for cwid in docs:
        if cwid in L:
            if cwidjud[cwid] > 0:
                label = 1
            else:
                label = 0
        else:
            label = -2
        qrel.append(str(qid)+" 0 "+cwid+" "+str(label))
    return "\n".join(qrel)

def oqrel(qid, L, cwidjud, docs):
    qrel=list()
    for cwid in docs:
        if cwid in L:
            qrel.append(str(qid)+" 0 "+cwid+" "+str(cwidjud[cwid]))
        else:
            qrel.append(str(qid)+" 0 "+cwid+" "+str(-2))
    return "\n".join(qrel)

# include probability
# qid cwid jud algorithm probability
def prel(qid, cwidjud, docs, cwidinProb):
    prels=list()
    for cwid in docs:
        if cwid in cwidinProb:
            prob = cwidinProb[cwid]
            label = cwidjud[cwid]
            # for the algorithm id, we set as 2:
            # refer to: http://ciir.cs.umass.edu/research/million/results07.html
            # 0 (UMass algorithm), 1 (NEU algorithm with a selection bug), 
            # 2 (selected by both algorithms), or 3 (NEU algorithm after the bug was fixed)
            newline = [str(qid), cwid, str(label), str(2),'%.4f'%prob]
            prels.append(' '.join(newline))
    return "\n".join(prels)


def bpqrel(qid, cwidjud, docs, cwidpred):
    qrel=list()
    for cwid in docs:
        if cwid in cwidpred:
            if cwidpred[cwid] > 0:
                label = 1
            else:
                label = 0
        else:
            label = -2
        qrel.append(str(qid)+" 0 "+cwid+" "+str(label))
    return "\n".join(qrel)
