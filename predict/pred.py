import getopt,sys
from os.path import isdir, join, isfile
from os import makedirs, remove
from sklearn.svm import LinearSVC
from sklearn.feature_extraction import DictVectorizer
from writeqrel import *

topk=20
opts, args = getopt.getopt(sys.argv[1:],"j:o:f:q:r:")
for opt, arg in opts:
    if opt=='-o':
        outdir=str(arg)
    if opt=='-f':
        trainf=str(arg)
    if opt=='-q':
        qid=int(arg)
    if opt=='-j':
        qrelf=str(arg)
    if opt=='-r':
        trecrunf=str(arg)

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
        jud=int(linearray[3])
        if jud == -2:
            continue
        cwid=linearray[2]
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
icwids=set.intersection(set(features.keys()), runcwids)

# generate training and test data
X_train = list()
y_train = list()
docs=list(runcwids)
for cwid in cwidjud.keys():
    if cwid not in icwids:
        continue
    jud = cwidjud[cwid]
    X_train.append(features[cwid])
    if jud > 0:
        y_train.append(1)
    else:
        y_train.append(0)
X_test = list()
fids_test=list()
for cwid in runcwids:
    if cwid in cwidjud.keys() or cwid not in icwids:
        continue
    X_test.append(features[cwid])
    fids_test.append(cwid)
vec=DictVectorizer(sparse=False)
X = X_train + X_test
X=vec.fit_transform(X)
X_train = X[:len(X_train)]
X_test = X[len(X_train):]

######################################################
# main program
######################################################
if 1 in y_train and 0 in y_train:
    clf=LinearSVC(class_weight='auto')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
else:
    y_pred = [-2]*len(fids_test)
# output pqrel 
cwid_pred = dict(zip(fids_test, y_pred))
if not isdir(outdir):
    makedirs(outdir)
outfname=join(outdir, str(qid) + ".pqrel")
if isfile(outfname):
    remove(outfname)    
outpqrel=open(outfname,'w')
outpqrel.write(bpqrel(qid,cwidjud,docs,cwid_pred))
outpqrel.close()
