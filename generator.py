from additional import getRandValue
from random import randint
from task import Task

class Generator:
    def __init__(self, nb_tasks, util_factor, filename):
        self._nb_tasks = int(nb_tasks)
        self._util_factor = float(util_factor)/100
        self._filename = filename
        self._tasks = []
        self._eps_util = 0.003


    def getNbTasks(self):
        return self._nb_tasks

    def getUtilFactor(self):
        return self._util_factor

    def getFileName(self):
        return self._filename

    def getTasks(self):
        return self._tasks

    def getEpsUtil(self):
        return self._eps_util

    def createTasks(self, periods, worst_cases, offsets, deadlines):
        for i in range (self.getNbTasks()):
            new_task = Task(offsets[i], periods[i], deadlines[i], worst_cases[i], i)
            self._tasks.append(new_task)

    def createPeriods(self):
        periods = []
        lcm = getRandValue(2,30)  # To get randomly P :  A*B=LCM(A,B)*GCD(A,B)
        gcd = getRandValue(2,lcm)  # Thus A and B can be the LCM and GCD values   -   (gcd must be lower than lcm)
        #Start the random generation to 2, to get at least 20 for a period, and then have a WCET of 10
        for i in range (self.getNbTasks()):    #init the periods list for tasks
            if (i%2 == 0):
                periods.append(lcm)
            else:
                periods.append(gcd)
        return periods



    def createWorstCases(self, periods):
        worst_cases = []
        valid_utilization = False
        while (not valid_utilization):
            for i in range(self.getNbTasks()):
                worst_cases.append(getRandValue(1, (periods[i]/10)//2))
            gen_util = 0

            for i in range(self.getNbTasks()):  # Check processor utilization
                gen_util += worst_cases[i] / periods[i]
            print(gen_util)
            valid_utilization = self.checkUtilization(gen_util)
            if (not valid_utilization):
                worst_cases.clear()
        print("Good WCET found : utilization check")
        return worst_cases

    def checkUtilization(self,gen_util):
        valid_utilization = False
        if (self.getUtilFactor()+self.getEpsUtil() >1):
            if (gen_util <= 1 and gen_util>= self.getUtilFactor() - self.getEpsUtil()):
                valid_utilization = True
        else:
            if (gen_util <= self.getUtilFactor() + self.getEpsUtil() and gen_util>= self.getUtilFactor() - self.getEpsUtil()):
                valid_utilization = True
        return valid_utilization

    def createOffsets(self):
        offsets = []
        not_nul_offset = randint(0,self.getNbTasks())   #To be sure to have at least 1 non nul offset in the taskset
        for i in range (self.getNbTasks()):
            if (i != not_nul_offset):
                offsets.append(getRandValue(0,50))
            else:
                offsets.append(getRandValue(1,50))

        return offsets

    def createDeadLines(self, periods):
        deadlines = []
        for i in range (self.getNbTasks()):
            deadlines.append(getRandValue(1,periods[i]/10))     #Deadlines cannot be larger than periods
        return deadlines


    def generateSystem(self):
        print("generate periods")
        periods = self.createPeriods()
        print("generate worst cases")
        worst_cases = self.createWorstCases(periods)
        offsets = self.createOffsets()
        deadlines = self.createDeadLines(periods)
        self.createTasks(periods,worst_cases,offsets,deadlines)

    def generateFile(self):
        lines = []
        with open(self.getFileName(), 'w') as f:
            for task in self.getTasks():
                lines.append(str(task.getOffset())+" "+str(task.getPeriod())+" "+str(task.getDeadline())+" "+str(task.getWCET()))
            f.write('\n'.join(lines))
