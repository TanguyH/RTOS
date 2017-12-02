from task import Task

class TaskSet:
    def __init__(self, task_set=[]):
        self._task_set = task_set

    def getTaskSet(self):
        return self._task_set

    def addTask(self, task):
        self._task_set.append(task)

    def findFeasibilityInterval(self):
        O_max = 0
        P_max = 0
        for task in self.getTaskSet():
            if(task.getOffset() > O_max):
                O_max = task.getOffset()
            if(task.getPeriod() > P_max):
                P_max = task.getPeriod()
        return [O_max, O_max + 2 * P_max]
