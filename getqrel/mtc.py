import getopt,sys,math
from os.path import isdir, join
from os import makedirs
import numpy as np
from operator import sub
from scipy.sparse import csr_matrix
from writeqrel import *

topk=20
opts, args = getopt.getopt(sys.argv[1:],"j:o:q:r:")
for opt, arg in opts:
    if opt=='-o':
        outputdir=str(arg)
    if opt=='-q':
        qid=int(arg)
    if opt=='-r':
        trecrunf=str(arg)
    if opt=='-j':
        qrelf=str(arg)

# {cwid:jud}
def readqrel(qrelf):
    qrelF=open(qrelf,'r')
    cwidjud=dict()
    for line in qrelF:
        linearray=line.split()
        cwid=linearray[2]
        if cwid not in runcwids:
            continue
        jud=int(linearray[3])
        cwidjud[cwid]=jud
    qrelF.close()
    return cwidjud

def readtrecrun(runf):
    trf=open(runf,'r')
    runcwids=set()
    runnames=set()
    runcwidrank=dict()
    for line in trf:
        linearray=line.split()
        pos=int(linearray[3])
        if pos > topk:
            continue
        cwid=str(linearray[2])
        runname=str(linearray[5])
        runnames.add(runname)
        runcwids.add(cwid)
        if runname not in runcwidrank:
            runcwidrank[runname]=dict()
        runcwidrank[runname][cwid]=pos
    trf.close()
    return runcwids,runcwidrank,runnames
percents=[0.01,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9, 0.95]
######################################################
# read in the data
######################################################
runcwids, runcwidrank, runnames = readtrecrun(trecrunf)
cwidjud  = readqrel(qrelf)

# generate the document-system rank matrix
# each row represents a document, each column correponds
# to a system
docs=list()
labels=list()
systems=list(runnames)
# {runind-[docrank]}, the index of the list is the docindex from docs list, runindex is from systems list
systemdoc=dict()
docsystem=dict()
# |R|
relNum=0
for indOfRun in range(len(systems)):
    run = systems[indOfRun]
    if indOfRun not in systemdoc:
        systemdoc[indOfRun]=[-1]*len(runcwids)
    for cwid in runcwidrank[run]:
        if cwid not in docs:
            docs.append(cwid)
            dindex=len(docs)-1
            docsystem[dindex]=list()
            if cwidjud[cwid] > 0:
                relNum += 1
                labels.append(1)
            else:
                labels.append(0)
        else:
            dindex=docs.index(cwid)
        docsystem[dindex].append(indOfRun)
        systemdoc[indOfRun][dindex]=runcwidrank[run][cwid]

docnum=len(docs)
dnumPerc=dict()
for perc in percents:
    dnumPerc[int(docnum * perc)]=perc
######################################################
######################################################
## the implement of MTC
## described in paper (Carterette et.al, sigir06) and Carterette's sigir10 tutorial 
## (P97, updating document weight; P98, stop condition; P99, MTC for AP the algorithm)
## here we impletement the original version of MTC: with p = 0.5 and actively fetch document for label
## at each round

## data structure
## suppose we have n documents and k systems
## A_(n X n): the weight for each document in computing AP for each system
## C_(n X n): the difference of A between two given system C[si,sj] = A[si] - A[sj]
## S: maintained list for the documents being judged
## U: maintained list for the documents unjudged yet
## As_(k) the list of A
## Cs_(k X k) the matrix recording the difference among A, C[si,sj] = A[si] - A[sj],
## and Cs is upper triangle
## APDiff_(k X k) the matrix keep updating the delat_AP
## APDone_(k X k) the matrix keep recording whether we finished for each system pair
## docw_(n): the global weight for each document, docw[i] = \sum {doc_w from all system pair}
## docwrs_(k X k): the docwr for each system pair,each entry, representing a system pair, is a vector, recording weight for all doc

############
## docws_(k X k): the docw for each system pair, each entry, representing a system pair, is a vector, recording weight for all doc
## docwns_(k X k): the docwn for each system pair, ..
## docwn_(n): the global nonrelevant weight for each document, largest nonrelevant weight from all system pair
##########

## main algorithm
## S = empty, U = all documents
## prepare As and Cs
## while(!all done in APDone)
##      for doc_i in U
##          w_sum_i<-0 // sum up all doc weight from different system pair
##          for system pair in APDone_(k X k)
##              if system pair not done
##                compute w_i, wr_i for doc_i for current system pair
##                w_sum_i += w_i
##                docwrs[system pair][i]<- wr_i
##          docw[i]<-w_sum_i
##      pick up doc_l with largest weight from docw
##      fetch label for doc_l
##      compute delta_AP and update APDiff, for all system pair
##      check stop condition and update APDone
##      S <- S + doc_l
##      U <- U - doc_l
##
## compute w_i for each doc_i in given system pair
## computeW(d_i, system pair, Cs, S, U)
##      Cs_delta = Cs[system pair] // get the delta_a matrix for these two systems
##      mitJudged = 0
##      for d_j in S
##         if d_j is relevant
##            mitJudged += Cs_delta[i,j]
##      mitUnjudged = 0
##      for d_j in U
##          mitUnjudged += Cs_delta[i,j]
##      wr = Cs_delta[i, i] + mitJudged
##      wn = Cs_delta[i, i] + mitJudged + mitUnjudged
##
## check stop condition for given system pair
## checkDone(docwr, S, APDone)
##     for system pair in APDone
##         if system pair not done
##             isdone<-true
##             compute delta_AP for system pair with labeled doc from S
##             if delta_AP > 0
##                for wr in increasingSort(docwr)
##                      delta_AP += wr
##                      if delta_AP < 0
##                          isdone<-false
##                          break
##                      if wr > 0
##                          break
##             if delta_AP < 0
##                for wr in decreasingSort(docwr)
##                      delta_AP += wr
##                      if delta_AP > 0
##                          isdone<-false
##                          break
##                      if wr < 0
##                          break
##             APDone[system pair]<-isdone
##             
##
######################################################
######################################################

######################################################
# prepare a_ij matrix for each system: [A]
# entry: a_ij = 1 / max(rank(d_i), rank(d_j))
# dimension: |[A]| = |Systems|, A: n X n, where n is number of document
# prepare c_ij matrix for each system pair: [C]
# entry: c_ij = a1_ij - a2_ij
# dimension: [[C]]: k X k and up triangle 
# C: n X n, where n is the number of document
# initialize Cs
######################################################
As=[list()]*len(systems)
for sys_i in range(len(systems)):
    docrank_i = systemdoc[sys_i]
    rows=list()
    cols=list()
    datas=list()
    for doc_x in range(len(docs)):
        for doc_y in range(doc_x + 1,len(docs)):
            rankx_i = docrank_i[doc_x]
            ranky_i = docrank_i[doc_y]
            if rankx_i != -1 and ranky_i != -1:
                axy = 1.0 / (max(rankx_i, ranky_i) + 1)
                rows.append(doc_x)
                cols.append(doc_y)
                datas.append(axy)
    A_i = csr_matrix((datas, (rows, cols)), shape=(len(docs), len(docs)))
    As[sys_i] = A_i + A_i.T


Cs=[[list()]*len(systems) for s in range(len(systems))]
for sys_i in range(0, len(systems)):
    for sys_j in range(sys_i + 1, len(systems)):
        A_i = As[sys_i].todense()
        A_j = As[sys_j].todense()
        Cs[sys_i][sys_j] = (A_i - A_j)



######################################################
# compute detla AP
######################################################
def computeDeltaAP(sys_i, sys_j, SR):
    sys_i_rank = list()
    sys_j_rank = list()
    for d in SR:
        if d in systemdoc[sys_i]:
            if systemdoc[sys_i][d] != -1:
                sys_i_rank.append(systemdoc[sys_i][d])
        if d in systemdoc[sys_j]:
            if systemdoc[sys_j][d] != -1:
                sys_j_rank.append(systemdoc[sys_j][d])
    sys_i_rank = sorted(sys_i_rank)
    sys_j_rank = sorted(sys_j_rank)
    map_i = 0
    for i in range(len(sys_i_rank)):
        map_i += (i + 1.0) / sys_i_rank[i]
    map_j = 0
    for j in range(len(sys_j_rank)):
        map_j += (j + 1.0) / sys_j_rank[j]
    return map_i - map_j

######################################################
# update AP
######################################################
def updateAP(d, sysReldocs, sysAPs):
    for sys in docsystem[d]:
        rank = systemdoc[sys][d]
        sysReldocs[sys].append(rank)
        ranks = sorted(sysReldocs[sys])
        mapscore = 0
        for numrel in range(len(ranks)):
            mapscore += (numrel + 1.0) / ranks[numrel]
        sysAPs[sys] = mapscore
######################################################
# evaluate for each system pair, whether to stop
######################################################
def evalIsDone(pairs2Do, APDone, syspairDocwr, sysAPs):
    allDone=True
    currentPairs = list(pairs2Do)
    for sys_i,sys_j in currentPairs:
        isDone=True
        delta_AP=sysAPs[sys_i] - sysAPs[sys_j]
        docwr = syspairDocwr[(sys_i,sys_j)]
        if delta_AP > 0:
            for wr in sorted(docwr):
                delta_AP += wr
                if delta_AP < 0:
                    isDone=False
                    break
                if wr > 0:
                    break
        elif delta_AP < 0:
            for wr in sorted(docwr,reverse=True):
                delta_AP += wr
                if delta_AP > 0:
                    isDone=False
                    break
                if wr < 0:
                    break
        else:
            isDone=False
        APDone[sys_i][sys_j]=isDone
        if isDone:
            pairs2Do.remove((sys_i,sys_j))
        if allDone:
            allDone = isDone and allDone
    return APDone, allDone

######################################################
# initial the doc weight, output wr, wn
######################################################
def initDocWeight(pairs2Do):
    syspairDocwrs=list()
    syspairDocwns=list()
    for d in range(len(docs)):
        syspairDocwr=dict()
        syspairDocwn=dict()
        for sys_i, sys_j in pairs2Do:
            r_i = systemdoc[sys_i][d]
            r_j = systemdoc[sys_j][d]
            if r_i == -1 and r_j == -1:
                c_d = 0
            elif r_i != -1 and r_j != -1:
                c_d = 1.0 / (r_i + 1) - 1.0 / (r_j + 1)
            elif r_i == -1 and r_j != -1:
                c_d = 0 - 1.0 / (r_j + 1)
            elif r_i != -1 and r_j == -1:
                c_d = 1.0 / (r_i + 1)
            syspairDocwr[(sys_i,sys_j)]=c_d
            syspairDocwn[(sys_i,sys_j)]=c_d
        syspairDocwrs.append(dict(syspairDocwr))
        syspairDocwns.append(dict(syspairDocwn))
    return syspairDocwrs, syspairDocwns

######################################################
# for unlabeled document d_i, update the wr, wn and w 
# according to the latest labeled document d_j
# if latest label is relevant:
#       add c_ij to wr
# if latest label is irrelevant:
#       substract c_ij from wn
# update w
# syspairDocwr: (sys pair)-docwr
# syspairDocwn: (sys pair)-docwn
# sysPairWrs: (syspair)-list of docwr
######################################################
def unjudgedDocWeight(d_i, ds_jud, pairs2Do, syspairDocwr, syspairDocwn, sysPairWrs):
    ws=list()
    for sys_i,sys_j in pairs2Do:
        if (sys_i, sys_j) not in sysPairWrs:
            sysPairWrs[(sys_i, sys_j)]=list()
        if systemdoc[sys_i][d_i] != -1 or systemdoc[sys_j][d_i] != -1:
            C_ij=Cs[sys_i][sys_j]
            for d_j in ds_jud:
                c_ij=C_ij[d_i,d_j]
                if labels[d_j] > 0:
                    syspairDocwr[(sys_i,sys_j)] += c_ij
                if labels[d_j] <= 0:
                    syspairDocwn[(sys_i,sys_j)] -= c_ij
            wr=syspairDocwr[(sys_i,sys_j)]
            wn=syspairDocwn[(sys_i,sys_j)]
            sysPairWrs[(sys_i, sys_j)].append(wr)
            w = abs(max(wr, wn))
            ws.append(w)
    return sum(ws)


######################################################
# main algorithm
######################################################
# U: unlabeled S: labeled doc list
U=range(len(docs))
S=list()
SR=list()
isDone=False
sysNotDone=range(len(systems))
APDone=[[False]*len(systems) for i in range(len(systems))]
pairs2Do = [(sys_i, sys_j) for sys_i in range(len(systems)) for sys_j in range(len(systems)) \
                if (sys_j > sys_i)]
docSyspairWrs, docSyspairWns = initDocWeight(pairs2Do)
# list of list of rel docs, list of AP
sysReldocs = [[]]*len(systems)
sysAPs = len(systems)*[0]
ds_jud=list()
while not isDone and len(U) > 0:
    syspairWrs=dict()
    docw=dict()
    for d_i in U:
        docweight = unjudgedDocWeight(d_i, ds_jud, pairs2Do, docSyspairWrs[d_i], docSyspairWns[d_i],syspairWrs)
        ds_jud=list()
        if docweight not in docw:
            docw[docweight]=list()
        docw[docweight].append(d_i)
    sorteddocw=sorted(docw.keys(), reverse=True)
    for dw in sorteddocw:
        for max_d in docw[dw]:
            S.append(max_d)
            if len(S) in dnumPerc.keys():
                perc = dnumPerc[len(S)]
                outdir = join(outputdir,str(perc))
                if not isdir(outdir):
                    makedirs(outdir)
                outbqrel=open(join(outdir, str(qid) + ".bqrel"),'w')
                outoqrel=open(join(outdir, str(qid) + ".oqrel"),'w')
                S_cwids = [docs[dind] for dind in S]
                outbqrel.write(bqrel(qid, S_cwids,cwidjud,docs))
                outoqrel.write(oqrel(qid, S_cwids,cwidjud,docs))
                outbqrel.close()
                outoqrel.close()
            U.remove(max_d)
            ds_jud.append(max_d)
            if labels[max_d] > 0:
                SR.append(max_d)
                updateAP(max_d, sysReldocs, sysAPs)
                break
    APDone, isDone = evalIsDone(pairs2Do, APDone, syspairWrs, sysAPs)
    if isDone:
        perc = float(len(S)) / len(labels)
        outdir = join(outputdir,'done')
        if not isdir(outdir):
            makedirs(outdir)
        outbqrel=open(join(outdir, str(qid) + "-" + '%.1f'%(perc*100)  + ".bqrel"),'w')
        outoqrel=open(join(outdir, str(qid) + "-" + '%.1f'%(perc*100)  +  ".oqrel"),'w')
        S_cwids = [docs[dind] for dind in S]
        outbqrel.write(bqrel(qid, S_cwids,cwidjud,docs))
        outoqrel.write(oqrel(qid, S_cwids,cwidjud,docs))
        outbqrel.close()
        outoqrel.close()
