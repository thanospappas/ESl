from editor.Features import Features
import operator
import pylab as P
import math
from editor.CompoundSentiment import CompoundSentiment
import pylab
import matplotlib.pyplot as plt
from Topic import Topic
import networkx as nx

class GraphModel:
    densityFactor = -1
    graph = None
    topics = []
    edgeScore = None
    signThreshold = 0
    epsilon = -1.0
    authorPairScore = {}
    authorPairCount = {}
    authorToInteger = {}
    savingPath = ""
    edgePairDict = {}
    fileName = ""

    def __init__(self, k, topics, thres, e, filename,savingPath):
        self.topics = topics
        self.densityFactor = k
        self.signThreshold = thres
        self.graph = nx.DiGraph()
        self.epsilon = e
        self.fileName = filename
        self.savingPath = savingPath

    def writeHeaderFile(self,f):
        first = "Author1\tAuthor2\tSign\tAvgCommentAuthor1\tAvgCommentEdge\tAvgScoreAuthor1\tAvgScoreEdge\t"
        second = "In+1\tIn-1\tOut+1\tOut-1\tIn+2\tIn-2\tOut+2\tOut-2\tCommonNeighbors\t"
        third = "FFpp\tFFpm\tFFmp\tFFmm\tFBpp\tFBpm\tFBmp\tFBmm\tBFpp\tBFpm\tBFmp\tBFmm\tBBpp\tBBpm\tBBmp\tBBmm\n"
        firstLine = first + second + third
        f.write(firstLine)

    def generateGraph(self):

        f = open(self.savingPath + self.fileName,'w')
        self.writeHeaderFile(f)
        #authorCommentCount = {}
        num = 1
        authorPairCommentsDict = {}
        intoAuthor = {}

        for topic in self.topics:
            print "working on topic: " + topic.getName()
            authors = topic.getAuthors()
            count = 0

            for author, comments in authors.iteritems():
                for comment in comments:
                    i = 0
                    pid = comment.getParentId()
                    while i < self.densityFactor:
                        selectedComment = topic.getCommentFromId(pid)

                        if selectedComment == -1:
                            count += 1
                            receiverAuthor = pid
                        else:
                            receiverAuthor = selectedComment.getAuthor()

                        pair = str(author) + "," + str(receiverAuthor)
                        if pair in self.authorPairCount:
                                self.authorPairCount[pair] += 1
                        else:
                            self.authorPairCount[pair] = 1

                        self.fillCommentsDict(pair,authorPairCommentsDict,comment)

                        if str(receiverAuthor) not in self.authorToInteger:
                            self.authorToInteger[str(receiverAuthor)] = num
                            test1 = self.authorToInteger[str(receiverAuthor)]
                            self.graph.add_node(test1)
                            intoAuthor[num] = str(receiverAuthor)
                            num += 1

                        if "int" in str(type(selectedComment)):
                            break

                        pid = selectedComment.getParentId()
                        i += 1

                #generate ids to authors
                if str(author) not in self.authorToInteger:
                    self.authorToInteger[str(author)] = num
                    test1 = self.authorToInteger[str(author)]
                    self.graph.add_node(test1)
                    intoAuthor[num] = str(author)
                    num += 1

        #Add edges
        for pair, score in authorPairCommentsDict.iteritems():
            a = pair.split(",")
            a1 = a[0]
            a2 = a[1]
            test1 = self.authorToInteger[a1]
            test2 = self.authorToInteger[a2]
            self.graph.add_edge(test1,test2,weight = 1)

        #Pruning
        prunedEdges = self.pruneGraph(intoAuthor,authorPairCommentsDict)

        #Convert digraph to undirected graph
        unG = self.graph.to_undirected(reciprocal=False)

        print "After pruning..."
        size = len(prunedEdges)
        loading = 0
        compl = 0.1
        #Compute sentiment + sign + features
        for pair, comments in prunedEdges.iteritems():
            loading+=1
            perc = loading/(1.0*size)
            if perc > compl:
                print "Loading at..." + str(compl*100) + "%"
                compl += 0.1

            a = pair.split(",")
            a1 = a[0]
            a2 = a[1]
            author1 = self.authorToInteger[a1]
            author2 = self.authorToInteger[a2]
            self.computeOurFeatures(comments,pair)
            self.computeSign(comments,f,author1,author2,pair)
            self.computeRestFeatures(author1,author2,f,unG)

        self.computeDegreeDistribution()
        f.close()

    def getGraph(self):
        return self.graph

    def fillCommentsDict(self,pair,authorPairCommentsDict,comment):
        if pair in authorPairCommentsDict:
            clist = authorPairCommentsDict[pair]
            clist.append(comment)
            authorPairCommentsDict[pair] = clist
        else:
            clist =[]
            clist.append(comment)
            authorPairCommentsDict[pair] = clist

    def computeOurFeatures(self,comments,pair):
        #Dika mas features
        for comment in comments:
            if pair in self.edgePairDict:
                features1 = self.edgePairDict[pair]
                avg1 = features1.getAvgComment12() + len(comment.getBody())
                avg2 = features1.getAvgScore12() + comment.getScore()
                features1.setEdgeFeatures(avg1, avg2)
                self.edgePairDict[pair] = features1
            else:
                features = Features()
                features.setEdgeFeatures(len(comment.getBody()), comment.getScore())
                self.edgePairDict[pair] = features

        feature = self.edgePairDict[pair]
        feature.setEdgeFeatures(feature.getAvgComment12()/((1.0)*self.authorPairCount[pair]),feature.getAvgScore12()/((1.0)*self.authorPairCount[pair]))
        a = pair.split(",")[0]
        count = 0
        commentLen = 0
        commentScore = 0
        for topic in self.topics:
            auth = topic.getAuthors()
            if a in auth:
                for comment in auth[a]:
                    count += 1
                    commentLen += len(comment.getBody())
                    commentScore += comment.getScore()
        avg1 = commentLen/ (1.0*count)
        avg2 = commentScore/ (1.0*count)
        feature.setOverall(avg1,avg2)

        self.edgePairDict[pair] = feature


    def pruneGraph(self,intoAuthor,authorPairCommentsDict):
        listforRemoval = []
        for node in nx.nodes(self.graph):
            if self.graph.degree(node) < 10:
                listforRemoval.append(node)

        for node in listforRemoval:
            self.graph.remove_node(node)

        #Extracting largest component
        largest = max(nx.strongly_connected_components(self.graph), key=len)
        H = self.graph.subgraph(largest)
        self.graph = H
        prunedEdges = {}
        for node in nx.nodes(self.graph):
            neighbors = self.graph.neighbors(node)
            for neighbor in neighbors:
                pair = str(intoAuthor[node]) + "," + str(intoAuthor[neighbor])
                prunedEdges[pair] = authorPairCommentsDict[pair]

        return prunedEdges

    def computeSign(self,comments,f,node1,node2,pair):
        #Teliko prosimo
        score = self.computeSentiment(comments)
        if score > 0:
            self.graph.add_edge(node1,node2,weight = 1)
            finalString = str(node1) + "\t" + str(node2) + "\t" + "1" + "\t" + str(self.edgePairDict[pair].masterGetter()) + "\t"
            f.write(finalString)

        else:
            self.graph.add_edge(node1,node2,weight = -1)
            finalString = str(node1) + "\t" + str(node2) + "\t" + "-1"  + "\t" + str(self.edgePairDict[pair].masterGetter()) + "\t"
            f.write(finalString)

    def computeSentiment(self, comments):
        cs = None
        cs = CompoundSentiment()
        totalSum = 0
        for comment in comments:
            scores = cs.computeVaderScore(comment.getBody())

            if float(scores[0]) < self.epsilon and float(scores[0]) > ((-1)*self.epsilon):
                if float(scores[1]) >= float(scores[3]) and float(scores[0]) <= 0:
                    totalSum += float(scores[0])
                elif float(scores[1]) >= float(scores[3]) and float(scores[0]) > 0:
                    totalSum += ((-1)*float(scores[0]))
                elif float(scores[1]) < float(scores[3]) and float(scores[0]) <= 0:
                    totalSum += ((-1)*float(scores[0]))
                else:
                    totalSum += float(scores[0])
            else:
                totalSum += float(scores[0])
        avg = totalSum / (1.0*len(comments))
        return avg

    def computeRestFeatures(self,author1,author2,f,unG):
        #Rest features
        neighbors1 = nx.all_neighbors(self.graph,author1)
        neighbors2 = nx.all_neighbors(self.graph,author2)
        commonNeighbors = 0

        nodesSeen = {}
        plusCountIn = 0
        minusCountIn =0
        plusCountOut = 0
        minusCountOut =0

        rplusCountIn = 0
        rminusCountIn =0
        rplusCountOut = 0
        rminusCountOut =0


        triadList = [0]*16
        for neighbor1 in neighbors1:
            for neighbor2 in neighbors2:
                pn = str(author2) + "," + str(neighbor2)
                if pn not in nodesSeen:
                    nodesSeen[pn] = 1
                    tmSign = self.graph.get_edge_data(author2,neighbor2,default={'weight': 0})
                    tmpSign = tmSign['weight']
                    if tmpSign < 0:
                        rminusCountOut += 1
                    elif tmpSign > 0:
                        rplusCountOut += 1
                    else:
                        tmSign = self.graph.get_edge_data(neighbor2,author2,default={'weight': 0})
                        tmpSign = tmSign['weight']
                        if tmpSign < 0:
                            rminusCountIn += 1
                        elif tmpSign > 0:
                            rplusCountIn += 1

            pn1 = str(author1) + "," + str(neighbor1)
            if pn1 not in nodesSeen:
                nodesSeen[pn1] = 1
                tmSign = self.graph.get_edge_data(author1,neighbor1,default={'weight': 0})
                tmpSign = tmSign['weight']
                if tmpSign < 0:
                    minusCountOut += 1
                elif tmpSign > 0:
                    plusCountOut += 1
                else:
                    tmSign = self.graph.get_edge_data(neighbor1,author1,default={'weight': 0})
                    tmpSign = tmSign['weight']
                    if tmpSign < 0:
                        minusCountIn += 1
                    elif tmpSign > 0:
                        plusCountIn += 1

        commonNeigh = sorted(nx.common_neighbors(unG,author1,author2))
        for inode in commonNeigh:
            self.computeTriads(inode,author1,author2,triadList)

        commonNeighbors = len(commonNeigh)
        #Write to file
        text1 = str(plusCountIn) + "\t" + str(minusCountIn) + "\t" + str(plusCountOut) + "\t" + str(minusCountOut) + "\t"
        text2 = str(rplusCountIn) + "\t" + str(rminusCountIn) + "\t" + str(rplusCountOut) + "\t" + str(rminusCountOut) + "\t"
        final = text1 + text2 + str(commonNeighbors)
        for item in triadList:
            final += "\t" + str(item)

        f.write(final+"\n")


    def computeDegreeDistribution(self):
        degreeList = []
        for node in nx.nodes(self.graph):
            degreeList.append(self.graph.out_degree(node)+self.graph.in_degree(node))
        degreeList.sort(reverse=True)

        degreeDict = {}
        for degree in degreeList:
            if degree in degreeDict:
                degreeDict[degree] += 1
            else:
                degreeDict[degree] = 1

        sorted_x = sorted(degreeDict.items(), key=operator.itemgetter(0))
        a = dict(sorted_x)
        self.discretePlot(a)


    def discretePlot(self,degrees):
        discxplot = []
        discyplot = []
        for key, value in degrees.items():
            discxplot.append(key)
            discyplot.append(value)

        minObs = min(discyplot)
        n = len(discyplot)
        summerTime = 0
        for i in discyplot:
            x = i/(1.0*minObs)
            summerTime += math.log(x)

        for i in range(0,len(discxplot)):
            discxplot[i] = math.log(discxplot[i])
            discyplot[i] = math.log(discyplot[i])

        a = 1 + (n / summerTime)

        print "Simple distribution power law exponent a is: " + str(a)
        P.xlabel('Degree')
        P.ylabel('Observations')
        P.title('Discrete plot')
        P.plot(discxplot, discyplot, 'r-')
        P.show()

    def computeTriads(self, commonNeighbor, node1, node2, triadList):
        tmSign = self.graph.get_edge_data(node1,commonNeighbor,default={'weight':0})
        tmpSign = tmSign['weight']
        if tmpSign < 0:
            #Fm
            tmSign = self.graph.get_edge_data(node2,commonNeighbor,default={'weight':0})
            tmpSign = tmSign['weight']
            if tmpSign < 0:
                #FBmm
                triadList[7] += 1
            elif tmpSign > 0:
                #FBmp
                triadList[6] += 1
            else:
                tmSign = self.graph.get_edge_data(commonNeighbor,node2,default={'weight':0})
                tmpSign = tmSign['weight']
                if tmpSign < 0:
                    #FFmm
                    triadList[3] += 1
                elif tmpSign > 0:
                    #FFmp
                    triadList[2] += 1
        elif tmpSign > 0:
            #Fp
            tmSign = self.graph.get_edge_data(node2,commonNeighbor,default={'weight':0})
            tmpSign = tmSign['weight']
            #print "Sign:" + str(tmpSign)
            if tmpSign < 0:
                #FBpm
                triadList[5] += 1
            elif tmpSign > 0:
                #FBpp
                triadList[4] += 1
            else:
                tmSign = self.graph.get_edge_data(commonNeighbor,node2,default={'weight':0})
                tmpSign = tmSign['weight']
                if tmpSign < 0:
                    #FFpm
                    triadList[1] += 1
                elif tmpSign > 0:
                    #FFpp
                    triadList[0] += 1
        else:
            tmSign = self.graph.get_edge_data(commonNeighbor,node1,default={'weight':0})
            tmpSign = tmSign['weight']
            if tmpSign < 0:
                #Bm
                tmSign = self.graph.get_edge_data(node2,commonNeighbor,default={'weight':0})
                tmpSign = tmSign['weight']
                if tmpSign < 0:
                    #BBmm
                    triadList[15] += 1
                elif tmpSign > 0:
                    #BBmp
                    triadList[14] += 1
                else:
                    tmSign = self.graph.get_edge_data(commonNeighbor,node2,default={'weight':0})
                    tmpSign = tmSign['weight']
                    if tmpSign < 0:
                        #BFmm
                        triadList[11] += 1
                    elif tmpSign > 0:
                        #BFmp
                        triadList[10] += 1
            elif tmpSign > 0:
                #Bp
                tmSign = self.graph.get_edge_data(node2,commonNeighbor,default={'weight':0})
                tmpSign = tmSign['weight']
                if tmpSign < 0:
                    #BBpm
                    triadList[13] += 1
                elif tmpSign > 0:
                    #BBpp
                    triadList[12] += 1
                else:
                    tmSign = self.graph.get_edge_data(commonNeighbor,node2,default={'weight':0})
                    tmpSign = tmSign['weight']
                    if tmpSign < 0:
                        #BFpm
                        triadList[9] += 1
                    elif tmpSign > 0:
                        #BFpp
                        triadList[8] += 1




