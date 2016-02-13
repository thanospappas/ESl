class Features:
    avgCommentOverall = 0
    avgComment12 = 0
    avgScoreOverall = 0
    avgScore12 = 0

    def setEdgeFeatures(self, avgComment12, avgScore12):
        self.avgComment12 = avgComment12
        self.avgScore12 = avgScore12

    def setOverall(self,avgCommentOverall,avgScoreOverall):
        self.avgCommentOverall = avgCommentOverall
        self.avgScoreOverall = avgScoreOverall

    def masterGetter(self):
        text = str(self.avgCommentOverall) + "\t" + str(self.avgComment12) + "\t" + str(self.avgScoreOverall) + "\t" + str(self.avgScore12)
        return text

    def getAvgComment12(self):
        return self.avgComment12

    def getAvgScore12(self):
        return self.avgScore12