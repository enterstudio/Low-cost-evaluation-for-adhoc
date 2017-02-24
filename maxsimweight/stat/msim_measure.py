from scipy import stats
import sys, os, math

directory="/scratch/GW/pool0/khui/result/2stagelowcost/maxsim/threshold"
# input: {qid, v} v= f1, prec, recall, accuracy
# return:
# 1, percentage of legal value (v >= 0), w.r.t. total query number 200
# 2, min max mean confidence interval
def permln(qidV):
    measures=qidV.values()
    lmeasures = [v for v in measures if v >= 0]
    length=len(lmeasures)
    lpercent = length / float(len(measures))
    n, min_max, mean, var, skew, kurt = stats.describe(lmeasures)
    left_right = stats.t.interval(0.95,length-1 ,loc=mean, scale=math.sqrt(var/length))
    resultstr=['%.4f'%min_max[0], \
                '%.4f'%min_max[1], \
                '%.4f'%mean, \
                '%.4f'%left_right[0], \
                '%.4f'%left_right[1], \
                '%.2f%%'%(lpercent*100)]
    return " ".join(resultstr)



# input:
#       qid featureM-selectM selectweight percent mln f1 accuracy precision recall
def methodselect():
    mlnpercqidf1 = {}
    mlns = []
    for line in mf:
        cols=line.split("\t")
        # percent - {mlname - {qid, value}}
        if len(cols) != 9:
            print 'ERROR',line
            continue
        qid = int(cols[0])
        if qid > 50:
            continue
        mln = str(cols[4])
        swn = str(cols[2])
        perc = float(cols[3])
        f1 = float(cols[5].split(":")[1])
        accu = float(cols[6].split(":")[1])
        prec = float(cols[7].split(":")[1])
        reca = float(cols[8].split(":")[1])
        mlns.append(mln)
        if mln not in mlnpercqidf1:
            mlnpercqidf1[mln] = dict()
        if swn not in mlnpercqidf1[mln]:
            mlnpercqidf1[mln][swn] = dict()
        if perc not in mlnpercqidf1[mln][swn]:
            mlnpercqidf1[mln][swn][perc] = dict()
        mlnpercqidf1[mln][swn][perc][qid]=f1
    mf.close()

    for mln in sorted(mlnpercqidf1.keys()):
        for swn in sorted(mlnpercqidf1[mln].keys()):
            print(" ".join(['#',selectm,feature,mln,swn]))
            for perc in sorted(mlnpercqidf1[mln][swn].keys()):
                print('%.2f '%perc +  permln(mlnpercqidf1[mln][swn][perc]))
            print("\n\n")



for threshold in ['0.00','0.60','0.70','0.80']:
    mf = open(directory + "/_measure_" + threshold)
    percF1=dict()
    print('# '+threshold)
    for line in mf:
        cols=line.split("\t")
        # percent - {mlname - {qid, value}}
        if len(cols) != 9:
            print 'ERROR',line
            continue
        qid = int(cols[0])
        threshold = float(cols[1])
        perc = float(cols[3])
        f1 = float(cols[5].split(":")[1])
        if perc not in percF1:
            percF1[perc]=dict()
        percF1[perc][qid]=f1
    for perc in sorted(percF1.keys()):
        print('%.2f '%perc +  permln(percF1[perc]))
    print("\n\n\n")
    mf.close()



