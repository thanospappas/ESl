from input.Parser import Parser
from datastructure.GraphModel import GraphModel
import networkx as nx
from predictor.Predictor import Predictor
from restdataset.GraphCreator import GraphCreator

densityFactor = 1
threshold = 1
epsilon = 0.2
def printMenu():
    print "-------------------------------------"
    print "               ESl Menu              "
    print "-------------------------------------"
    print "Choose:"
    print "1. Load Reddit Json Files"
    print "2. Create Reddit Graph"
    print "3. Create Wikipedia, Slashdot & Epinions Graphs"
    print "4. Use Logistic Regression"
    print "5. Exit"
    try:
        reply = int(raw_input('Answer:'))
    except ValueError:
        print "Not a number"

    return reply

def main():
    parser = None
    while True:
        reply = printMenu()

        if reply == 1:
            parser = Parser("/home/thanos/PycharmProjects/ESl/reddit_new/")
            parser.parseFiles()
        elif reply == 2:
            if parser is None:
                print "Error!!! You have to load the json files first!"
                continue
            print "-----------------------\nChoose Graph Type:"
            print "1. All Topics"
            print "2. Top Topics"
            print "3. Controversial Topics"
            print "-----------------------"
            try:
                replyTopic = int(raw_input('Answer:'))
            except ValueError:
                print "Not a number"
            topics = parser.getTopics()
            selectedTopics = []
            if replyTopic == 1:
                for topic in topics:
                        selectedTopics.append(topic)
            elif replyTopic == 2:
                for topic in topics:
                    if "TopTopic" in str(type(topic)):#"science" in topic.getName():#"ControvertialTopic" in str(type(topic)):
                        selectedTopics.append(topic)
            elif replyTopic == 3:
                for topic in topics:
                    if "ControvertialTopic" in str(type(topic)):#"science" in topic.getName():#"ControvertialTopic" in str(type(topic)):
                        selectedTopics.append(topic)
            outputFilename = str(raw_input('Output File Name:'))#science
            outputFilepath = str(raw_input('Output File Path:'))#/home/thanos/graphs/
            epsilon = float(raw_input('Epsilon:'))

            graphModel = GraphModel(densityFactor, selectedTopics, threshold, epsilon, outputFilename,outputFilepath)
            graphModel.generateGraph()
            G = graphModel.getGraph()
            gfinal = nx.DiGraph()
            gfinal.add_edges_from(G.edges())
            print str(nx.density(gfinal))

        elif reply == 3:
            inputEpinions = str(raw_input('Input Epinions:'))#/home/thanos/PycharmProjects/ESl/datasets/soc-sign-epinions.txt
            inputSlashdot = str(raw_input('Input Slashdot:'))#/home/thanos/PycharmProjects/ESl/datasets/soc-sign-Slashdot090221.txt
            inputWiki = str(raw_input('Input Wiki:'))#/home/thanos/PycharmProjects/ESl/datasets/rfa_all.NL-SEPARATED.txt
            gCreator = GraphCreator()
            gCreator.readEpinions(inputEpinions)
            gCreator.readSlashDot(inputSlashdot)
            gCreator.readWiki(inputWiki)
            gCreator.computeAll()

        elif reply == 4:
            p = Predictor("/home/thanos/graphs/epinions")
            p.readData(True)
            p.train()
            p.predict()
            p.calculateStability()
        elif reply == 5:
            break

if __name__ == '__main__':     # if the function is the main function ...
    main()# ...call it




