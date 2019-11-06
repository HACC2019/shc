class Meter:
    def __init__(self, name):
        self.problems = []
        self.name = name
        self.status = 0


class Problem:
    def __init__(self, time, session):
        self.problemName = None
        self.color = None


class ProblemUsageDrop(Problem):
    def __init__(self):
        super().__init__()
        self.problemName = "Usage Drop"
        self.color = 0xFF0000
