from Topic import Topic

class ControvertialTopic(Topic):

    def __init__(self):
        self._comments = []

    def getComments(self):
        return self._comments

    def setComments(self):
        pass

    def addComment(self,comment):
        self._comments.append(comment)

    def getName(self):
        return self._name

    def setName(self,name):
        self._name = name

    def toString(self):
        return "Controvertial"

    def getAuthors(self):
        return self._authors

    def setAuthors(self):
        for comment in self._comments:
            if comment.getAuthor() in self._authors:
                list1 = self._authors[comment.getAuthor()]
                list1.append(comment)
                self._authors[comment.getAuthor()] = list1
            else:
                list1 = []
                list1.append(comment)
                self._authors[comment.getAuthor()] = list1

    def setCommentFromId(self):
        for comment in self._comments:
            if comment.getName() not in self._commentIds:
                self._commentIds[comment.getName()] = comment

    def getCommentFromId(self, pid):
        try:
            return self._commentIds[pid]
        except Exception, e:
            return -1


    def clearAuthors(self):
        self._authors = {}