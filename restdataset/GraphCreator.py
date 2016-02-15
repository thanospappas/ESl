import networkx as nx
class GraphCreator:

    epinionsGraph = None
    slashdotGraph = None
    wikiGraph = None

    def __init__(self):
         self.epinionsGraph = nx.DiGraph()
         self.slashdotGraph = nx.DiGraph()
         self.wikiGraph = nx.DiGraph()

    def readSlashDot(self,fileName):
        f = open(fileName,'r')
        for line in f:
            if "#" in line:
                continue
            splittedLine = line.split("\t")
            self.slashdotGraph.add_node(int(splittedLine[0]))
            self.slashdotGraph.add_node(int(splittedLine[1]))
            self.slashdotGraph.add_edge(int(splittedLine[0]),int(splittedLine[1]),weight = int(splittedLine[2]))

        f.close()

    def readEpinions(self, fileName):
        f = open(fileName,'r')
        for line in f:
            if "#" in line:
                continue
            splittedLine = line.split("\t")
            self.epinionsGraph.add_node(int(splittedLine[0]))
            self.epinionsGraph.add_node(int(splittedLine[1]))
            self.epinionsGraph.add_edge(int(splittedLine[0]),int(splittedLine[1]),weight = int(splittedLine[2]))

        f.close()

    def readWiki(self,fileName):
        f = open(fileName,'r')
        i = 0
        authorToInt = {}
        num = 0
        source = -1
        target = -1
        for line in f:
            if len(line) < 2:
                source = -1
                target = -1
                i=0
                continue
            value = line.split(":")[1]
            i +=1

            if i == 1:
                if value not in authorToInt:
                    authorToInt[value] = num
                    num += 1
                self.wikiGraph.add_node(authorToInt[value])
                source = authorToInt[value]

            elif i == 2:
                if value not in authorToInt:
                    authorToInt[value] = num
                    num +=1
                self.wikiGraph.add_node(authorToInt[value])
                target = authorToInt[value]

            elif i == 3:
                self.wikiGraph.add_edge(source,target,weight = int(value))
            elif i == 8:
                source = -1
                target = -1
                i=0

    def computeTriads(self, commonNeighbor, node1, node2, triadList,graph):
        tmSign = graph.get_edge_data(node1,commonNeighbor,default={'weight':0})
        tmpSign = tmSign['weight']
        if tmpSign < 0:
            #Fm
            tmSign = graph.get_edge_data(node2,commonNeighbor,default={'weight':0})
            tmpSign = tmSign['weight']
            if tmpSign < 0:
                #FBmm
                triadList[7] += 1
            elif tmpSign > 0:
                #FBmp
                triadList[6] += 1
            else:
                tmSign = graph.get_edge_data(commonNeighbor,node2,default={'weight':0})
                tmpSign = tmSign['weight']
                if tmpSign < 0:
                    #FFmm
                    triadList[3] += 1
                elif tmpSign > 0:
                    #FFmp
                    triadList[2] += 1
        elif tmpSign > 0:
            #Fp
            tmSign = graph.get_edge_data(node2,commonNeighbor,default={'weight':0})
            tmpSign = tmSign['weight']
            #print "Sign:" + str(tmpSign)
            if tmpSign < 0:
                #FBpm
                triadList[5] += 1
            elif tmpSign > 0:
                #FBpp
                triadList[4] += 1
            else:
                tmSign = graph.get_edge_data(commonNeighbor,node2,default={'weight':0})
                tmpSign = tmSign['weight']
                if tmpSign < 0:
                    #FFpm
                    triadList[1] += 1
                elif tmpSign > 0:
                    #FFpp
                    triadList[0] += 1
        else:
            tmSign = graph.get_edge_data(commonNeighbor,node1,default={'weight':0})
            tmpSign = tmSign['weight']
            if tmpSign < 0:
                #Bm
                tmSign = graph.get_edge_data(node2,commonNeighbor,default={'weight':0})
                tmpSign = tmSign['weight']
                if tmpSign < 0:
                    #BBmm
                    triadList[15] += 1
                elif tmpSign > 0:
                    #BBmp
                    triadList[14] += 1
                else:
                    tmSign = graph.get_edge_data(commonNeighbor,node2,default={'weight':0})
                    tmpSign = tmSign['weight']
                    if tmpSign < 0:
                        #BFmm
                        triadList[11] += 1
                    elif tmpSign > 0:
                        #BFmp
                        triadList[10] += 1
            elif tmpSign > 0:
                #Bp
                tmSign = graph.get_edge_data(node2,commonNeighbor,default={'weight':0})
                tmpSign = tmSign['weight']
                if tmpSign < 0:
                    #BBpm
                    triadList[13] += 1
                elif tmpSign > 0:
                    #BBpp
                    triadList[12] += 1
                else:
                    tmSign = graph.get_edge_data(commonNeighbor,node2,default={'weight':0})
                    tmpSign = tmSign['weight']
                    if tmpSign < 0:
                        #BFpm
                        triadList[9] += 1
                    elif tmpSign > 0:
                        #BFpp
                        triadList[8] += 1
        #print "IN: " + str(triadList)

    def computeFeatures(self,graph,graphFileName):
        f = open(graphFileName,'w')
        first = "Author1\tAuthor2\tSign\tIn+1\tIn-1\tOut+1\tOut-1\tIn+2\tIn-2\tOut+2\tOut-2\tCommonNeighbors\t"
        second = "FFpp\tFFpm\tFFmp\tFFmm\tFBpp\tFBpm\tFBmp\tFBmm\tBFpp\tBFpm\tBFmp\tBFmm\tBBpp\tBBpm\tBBmp\tBBmm\n"
        firstLine = first + second
        f.write(firstLine)


        edges = nx.edges(graph)
        unG = graph.to_undirected(reciprocal=False)
        for edge in edges:#pair, score in self.authorPairScore.iteritems():
            test1 = edge[0]
            test2 = edge[1]
            if test1 == test2:
                continue
            sign = graph.get_edge_data(test1,test2)
            f.write(str(test1) + "\t" + str(test2) + "\t" + str(sign['weight']) + "\t")

            neighbors1 = nx.all_neighbors(graph,test1)#self.graph.neighbors(test1)
            neighbors2 = nx.all_neighbors(graph,test2)#self.graph.neighbors(test2)

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
                    pn = str(test2) + "," + str(neighbor2)
                    if pn not in nodesSeen:
                        nodesSeen[pn] = 1
                        tmSign = graph.get_edge_data(test2,neighbor2,default={'weight':0})
                        tmpSign = tmSign['weight']
                        if tmpSign < 0:
                            rminusCountOut += 1
                        elif tmpSign > 0:
                            rplusCountOut += 1
                        else:
                            tmSign = graph.get_edge_data(neighbor2,test2,default={'weight':0})
                            tmpSign = tmSign['weight']
                            if tmpSign < 0:
                                rminusCountIn += 1
                            elif tmpSign > 0:
                                rplusCountIn += 1

                pn1 = str(test1) + "," + str(neighbor1)
                if pn1 not in nodesSeen:
                    nodesSeen[pn1] = 1
                    tmSign = graph.get_edge_data(test1,neighbor1,default={'weight':0})
                    tmpSign = tmSign['weight']
                    if tmpSign < 0:
                        minusCountOut += 1
                    elif tmpSign > 0:
                        plusCountOut += 1
                    else:
                        tmSign = graph.get_edge_data(neighbor1,test1,default={'weight':0})
                        tmpSign = tmSign['weight']
                        if tmpSign < 0:
                            minusCountIn += 1
                        elif tmpSign > 0:
                            plusCountIn += 1
            commonNeigh = sorted(nx.common_neighbors(unG,test1,test2))
            for inode in commonNeigh:
                self.computeTriads(inode,test1,test2,triadList,graph)

            commonNeighbors = len(commonNeigh)

            text1 = str(plusCountIn) + "\t" + str(minusCountIn) + "\t" + str(plusCountOut) + "\t" + str(minusCountOut) + "\t"
            text2 = str(rplusCountIn) + "\t" + str(rminusCountIn) + "\t" + str(rplusCountOut) + "\t" + str(rminusCountOut) + "\t"
            final = text1 + text2 + str(commonNeighbors)
            for item in triadList:
                final += "\t" + str(item)

            f.write(final+"\n")
        f.close()

    def writeSlashDot(self):
        pass

    def writeEpinions(self):
        pass

    def writeWiki(self):
        pass
