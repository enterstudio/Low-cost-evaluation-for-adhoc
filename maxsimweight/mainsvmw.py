from ml import *
from basicfunc import *
from time import time
import getopt,sys,math
from os.path import isdir, isfile,join,basename
from os import listdir, mkdir
from sklearn import tree, metrics
from sklearn.svm import LinearSVC,OneClassSVM,SVC
from sklearn.linear_model import RidgeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier,NearestCentroid
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np
from scipy import stats
from selectivelabel import *
from predictlabel import *

alpha=0.5
percent=0.1
n_clusters=2
topk=20
opts, args = getopt.getopt(sys.argv[1:],"j:o:f:q:t:r:w:")
for opt, arg in opts:
    if opt=='-o':
        outputdir=str(arg)
    if opt=='-f':
        trainf=str(arg)
    if opt=='-q':
        qid=int(arg)
    if opt=='-t':
        threshold=int(arg)
    if opt=='-r':
        trecrun=str(arg)
    if opt=='-a':
        alpha=float(arg)
    if opt=='-p':
        percent=float(arg)
    if opt=='-j':
        qrelf=str(arg)
    if opt=='-w':
        wn=str(arg)

name_param=dict()
if not isdir(outputdir):
    mkdir(outputdir)

######################################################
# read in the data
######################################################
# read in the system-doc info
# qid-{cwid-{runnames:rank}}
qidCwidRunRank, qidcwids, runnames=qidCwidRuns(trecrun, topk)
# read in tf-idf feature
features,fcwids = tfidffeatures(trainf)
# qid-[cwids]
relq, irrelq, fullq, qids = qrelrelirrel(qrelf)

# get the intersection of the cwids from three source: feature, runs, qrel
rcwids=set(qidcwids[qid])
fcwids=set(fcwids)
qcwids=set(fullq[qid])
icwids=set.intersection(rcwids, fcwids, qcwids)

# generate the document-system rank matrix
# each row represents a document, each column correponds
# to a system
SYSTEMS=[]
labeledcwid=list()

for cwid in qidCwidRunRank[qid]:
    sysrank={}
    if cwid not in icwids:
        continue
    labeledcwid.append(cwid)
    for run in qidCwidRunRank[qid][cwid]:
        sysrank[run]=qidCwidRunRank[qid][cwid][run]
    SYSTEMS.append(dict(sysrank))


# remove the duplicate entry in the training data
# since the existence of the subtopic
ys=list()
Xs=list()
for k in range(0, len(labeledcwid)):
    cwid = labeledcwid[k]
    if cwid in relq[qid]:
        ys.append(1)
        Xs.append(features[cwid])
    elif cwid in irrelq[qid]:
        ys.append(0)
        Xs.append(features[cwid])
    else:
        print cwid, 'not in qrel'

TFIDF=Xs
fids=labeledcwid
labels=ys
vec=DictVectorizer(sparse=False)
tfidf=vec.fit_transform(TFIDF)
sys=vec.fit_transform(SYSTEMS)
tfsys=np.concatenate((tfidf,sys), axis=1)
######################################################
# prepare the distance matrix
######################################################
def updateparams(descript):
    darray=descript.split(':')
    for dstr in darray:
        kv=dstr.split('=')
        name_param[kv[0]]=kv[1]


# compute the distance
tfDist=pairwise_distances(tfidf,Y=None,metric='cosine', n_jobs=-1)
#sysDist=pairwise_distances(sys,Y=None,metric='cosine', n_jobs=-1)
#tfsysDist=pairwise_distances(tfsys,Y=None,metric='cosine', n_jobs=-1)
#tfdDist=pairwise_distances(tfDist,Y=None,metric='cosine', n_jobs=-1)

######################################################
# prepare the similarity matrix
######################################################
# combine the two matrix
tfSim = np.ones(tfDist.shape) - tfDist
#tfsysSim = np.ones(tfsysDist.shape) - tfsysDist
#tfdSim = np.ones(tfdDist.shape) - tfdDist

######################################################
# machine learning algorithm
######################################################
mlModels=(
#       (LinearSVC(loss='l2', penalty="l1",dual=False,C=1, tol=1e-3), "svcL2L1","mlname=LinearSVC: \
#                mlparam=loss-l2,penalty-l1,duel-false,C-1,tol-0.001"),
        (LinearSVC(class_weight={0:3.0,1:float(threshold)}), "svcL2L2w","mlname=LinearSVC: \
                                mlparam=loss-l2,penalty-l2,duel-false,C-1,tol-0.001"),
#       (SVC(kernel='linear', C=1.0), "svcln","mlname=SVC:mlparam=kernal-linear,C-1.0"),
#       (RidgeClassifier(tol=1e-2, solver="lsqr"),"ridge","mlname=Ridge:mlparam=solver-lsqr,tol-0.01"),
    )

######################################################
# different weight vector for feature selection
######################################################
docw = docweight(SYSTEMS)
# weight vector, weight name
sweight={
           # "aones":(np.ones(len(fids)), "w-aones"),
           # (list(docw.syscount()), "w-sysrr"),
           # (list(docw.syscountn()),"w-sysrn"),
           # (list(docw.syscountpn()),"w-syr10"),
           # (list(docw.syscountpn(0.2)), "w-syr20"),
           # (list(docw.syscountpn(0.3)), "w-syr30"),
        "srk":(list(docw.sysrankw()),"w-srk"),
          #  (list(docw.sysrankw(0.2)),"w-srk20"),
          #  (list(docw.sysrankw(0.3)),"w-srk30")
          }

######################################################
# combination of feature and feature selection matrix
######################################################
# feature matrix, feature selection matrix, feature name, 
# feature selection name
# fnsn, for the directory name
ffselect=(
            (tfidf, tfSim, "f-tfidf", "s-tfidfSim","tf-tfidfSim"),
            #(tfsys, tfsysSim, "f-tfsys", "s-tfsysSim","tfs-tfsysSim-1"),      #1
            #(tfDist, tfSim, "f-tfDist", "s-tfidfSim","tfd-tfidfSim-2"),       #2
            #(tfDist, tfsysSim, "f-tfDist", "s-tfsysSim","tfd-tfsysSim-3"),   #3
            #(tfDist, tfdSim, "f-tfDist", "s-tfdSim","tfd-tfdistSim-4"),   #4
        )

######################################################
# main program
######################################################
# make output directory
# directory:  /feature type/selection method/percentage/ml-method_ml-params_selectivelabel-param/
# files: {qid}.qrel, _parameters, _ml-measures, ../selection method/percentage/select_stat/{qid}_feature_percent.stat
threshold = threshold / 3.0
for featureM,selectM,fn,sn,fsn in ffselect:
    statfile = open(outputdir + "/" + "_stat_"+wn+"_"+ '%.1f'%threshold,'a',1)
    measuref = open(outputdir + "/" + "_measure_"+wn+"_"+'%.1f'%threshold,'a',1)
    fsdir = outputdir+"/"+str(threshold)
    if not isdir(fsdir):
        mkdir(fsdir,0o775)
    ######################################
    # different selective labeling methods
    ######################################
    # maxsimi
    for percent in [0.01,0.03,0.05,0.1,0.15, 0.2,0.25, 0.3, 0.4,0.6,0.8,0.9]:
        wV = sweight[wn][0]
        maxselect=maxsimiw(selectM, wV)
    #    wvectordir = fsdir + "/" + wn
        percentdir = fsdir +"/"+ str(percent)
    #    if not isdir(wvectordir):
    #        mkdir(wvectordir,0o775)
        if not isdir(percentdir):
            mkdir(percentdir,0o775)
        k = int(len(labels) * percent)
        L = maxselect.getDocs(k)
        # output selective label stat
        namestr='%.1f'%threshold+"\t"+wn +"\t" + '%.2f'%percent
        statfile.write(stat(qid,percent,namestr,selectM,L,labels) + "\n")
        X_train, y_train, ids_train, X_test, y_test, ids_test = selectlabels(percent,L,featureM,labels,fids)
        if sum(y_train) == 0:
            print qid,percent,fsn,wn,'no positive in train'
            continue
        if 0 not in y_train:
            print qid,percent,fsn,wn,'no negative in train'
            continue
        # ML to predict
        mlpred=predictlabel(X_train, y_train, X_test, y_test)
        for model, ml_name, ml_descrip in mlModels:
            mldir = percentdir
            if not isdir(mldir):
                mkdir(mldir,0o775)
            qrelf = open(mldir + "/" + str(qid) + ".qrel",'a')
            pred = mlpred.fit_pred(model=model)
            # output prediction measure
            measuref.write(mlpred.measure(qid=qid, pred=pred, \
                    name=namestr) + "\n")
            # output qrel
            qrelf.write(mlpred.qrel(pred=pred,qid=qid,ids_test=ids_test,ids_train=ids_train) + "\n")
            qrelf.flush()
            qrelf.close()
    measuref.close()
    statfile.close()
