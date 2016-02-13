from abc import ABCMeta, abstractmethod


class Topic:
    __metaclass__ = ABCMeta
    _comments = []
    _authors = {}
    _commentIds = {}
    _name = ""

    @abstractmethod
    def getComments(self): pass

    @abstractmethod
    def setComments(self): pass

    @abstractmethod
    def toString(self): pass

    @abstractmethod
    def addComment(self): pass

    @abstractmethod
    def setName(self,name): pass

    @abstractmethod
    def getName(self): pass


    @abstractmethod
    def getAuthors(self): pass

    @abstractmethod
    def setAuthors(self): pass

    @abstractmethod
    def getCommentFromId(self,pid): pass

    @abstractmethod
    def setCommentFromId(self): pass

    @abstractmethod
    def clearAuthors(self): pass