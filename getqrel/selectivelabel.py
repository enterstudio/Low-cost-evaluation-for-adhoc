import numpy as np
import os, math

def computePurity(est_label,labels):
    relpercent={}
    precision={}
    pointpercent={}
    totalrel=float(sum(labels))
    est_l=np.array(est_label)
    act_l=np.array(labels)
    totalpoint=float(len(est_l))
    for l in sorted(set(est_label)):
        if totalrel > 0:
            relpercent[l]=sum(act_l[[est_l==l]])/totalrel
        else:
            relpercent[l]=0
        precision[l]=sum(act_l[[est_l==l]])/float(len(est_l[est_l==l]))
        pointpercent[l]=len(est_l[[est_l==l]])/totalpoint
    return relpercent,pointpercent,precision


def stat(qid, percent,name, simi, posLabels,labels):
    outputstr=list()
    est_labels = [0] * len(labels)
    for index in posLabels:
        est_labels[index] = 1
    estimator_labels_ = np.array(est_labels)
    relpercent,pointpercent,precision=computePurity(est_labels,labels)
    for l in sorted(relpercent.keys()):
        outputstr.append(str(qid) +'\t' + name + '\t'  +'%.2f'%percent+'\t'+str(l)+ \
                '\t%.4f'%(np.sum(simi[[estimator_labels_==l]])/ \
                float((np.count_nonzero([estimator_labels_==l]) * len(labels)))) + \
                '\t%.2f%%'%(relpercent[l]*100)+ \
                '\t%.2f%%'%(precision[l]*100)+ \
                '\t%.2f%%'%(pointpercent[l]*100) + \
                '\t'+'%.2f%%'%(sum(labels)/float(len(labels)) * 100) + \
                '\t'+str(sum(labels)) + \
                '\t'+str(len(labels)))
    return "\n".join(outputstr)


def selectlabels(k, L, X, y, ids):
    X_train = [X[index] for index in L]
    X_test = [X[index] for index in range(0, len(y)) if index not in L]
    y_train = [y[index] for index in L]
    y_test = [y[index] for index in range(0, len(y)) if index not in L]
    ids_train = [ids[index] for index in L]
    ids_test = [ids[index] for index in range(0, len(y)) if index not in L]
    #percent = len(L) / float(trecrun[qid][k])
    return X_train, y_train, ids_train, X_test, y_test, ids_test

class maxsimiw:
    '''
    Datastructure, in total, we have n docs
    SIM_(nxn): similarity between docs
    MAX_(n): record of the for the maximum similarity between d_i and d in L, 
    i.e., max_{d \in L} sim(d_ij, d), denoted as maxsim(d_ij,d_L)
    k: the size of L
    w_(n): the weight vector for documents, where w_i is the weight for d_i

    Algo:
    MAX = {0}
    while |L| <= k:
        (1)
        compute delta_sim for each d_i to select the next doc in L: for each document d_j in D, 
        sum up the similarity difference (gain), if sim(d_i, d_j) is larger than last step's maxsim of d_j,
        i.e., maxsim(d_j, d_L):
            gain_simi(d_i) = \sum_{d_j \in D, sim(d_i, d_j) > maxsim(d_j, d_L)} w_i(sim(d_j, d_i) - maxsim(d_j, d_L))
        (2) 
        pick up d_i with the max gain_simi value, intuitively, this step gain the representativeness of the L
        L = L \cup d_i
        (3)
        update MAX accordingly, for d_j in {d_j \in D, sim(d_i, d_j) > maxsim(d_j, d_L)} in (1), update the MAX entries
    '''
    mname='maxsimiw'
    
    def __init__(self, simi, w, threshold=0):
        self.simi = np.matrix(simi)
        self.maxa = np.zeros(simi.shape[0])
        self.w = np.array(w)
        self.thres = threshold
        self.L = list()

    def computeSimiGain(self):
        simi = self.simi
        maxa = self.maxa
        w = self.w
        nx, ny = simi.shape
        threshold = self.thres
        # {similarity gain sum : r-index of the doc}
        deltasums = dict()
        # d_i as candidate to add to L 
        for i in range(0, nx):
            if i in self.L:
                continue
            simdeltasum = 0
            # for each d_j in D, compute the gain and sumup
            for j in range(0, ny):
                simv = simi[i,j]
                maxv = maxa[j]
                if simv > maxv and simv >= (threshold * simi[i,i]):
                    # take the importance of d_j, w_j, into consideration
                    simdeltasum += (simv - maxv) * w[j]
            deltasums[simdeltasum] = i
        #print deltasums.keys()
        argmax_d = deltasums[max(deltasums.keys())]
        return argmax_d

    def updatemaxa(self, argmax_d):
        simi = self.simi
        maxa = self.maxa
        nx, ny = simi.shape
        i = argmax_d
        threshold = self.thres
        # when add argmax_d to L, for each 
        # d_j check and update there max similarity
        # w.r.t. the L
        for j in range(0, ny):  
            simv = simi[i,j]
            maxv = maxa[j]
            if simv > maxv and simv >= (threshold * simi[i,i]):
                maxa[j] = simv 

    def getDocs(self, k):
        simi = self.simi
        maxa = self.maxa
        while len(self.L) < min(k, simi.shape[0]):
            argmax_d = self.computeSimiGain()
            self.updatemaxa(argmax_d)
            self.L.append(argmax_d)
        return self.L

class docweight:
    '''
    input: 
    sysrank: [{sys:rank}]

    algorithm:
    count the number of system that contains
    the given documents, and the weight equals
    to the count of occurrences of the doc in the sysrank
    '''
    def __init__(self, sysrank):
        self.sysrank = sysrank

    def syscount(self):
        sysrank = self.sysrank
        weights = [len(sysr) for sysr in sysrank]
        return weights

    def syscountn(self):
        sysrank = self.sysrank
        raww = self.syscount()
        avew = np.mean(raww)
        normw = [round(float(w) / avew) if w > avew else 1 for w in raww]
        return normw
    
    # return weight of documents
    # for top percent documents in terms of occurrence count
    # return 2, others 1
    def syscountpn(self, percent=0.1):
        sysrank = self.sysrank
        raww = self.syscount()
        avew = np.mean(raww)
        threshold = np.percentile(raww, int((1 - percent) * 100))
        normw = [round(threshold/avew) if w > threshold else 1 for w in raww]
        return normw

    # use the 1 / log(pos + 1) 
    def sysrankw(self):
        sysrank = self.sysrank
        weight = list()
        for i in range(0, len(sysrank)):
            weight.append(sum([(1.0 / math.log(rank + 1, 2)) for rank in sysrank[i].values()]))
        return weight
    
    # compute the ap prior, indicating the relevance of an unlabeled documents
    # refer: A practical samplling strategy for efficient retrieval evaluation, Section 2.4
    def apprior(self, topk=20):
        sysrank = self.sysrank
        weight = list()
        const = 1.0 / (2 * topk)
        for i in range(len(sysrank)):
            weight.append(sum([(const * math.log(topk / float(rank), 2)) for rank in sysrank[i].values()]))
        return weight

    def disagree(self, sysnames):
        cwidSysrank = self.sysrank
        n = len(sysnames)
        D = np.matrix(np.diag([n] * n))
        W = np.matrix(np.ones((n,n)))
        L = D - W
        docDiffs = list()
        for sysrank in cwidSysrank:
            weight = list()
            for sysn in sorted(sysnames):
                if sysn in sysrank:
                    rank = sysrank[sysn]
                    weight.append(1.0 / math.log(rank + 1, 2))
                else:
                    weight.append(0)
            diff = (np.matrix(weight) * L * np.matrix(weight).T)[0,0]
            docDiffs.append(diff)
        return docDiffs


    def disagreesqrt(self, sysnames):
        docDiffs = self.disagree(sysnames)
        docDiffs = [math.sqrt(w) for w in docDiffs]
        return docDiffs

    def entropy(self, sysnames, posbinlen=5):
            C = float(len(sysnames))
            sysranks = self.sysrank
            docEntropy = list()
            for d in range(len(sysranks)):
                sysrank = sysranks[d]
                posbins = dict()
                # for each doc d, compute class-count
                for sys in sysnames:
                    if sys not in sysrank:
                        if 0 not in posbins:
                            posbins[0] = 0
                        posbins[0] += 1
                    else:
                        pos = sysrank[sys] / posbinlen
                        if pos not in posbins:
                            posbins[pos] = 0
                        posbins[pos] += 1
                # compute entropy
                entropy = 0
                for pos in posbins.keys():
                    count = posbins[pos]
                    prob = count / C
                    entropy += - prob * math.log(prob, 2)
                docEntropy.append(entropy)
            return docEntropy

    def kldivergence(self,sysnames):
        print "being called"
        C = float(len(sysnames))
        sysranks = self.sysrank
        docDivergence = list()
        for d in range(len(sysranks)):
            sysrank = sysranks[d]
            sysProb = dict()
            # for each doc d, compute class-count
            for sys in sysnames:
                if sys not in sysrank:
                    prob = 1.0 / math.log(200 + 1, 2)
                else:
                    pos = sysrank[sys]
                    prob = 1.0 / math.log(pos + 1, 2)
                sysProb[sys] = prob
            cProb = np.mean(sysProb.values())
            divergence = 0
            for sys in sysProb:
                rprob = sysProb[sys]
                irprob = 1 - sysProb[sys]
                relD = rprob * math.log(rprob / cProb, 2) \
                        if rprob / cProb > 0 else 0
                irelD = irprob * math.log(irprob / (1 - cProb), 2) \
                        if irprob / (1 - cProb) > 0 else 0
                divergence += (relD + irelD)
            docDivergence.append(np.absolute(divergence / C))
        return docDivergence


