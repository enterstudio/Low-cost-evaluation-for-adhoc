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

def bpqrel(qid, cwidjud, docs, cwidpred):
    qrel=list()
    for cwid in docs:
        if cwid in cwidpred:
            if cwidpred[cwid] > 0:
                label = 1
            elif cwidpred[cwid]==-2:
                label = -2
            else:
                label = 0
        elif cwid in cwidjud:
            label = cwidjud[cwid]
        else:
            label = -2
        qrel.append(str(qid)+" 0 "+cwid+" "+str(label))
    return "\n".join(qrel)
