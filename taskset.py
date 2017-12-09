from task import Task
from functools import reduce

class TaskSet:
    def __init__(self, source_file=None):
        self._task_set = []
        self._arrivals = []
        self._deadlines = []
        self._misses = []
        self._schedule = []
        self._schedule_block = 0
        self._schedule_queue = []

        if(source_file != None):
            self.loadTaskSet(source_file)

    def getTaskSet(self):
        return self._task_set

    def setTaskSet(self, task_set):
        self._task_set = task_set

    def getSchedule(self, i = None):
        if(i != None):
            return self._schedule[i]
        return self._schedule

    def setSchedule(self, i, task_number):
        self._schedule[i] = task_number

    def getScheduleBlockSize(self):
        return self._schedule_block

    def getNumberOfTasks(self):
        return len(self.getTaskSet())

    def getTaskSetWCET(self):
        task_WCET = []
        for task in self.getTaskSet():
            task_WCET.append(task.getWCET())
        return task_WCET

    def getTaskSetDeadlines(self):
        task_deadlines = []
        for task in self.getTaskSet():
            task_deadlines.append(task.getDeadline())
        return task_deadlines

    def getTaskSetPeriods(self):
        task_periods = []
        for task in self.getTaskSet():
            task_periods.append(task.getPeriod())
        return task_periods

    def getRelease(self, i):
        return self._arrivals[i]

    def setRelease(self, i, task_job):
        self._arrivals[i].append(task_job)

    def getDeadline(self, i):
        return self._deadlines[i]

    def getDeadlines(self):
        return self._deadlines

    def setDeadline(self, i, task_job):
        self._deadlines[i].append(task_job)

    def getMiss(self, i):
        return self._misses[i]

    def getMisses(self):
        return self._misses

    def flagDeadlineMiss(self, i, task_job):
        self._misses[i].append(task_job)

    def addTask(self, task):
        self._task_set.append(task)

    def loadTaskSet(self, source_file):
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
        self.setTaskSet(taskset.getTaskSet())

    def findFeasibilityInterval(self):
        O_max = 0
        P = self.computeP()
        for task in self.getTaskSet():
            if(task.getOffset() > O_max):
                O_max = task.getOffset()
        return [O_max, O_max + 2 * P]

    # not sure if working
    def checkForMisses(self, task_number):
        miss = False
        for slot in self.getMisses():
            for task_job in slot:
                if task_job[0] == task_number:
                    miss = True
        return miss

    def scheduleRelease(self, task_job, time):
        block = time // self.getScheduleBlockSize()
        self.setRelease(block, task_job)

    def scheduleTask(self, task, job, time):

        max_range = task.getPeriod() // self.getScheduleBlockSize()
        blocks_to_fit = task.getWCET() // self.getScheduleBlockSize()

        starting_point = time // self.getScheduleBlockSize()
        end_point = min(starting_point + max_range, len(self.getSchedule()))

        for block in range(starting_point, end_point):
            if(self.getSchedule(block) == [None,None] and blocks_to_fit > 0):
                self.setSchedule(block, [task.getTaskNumber(), job])
                blocks_to_fit -= 1

        if(blocks_to_fit > 0):
            self.flagDeadlineMiss(block, [task.getTaskNumber(), job])
            # reschedule task for later ? -> yes if deadlines SOFT !!

    def assignTasksToSlots(self, lowest_priority=None):
        # sort by priority
        priorities = {}
        for task_time in self._schedule_queue:
            task_no = task_time[0].getTaskNumber()
            if(task_no in priorities.keys()):
                priorities[task_no].append(task_time)
            else:
                priorities[task_no] = [task_time]

        # no lowest priority = schedule in implicit priority
        if(lowest_priority == None):
            for priority in priorities.keys():
                for task_time in priorities[priority]:
                    self.scheduleTask(task_time[0], task_time[1], task_time[2])

        # priority = schedule others first, then prior
        else:
            for priority in priorities.keys():
                if priority != lowest_priority:
                    for task_time in priorities[priority]:
                        self.scheduleTask(task_time[0], task_time[1], task_time[2])

            if(lowest_priority in priorities.keys()):
                for task_time in priorities[priority]:
                    self.scheduleTask(task_time[0], task_time[1], task_time[2])

    def scheduleDealine(self, task_job, time):
        block = time // self.getScheduleBlockSize()
        if(block < len(self.getDeadlines())):
            self.setDeadline(block, task_job)

    def checkForTaskRelease(self, time):
        for task in self.getTaskSet():
            if(time % task.getPeriod() == task.getOffset()):
                task_job = task.releaseJob(time)
                self.scheduleRelease(task_job, time)
                self._schedule_queue.append((task, task_job[1], time))

    def checkForTaskDeadline(self, time):
        for task in self.getTaskSet():
            if(time % task.getDeadline() == task.getOffset()):
                task_job = task.endCurrentJob(time)
                self.scheduleDealine(task_job, time)

    def defineScheduleSpace(self, start, end, min_job_run):
        self._schedule = [[None,None] for i in range((end-start)//min_job_run)]
        self._arrivals = [[] for i in range((end-start)//min_job_run)]
        self._deadlines = [[] for i in range((end-start)//min_job_run + 1)]     # deadlines require more space
        self._misses = [[] for i in range((end-start)//min_job_run)]
        self._schedule_block = min_job_run

    def buildSystem(self, start, end, lowest_priority=None):
        block_check = self.GCDlist(self.getTaskSetWCET())                       # gcd all task lengths
        deadline_check = self.GCDlist(self.getTaskSetDeadlines())               # gcd all deadlines
        period_check = self.GCDlist(self.getTaskSetPeriods())                   # gcd all periods

        slot_size = self.GCDlist([block_check, deadline_check, period_check])   # define slot_size
        self.defineScheduleSpace(start, end, slot_size)

        for time in range(start, end + slot_size, slot_size):
            if(time > start):
                self.checkForTaskDeadline(time)
            if(time != end):
                self.checkForTaskRelease(time)
        self.assignTasksToSlots(lowest_priority)

    def simulate(self, start, end, lowest_priority=None):

        print("Schedule from: " + start + " to: " + end + " ; " + str(self.getNumberOfTasks()) + " tasks")
        start, end = int(start), int(end)

        self.buildSystem(start, end, lowest_priority)

        slot_start, slot_end = 0, 0
        prev_task, prev_job = None, None

        for slot in range(len(self.getDeadlines())):

            # print arrivals
            if(slot < len(self.getSchedule())):
                arrivals = self.getRelease(slot)
                if(len(arrivals) != 0):
                    for i in range(len(arrivals)):
                        print(str(slot * self.getScheduleBlockSize()) + " : Arrival of job T" + str(arrivals[i][0]) + "J" + str(arrivals[i][1]))

            # print deadlines
            deadlines = self.getDeadline(slot)
            if(len(deadlines) !=  0):
                for i in range(len(deadlines)):
                    print(str((slot) * self.getScheduleBlockSize()) + " : Deadline of job T" + str(deadlines[i][0]) + "J" + str(deadlines[i][1]))

            # print scheduled slots
            if(slot < len(self.getSchedule())):
                run = self.getSchedule(slot)
                current_task, current_job = run[0], run[1]

                # case : job scheduled
                if(current_task != None):

                    # case : there is a next slot
                    if(slot < len(self.getSchedule()) -1):
                        next_run = self.getSchedule(slot + 1)
                    next_task, next_job = next_run[0], next_run[1]

                    # case : new task or job
                    if(current_task != prev_task or current_job != prev_job):
                        slot_start = slot
                    slot_end = slot+1

                    # case : end task or job
                    if(next_task != current_task or next_job != current_job):
                        print(str(slot_start * self.getScheduleBlockSize()) + "-" + str(slot_end * self.getScheduleBlockSize()) + ": T" + str(current_task) + "J" + str(current_job))

                prev_task, prev_job = current_task, current_job

                # print deadline _misses
                misses = self.getMiss(slot)
                if(len(misses) != 0):
                    for i in range(len(misses)):
                        print(str(slot * self.getScheduleBlockSize()) + " : Job T" + str(misses[i][0]) + "J" + str(misses[i][1]) + " misses a deadline")

    def GCDlist(self, elements):
        gcd = 0
        for i in range(len(elements)-1):
            gcd = self.GCD(gcd, elements[i])
        return gcd

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
