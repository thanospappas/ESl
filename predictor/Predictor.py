from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import random
import networkx as nx
import matplotlib.pyplot as plt

import numpy as np
from sklearn import svm, datasets
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier

class Predictor:

    fileName = ""
    features = []
    featuresOther = []
    output = []
    outputOther = []
    logistic = []
    trainThreshold = 0
    graph = nx.Graph()
    edgeSignDict = {}

    def __init__(self, filename):
        self.fileName = filename

    def readData(self, ours):
        f = open(self.fileName,'r')
        lines = f.readlines()
        lines1 = lines[1:]
        random.shuffle(lines1)
        open('all.random','w').writelines(lines1)
        f.close()
        f = open('all.random','r')
        with f:
            for line in f:
                line.replace('0\n',"0")
                splittedLine = line.split("\t")
                splittedLine[-1] = "".join(splittedLine[-1].split("\n"))
                splittedLine = map(float, splittedLine)
                sumu = splittedLine[9] + splittedLine[10]
                sumv = splittedLine[11] + splittedLine[12]
                #splittedLine.append(sumu)
                #splittedLine.append(sumv)
                selectedList = []
                tmp = []
                #tmp.append(splittedLine[15])
                tmp.append(sumu)
                tmp.append(sumv)
                selectedList = splittedLine[3:] + tmp# +splittedLine[13:14] + splittedLine[16:]
                #selectedList = splittedLine[12:]
                #self.features.append(splittedLine[9])
                #self.features.append(splittedLine[10])
                #self.features.append(splittedLine[9:11])
                #print selectedList
                #self.features.append(splittedLine[3:])
                self.features.append(selectedList)
                #print self.features
                self.output.append(splittedLine[2])
                if ours:
                    pair1 = str(splittedLine[0]) + "," + str(splittedLine[1])
                    pair2 = str(splittedLine[1]) + "," + str(splittedLine[0])
                    if pair1 not in self.edgeSignDict:
                        self.edgeSignDict[pair1] = splittedLine[2]
                    else:
                        if pair2 not in self.edgeSignDict:
                            self.edgeSignDict[pair1] += splittedLine[2]

        self.createGraph()
        f.close()
        self.readData1(True,"/home/thanos/graphs/all-new")

    def readData1(self, ours,filename):
        f = open(filename,'r')
        lines = f.readlines()
        lines1 = lines[1:]
        random.shuffle(lines1)
        open('all.random','w').writelines(lines1)
        f.close()
        f = open('all.random','r')
        with f:
            for line in f:
                line.replace('0\n',"0")
                splittedLine = line.split("\t")
                splittedLine[-1] = "".join(splittedLine[-1].split("\n"))
                splittedLine = map(float, splittedLine)
                sumu = splittedLine[5] + splittedLine[6]
                sumv = splittedLine[7] + splittedLine[8]

                selectedList = []
                tmp = []
                tmp.append(sumu)
                tmp.append(sumv)
                selectedList = splittedLine[7:] + tmp
                self.featuresOther.append(selectedList)
                self.outputOther.append(splittedLine[2])
                if ours:
                    pair1 = str(splittedLine[0]) + "," + str(splittedLine[1])
                    pair2 = str(splittedLine[1]) + "," + str(splittedLine[0])
                    if pair1 not in self.edgeSignDict:
                        self.edgeSignDict[pair1] = splittedLine[2]
                    else:
                        if pair2 not in self.edgeSignDict:
                            self.edgeSignDict[pair1] += splittedLine[2]

        self.createGraph()
        f.close()


    def train(self):
        self.trainThreshold = int(round(len(self.features)*0.8))
        self.logistic = LogisticRegression()
        self.logistic.fit(self.features[:self.trainThreshold],self.output[:self.trainThreshold])

    def predict(self):
        #print self.features[self.trainThreshold:]
        predictedSigns = self.logistic.predict(self.features[self.trainThreshold:])
        list1 = self.logistic.predict_proba(self.features[self.trainThreshold:])
        self.computeAccuracy(list1,predictedSigns)

    def predict1(self):
        #print self.features[self.trainThreshold:]
        predictedSigns = self.logistic.predict(self.featuresOther[1:])
        list1 = self.logistic.predict_proba(self.featuresOther[1:])
        self.computeAccuracy(list1,predictedSigns)

    def computeAccuracy1(self,predictions,predictedSigns):
        out = self.outputOther[1:]
        correct = 0
        for i in range(1,len(out)-1):
            if out[i] == predictedSigns[i]:
                correct+=1

        accuracy = correct / (1.0*len(out))
        print "Accuracy: " + str(accuracy)

    def computeAccuracy(self,predictions,predictedSigns):
        out = self.output[self.trainThreshold:]
        correct = 0
        for i in range(0,len(out)):
            if out[i] == predictedSigns[i]:
                correct+=1

        accuracy = correct / (1.0*len(out))
        print "Accuracy: " + str(accuracy)

    def createGraph(self):
        one = 0
        two = 0
        three = 0
        for edge, sign in self.edgeSignDict.iteritems():

            node1 = int(float(edge.split(",")[0]))
            node2 = int(float(edge.split(",")[1]))
            if int(sign) < 0:
                one +=1
                self.graph.add_edge(node1,node2,weight=-1)
            elif int(sign) > 0:
                two +=1
                self.graph.add_edge(node1,node2,weight=1)
            else:
                three +=1
                self.graph.add_edge(node1,node2,weight=0)


    def calculateStability(self):
        balanceTriangle = 0
        totalTriangles = 0
        for edge,sign in self.edgeSignDict.iteritems():
            node1 = int(float(edge.split(",")[0]))
            node2 = int(float(edge.split(",")[1]))
            commonNeigh = sorted(nx.common_neighbors(self.graph,node1,node2))

            for inode in commonNeigh:
                sign1n = self.graph.get_edge_data(node1,inode,default={'weight':10})['weight']
                sign2n = self.graph.get_edge_data(node2,inode,default={'weight':10})['weight']
                sign12 = self.graph.get_edge_data(node1,node2,default={'weight':10})['weight']
                mul = sign1n*sign2n*sign12

                if mul > 0 and mul <10 :
                    balanceTriangle +=1
                #if (sign1n*sign2n*sign12) != 0:
                totalTriangles += 1

        print "Balance percentage: " + str((1.0*balanceTriangle)/totalTriangles)




if __name__ == '__main__':
    """iris = load_iris()
    X, y = iris.data[:-2,:], iris.target[:-2]
    print str(len(X))
    print str(len(y))
    logistic = LogisticRegression()
    logistic.fit(X,y)
    print str(logistic.predict(iris.data[-2:,:])) + str(iris.target[-2])
    print str(logistic.predict_proba(iris.data[-2:,:]))"""

    """p = Predictor("/home/thanos/graphs/epinions")
    p.readData(True)
    p.train()
    p.predict()
    #p.calculateStability()
    print "-----"

    p = Predictor("/home/thanos/graphs/wiki")
    p.readData(True)
    p.train()
    p.predict()
    #p.calculateStability()
    print "-----"

    p = Predictor("/home/thanos/graphs/slashdot")
    p.readData(True)
    p.train()
    p.predict()
    #p.calculateStability()
    print "-----"""

    """p = Predictor("/home/thanos/graphs/all-new")
    p.readData(True)
    p.train()
    p.predict()
    p.calculateStability()
    print "-----"

    p = Predictor("/home/thanos/graphs/top")
    p.readData(True)
    p.train()
    p.predict()
    p.calculateStability()
    print "-----"

    p = Predictor("/home/thanos/graphs/controvertial")
    p.readData(True)
    p.train()
    p.predict()
    p.calculateStability()"""

    p = Predictor("/home/thanos/graphs/epinions")
    p.readData(True)
    p.train()
    p.predict()
    p.calculateStability()
    print "-----"

    #p = Predictor("/home/thanos/graphs/wiki")
    #p.readData1(True)
    #p.train()
    #p.predict1()
    #p.calculateStability()
    #print "-----"