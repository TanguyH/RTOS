from copy import *
from task import Task
from functools import reduce
from additional import *

class TaskSet:
    def __init__(self, source_file=None):
        self._tasks = []
        self._original_tasks = []
        self._arrivals = []
        self._deadlines = []
        self._misses = []
        self._schedule = []
        self._schedule_block = 0
        self._schedule_queue = []

        if(source_file != None):
            self.loadTasks(source_file)

    def getTasks(self, i=None):
        if(i != None):
            return self._tasks[i]
        return self._tasks

    def getOriginalTasks(self):
        return self._original_tasks

    def removeTask(self, task):
        self.getTasks().remove(task)

    def setTasks(self, task_set):
        self._tasks = task_set

    def setOriginalTasks(self, o_task_set):
        self._original_tasks = deepcopy(o_task_set)

    def getNumberOfTasks(self):
        return len(self.getTasks())

    def getTasksWCET(self):
        task_WCET = []
        for task in self.getTasks():
            task_WCET.append(task.getWCET())
        return task_WCET

    def getTasksDeadlines(self):
        task_deadlines = []
        for task in self.getTasks():
            task_deadlines.append(task.getDeadline())
        return task_deadlines

    def getTasksPeriods(self):
        task_periods = []
        for task in self.getTasks():
            task_periods.append(task.getPeriod())
        return task_periods

    def addTask(self, task):
        self._tasks.append(task)

    def loadTasks(self, source_file):
        """
        Method who will analyze a given .txt file to get all information about the task set
        """
        source_file = open(source_file, "r")
        taskset = TaskSet()
        task_count = 1
        for line in source_file:
            offset, period, deadline, WCET = line.split(" ")
            task = Task(int(offset), int(period), int(deadline), int(WCET), task_count)
            taskset.addTask(task)
            task_count += 1
        self.setTasks(taskset.getTasks())
        self.setOriginalTasks(taskset.getTasks())

    def findFeasibilityInterval(self):
        O_max = 0
        P = self.computeP()
        for task in self.getTasks():
            if(task.getOffset() > O_max):
                O_max = task.getOffset()
        return [O_max, O_max + 2 * P]

    def computeP(self):
        all_period = []
        for task in self.getTasks():
            all_period.append(task.getPeriod())
        return self.lcmArray(all_period)
