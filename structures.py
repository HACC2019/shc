class Meter:
    def __init__(self, name):
        self.problems = []
        self.name = name
        self.status = 0


class Problem:
    def __init__(self, starttime, endtime):
        self.problemName = None
        self.color = None


class ProblemUsageDrop(Problem):
    def __init__(self, starttime, endtime):
        super().__init__(starttime, endtime)
        self.problemName = "Usage Drop"
        self.color = 0xFF0000


class ProblemCongestion(Problem):
    def __init__(self, starttime, endtime):
        super().__init__(starttime, endtime)
        self.problemName = "Congestion"
        self.color = 0xFFFF00
