class Meter:
    def __init__(self, name):
        self.problems = []
        self.name = name
        self.status = 0


class Problem:
    def __init__(self, starttime, endtime, name, color, desc):
        self.problemName = name
        self.color = color
        self.problemStart = starttime
        self.problemEnd = endtime
        self.problemDesc = desc
