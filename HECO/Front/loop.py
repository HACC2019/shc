from .backend import find_problems, findDailyPercentage
import time

def loop():

    while True:
        findDailyPercentage(1535768703, 'A')
        find_problems()
        time.sleep(60 * 5)