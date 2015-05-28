import getopt,sys
from os.path import isdir, join
from os import makedirs
from shutil import rmtree
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import pairwise_kernels, cosine_similarity
import numpy as np
from selectivelabel import *
from writeqrel import *

topk=20
opts, args = getopt.getopt(sys.argv[1:],"j:o:f:q:r:k:w:t:")
for opt, arg in opts:
    if opt=='-o':
        outputdir=str(arg)
    if opt=='-f':
        trainf=str(arg)
    if opt=='-q':
        qid=int(arg)
    if opt=='-r':
        trecrunf=str(arg)
    if opt=='-j':
        qrelf=str(arg)
    if opt=='-k':
        kname=str(arg)
    if opt=='-w':
        wn=str(arg)
    if opt=='-t':
        threshold=float(arg)

def readtrecrun(runf):
    trf=open(runf,'r')
    runcwids=set()
    cwidsysrank=dict()
    for line in trf:
        linearray=line.split()
        pos=int(linearray[3])
        if pos > topk:
            continue
        cwid=str(linearray[2])
        runname=str(linearray[5])
        runcwids.add(cwid)
        if cwid not in cwidsysrank:
            cwidsysrank[cwid]=dict()
        cwidsysrank[cwid][runname]=pos
    trf.close()
    return runcwids, cwidsysrank

# {cwid:jud}
def readqrel(qrelf):
    qrelF=open(qrelf,'r')
    cwidjud=dict()
    for line in qrelF:
        linearray=line.split()
        cwid=linearray[2]
        jud=int(linearray[3])
        cwidjud[cwid]=jud
    qrelF.close()
    return cwidjud

# input format:  
# cwid label {term:fvalue}
# output format:
# cwid-{term:tf-idf}
def tfidffeatures(featurefile):
    features=open(featurefile,'r')
    cwids=set()
    result={}
    for line in features:
        linearray=line.split()
        if len(linearray) > 2:
            cwid=linearray[0]
            result[cwid]=dict()
            for i in range(1, len(linearray)):
                termtfidf=linearray[i].split(':')
                if len(termtfidf) == 2:
                    if len(termtfidf[0]) >=1:
                        if not termtfidf[0].replace('.','',1).isdigit():
                            result[cwid][termtfidf[0]]=float(termtfidf[1])
    features.close()
    return result

######################################################
# read in the data
######################################################
# read in tf-idf feature
features = tfidffeatures(trainf)
# read in selected qrel qid-[cwids]
cwidjud = readqrel(qrelf)
# read in trecruns
runcwids, docsysrank = readtrecrun(trecrunf)
# intereaction of different sources' cwid
icwids=set.intersection(set(cwidjud.keys()), set(features.keys()), runcwids)

# remove the duplicate entry in the training data
# since the existence of the subtopic
labels=list()
Xs=list()
fids=list()
cwidsysrank=list()
docs=list(runcwids)
for cwid in icwids:
    label = cwidjud[cwid]
    fids.append(cwid)
    cwidsysrank.append(dict(docsysrank[cwid]))
    if label > 0:
        labels.append(1)
        Xs.append(features[cwid])
    else:
        labels.append(0)
        Xs.append(features[cwid])

vec=DictVectorizer(sparse=False)
tfidf=vec.fit_transform(Xs)

######################################################
# prepare the kernel matrix
######################################################
# ['rbf', 'sigmoid', 'polynomial', 'poly', 'linear', 'cosine']
if kname == 'rbf':
    tfKernel = pairwise_kernels(tfidf, metric=kname, n_jobs=-1,filter_params=True,kwds={'gamma':1.8})
elif kname == 'cosine':
    tfKernel = cosine_similarity(tfidf)
######################################################
# different weight vector for feature selection
######################################################
docw = docweight(cwidsysrank)
# weight vector, weight name
sweight={
        "aones":(np.ones(len(fids)), "w-aones"),
        "srk":(list(docw.sysrankw()), "w-srk"),
        "appri":(list(docw.apprior()), "w-appri"),
        }

######################################################
# main program
######################################################
# make output directory
expid=wn+"-"+kname+"-"+str(threshold) +"-10"
# maxsimi
wV = sweight[wn][0]
maxselect=maxsimiw(tfKernel, wV, threshold)
for percent in [0.01,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]:
    k = int(round(len(fids) * percent))
    L = maxselect.getDocs(k)
    L_cwids = [fids[docind] for docind in L]
    outdir = join(outputdir, expid, 'qrels',str(percent))
    if not isdir(outdir):
        makedirs(outdir)
    outbqrel=open(join(outdir, str(qid) + ".bqrel"),'w')
    outoqrel=open(join(outdir, str(qid) + ".oqrel"),'w')
    outbqrel.write(bqrel(qid,L_cwids,cwidjud,docs))
    outoqrel.write(oqrel(qid,L_cwids,cwidjud,docs))
    outbqrel.close()
    outoqrel.close()
