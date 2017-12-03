from task import Task
from functools import reduce

class TaskSet:
    def __init__(self, task_set=[]):
        self._task_set = task_set

    def getTaskSet(self):
        return self._task_set

    def addTask(self, task):
        self._task_set.append(task)

    def findFeasibilityInterval(self):
        O_max = 0
        P = self.computeP()
        for task in self.getTaskSet():
            if(task.getOffset() > O_max):
                O_max = task.getOffset()
        return [O_max, O_max + 2 * P]

    def GCD(self, a, b):
        """
        :param a:
        :param b:
        :return: greatest common divisor of a and b
        """
        if b == 0:
            return a
        else:
            return self.GCD(b, a % b)

    def lcm(self, a,b):
        """
        :param a:
        :param b:
        :return: least common multiple of a and b
        """
        return a*b//self.GCD(a,b)

    def lcmArray(self,args):
        """
        :param args: list of int
        :return: return the least common multiple of all values in args list
        """
        return reduce(self.lcm, args)

    def computeP(self):
        all_period = []
        for task in self.getTaskSet():
            all_period.append(task.getPeriod())
        return self.lcmArray(all_period)