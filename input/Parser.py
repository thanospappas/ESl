from datastructure.TopicFactory import TopicFactory
from datastructure.Comment import Comment
from datastructure.Topic import Topic
from datastructure.TopTopic import TopTopic
import json
import os
from pprint import pprint

class Parser:
    filePath = ""
    topics = []

    def __init__(self, filePath):
        self.filePath = filePath

    def parseFiles(self):
        """for dirname, dirnames, filenames in os.walk("/home/thanos/PycharmProjects/ESl/reddit/"):
            for subdirname in dirnames:
                print(os.path.join(dirname, subdirname))
            for filename in filenames:
                filepath = os.path.join(dirname, filename)
                #print(filepath)
                self.parseSingleFile(filepath)"""

        for dirname, dirnames, filenames in os.walk(self.filePath):
            filepaths = []
            for subdirname in dirnames:
                os.path.join(dirname, subdirname)

            for filename in filenames:
                filepath = os.path.join(dirname, filename)
                #Dont read temp files...
                if "~" not in filepath:
                    filepaths.append(filepath)

            self.parseJSONFiles(filepaths)


    def parseSingleFile(self,fileName):
        f = open(fileName, 'r')
        if(".txt" not in fileName):
            return
        f1 = open(fileName.replace(".txt","") + '.json','w')
        f1.write("{\"data\":[")
        prevLine = ""
        for x in f:
            if x.split(":")[0] == "submission": #if first line has submission info
                continue
            info = x.split("\",\"",1)
            comment = Comment()
            body = info[0].replace("{\"body\":\"","")
            body = body.replace("\\","")
            comment.setBody(body.replace("\"",""))
            if not prevLine is "":
                f1.write(prevLine + ",")
            #f1.write("{\"body\":\"" + ' '.join(comment.getBody().split()) + "\",\"")
            if len(info) < 2:
                continue
            prevLine = "{\"body\":\"" + ' '.join(comment.getBody().split()) + "\",\"" + info[1]
            #f1.write(info[1] + ",")
            #comment.setScore(int(info[3]))"""
        f1.write(prevLine)
        f1.write("]}")
        f1.close()

    """
        Print function for debug purposes
    """
    def printTopic(self, topic):
        comments = topic.getComments()
        for comment in comments:
            print "Depth: " + str(comment.getDepth()) + ",",
            print "Score: " + str(comment.getScore()) + ",",
            print "Author: " + comment.getAuthor() + ",",
            print "Ups: " + str(comment.getUps()) + ",",
            print "Downs: " + str(comment.getDowns()) + ",",
            print "Contrversiality: " + str(comment.getControversiality()) + ",",
            print "Gilded: " + str(comment.getGilded()) + ",",
            print "Name: " + comment.getName() + ",",
            print "Subreddit: " + comment.getSubreddit() + ",",
            print "SubreditId: " + comment.getSubredditId() + ",",
            print "CreatedAt: " + str(comment.getCreatedAt()) + ",",
            print "CreatedUTC: " + str(comment.getCreatedUTC()) + ",",
            print "ParentId: " + comment.getParentId() + ","

    def parseJSONFiles(self,fileNames):
        topicType = None
        topicName = ""
        if len(fileNames) == 0:
            return

        fact = TopicFactory()

        if "controversial" in fileNames[0]:
            splittedName = fileNames[0].split("top_")
            topicName = splittedName[1].split("_")[0]
            topicType = fact.factory("controvertial")
        else:
            splittedName = fileNames[0].split("top_")
            topicName = splittedName[1].split("_")[0]
            topicType = fact.factory("top")

        topicType.clearAuthors()
        topicType.setName(topicName)

        for fileName in fileNames:
            with open(fileName) as data_file:
                data = json.load(data_file)

            list1 = data['data']
            if len(list1) == 0:
                print "File: " + str(fileName) + " is empty!"
                continue

            for comment in list1:
                userComment = Comment()
                if "[deleted]" in comment['body'] or "None" in comment['author']:
                    continue #comment was deleted: skip it

                userComment.setBody(comment['body'])
                userComment.setDepth(int(comment['depth']))
                userComment.setScore(int(comment['score']))
                userComment.setAuthor(comment['author'])
                userComment.setUps(int(comment['ups']))
                userComment.setDowns(int(comment['downs']))
                userComment.setControversiality(comment['controversiality'])
                userComment.setGilded(comment['gilded'])
                userComment.setName(comment['name'])
                userComment.setSubreddit(comment['subreddit'])
                userComment.setSubredditId(comment['subreddit_id'])
                userComment.setCreatedAt(int(comment['created']))
                userComment.setCreatedUTC(int(comment['created_utc']))
                userComment.setParentId(comment['parent_id'])

                topicType.addComment(userComment)

        topicType.setAuthors()
        topicType.setCommentFromId()
        self.topics.append(topicType)

    def getTopics(self):
        return self.topics

