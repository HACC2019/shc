class Meter:
    def __init__(self):
        self.problems = []
        self.status = 0


class Problem:
    def __init__(self):
        self.problemName = None
        self.color = None


class ProblemUsageDrop(Problem):
    def __init__(self):
        super().__init__()
        self.problemName = "Usage Drop"
        self.color = 0xFF0000
