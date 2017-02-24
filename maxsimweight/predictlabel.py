from sklearn import metrics


class predictlabel:
    def __init__(self, X_train, y_train, X_test, y_test):
        self.X_train = list(X_train)
        self.X_test = list(X_test)
        self.y_train = list(y_train)
        self.y_test = list(y_test)

    def fit(self, model):
        self.model = model
        self.model.fit(self.X_train, self.y_train)
        return self.model

    def predict(self):
        return self.model.predict(self.X_test)

    def fit_pred(self,model):
        self.fit(model)
        return self.predict()

    def measure(self, qid, pred, name):
        #pred=self.fit_pred(model)
        if sum(pred) == 0:
            accuracy=metrics.accuracy_score(self.y_test, pred)
            return str(qid) + "\t" + name+"\t"+"f1: %0.3f" %-1+"\t"+"accuracy: %0.3f" %accuracy+ \
                                    "\t"+"precision: %0.3f" %-1+"\t"+"recall: %0.3f" %0
        if sum(self.y_test) == 0:
            accuracy=metrics.accuracy_score(self.y_test, pred)
            return str(qid) + "\t" + name+"\t"+"f1: %0.3f" %-2+"\t"+"accuracy: %0.3f" %accuracy+ \
                                    "\t"+"precision: %0.3f" %-2+"\t"+"recall: %0.3f" %-2
        precision=metrics.precision_score(self.y_test, pred)
        recall=metrics.recall_score(self.y_test, pred)
        if precision == 0 or recall == 0:
            f1 = -1
        else:
            f1 = metrics.f1_score(self.y_test, pred)
        accuracy=metrics.accuracy_score(self.y_test, pred)
        return str(qid) + "\t" + name+"\t"+"f1: %0.3f" %f1+"\t"+"accuracy: %0.3f" %accuracy+ \
                "\t"+"precision: %0.3f" %precision+"\t"+"recall: %0.3f" %recall

    def qrel(self, pred, qid, ids_train, ids_test):
        #pred=self.fit_pred(model)
        qrel=list()
        for i in range(0, len(ids_test)):
            qrel.append(str(qid)+" 0 "+ids_test[i]+" "+str(pred[i]))
        for i in range(0, len(self.y_train)):
            qrel.append(str(qid)+" 0 "+ids_train[i]+" "+str(self.y_train[i]))
        return "\n".join(qrel)
            

