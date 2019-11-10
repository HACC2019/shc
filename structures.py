class Meter:
    def __init__(self, name):
        self.problems = []
        self.name = name
        self.status = 0


class Problem:
    def __init__(self, starttime, endtime):
        self.problemName = None
        self.color = None
        self.problemStart = starttime
        self.problemEnd = endtime
