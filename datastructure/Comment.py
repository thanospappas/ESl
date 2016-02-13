class Comment:
    body = ""
    depth = -1
    score = 0
    ups = 0
    downs = 0
    controversiality = 0
    gilded = 0
    author = -1
    name = ""
    subreddit = ""
    subredditId = -1
    createdAt = -1
    createdUTC = ""
    paretntId = -1

    def setBody(self,body):
        self.body = body

    def setDepth(self,depth):
        self.depth = depth

    def setScore(self,score):
        self.score = score

    def getBody(self):
        return self.body

    def getDepth(self):
        return self.depth

    def getScore(self):
        return self.score

    def setUps(self, ups):
        self.ups = ups

    def getUps(self):
        return self.ups

    def setDowns(self,downs):
        self.downs = downs

    def getDowns(self):
        return self.downs

    def setControversiality(self,contr):
        self.controversiality = contr

    def getControversiality(self):
        return self.controversiality

    def setGilded(self,gilded):
        self.gilded = gilded

    def getGilded(self):
        return self.gilded

    def setAuthor(self,author):
        self.author = author

    def getAuthor(self):
        return self.author

    def setName(self,name):
        self.name = name

    def getName(self):
        return self.name

    def setSubreddit(self,subr):
        self.subreddit = subr

    def getSubreddit(self):
        return self.subreddit

    def setSubredditId(self,id):
        self.subredditId = id

    def getSubredditId(self):
        return self.subredditId

    def setCreatedAt(self,created):
        self.createdAt = created

    def getCreatedAt(self):
        return self.createdAt

    def setCreatedUTC(self,created):
        self.createdUTC = created

    def getCreatedUTC(self):
        return self.createdUTC

    def setParentId(self,id):
        self.paretntId = id

    def getParentId(self):
        return self.paretntId