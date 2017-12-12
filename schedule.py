from additional import *

class Schedule:
    def __init__(self, task_set):
        self._task_set = task_set
        self._arrivals = []
        self._deadlines = []
        self._misses = []
        self._deadline_type = "soft"

        self._schedule = []
        self._schedule_block = 0
        self._schedule_queue = []

    def getTaskSet(self):
        return self._task_set

    def getTasksFromTaskset(self):
        return self.getTaskSet().getTasks()

    def getTasksFromOriginalTaskset(self):
        return self.getTaskSet().getOriginalTasks()

    def setTaskSet(self, task_set):
        self._task_set = task_set

    def getNumberOfTasks(self):
        return self.getTaskSet().getNumberOfTasks()

    def getTaskSetWCET(self):
        return self.getTaskSet().getTasksWCET()

    def getTaskSetDeadlines(self):
        return self.getTaskSet().getTasksDeadlines()

    def getTaskSetPeriods(self):
        return self.getTaskSet().getTasksPeriods()

    def getDeadlineType(self):
        return self._deadline_type

    def setHardDeadlines(self):
        self._deadline_type = "hard"

    def setSoftDeadlines(self):
        self._deadline_type = "soft"

    def getSchedule(self, i = None):
        if(i != None):
            return self._schedule[i]
        return self._schedule

    def setSchedule(self, i, task_number):
        self._schedule[i] = task_number

    def getScheduleBlockSize(self):
        return self._schedule_block

    def getRelease(self, i=None):
        if(i != None):
            return self._arrivals[i]
        return self._arrivals

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

    def clearTaskInformations(self):
        for task in self.getTasksFromTaskset():                                 #------ original ?
            task.clearJobRealease()

    # not sure if working
    def checkForMisses(self, task_number=None):
        miss = False
        if(task_number != None):
            for slot in self.getMisses():
                for task_job in slot:
                    if task_job[0] == task_number:
                        miss = True
        else:
            for elem in self.getMisses():
                if elem:
                    miss = True

        return miss

    def scheduleRelease(self, task_job, time):
        block = time // self.getScheduleBlockSize()
        self.setRelease(block, task_job)

    def scheduleTask(self, task, job, time, to_sched = 0):

        dead_range = task.getDeadline() // self.getScheduleBlockSize()
        max_range = task.getPeriod() // self.getScheduleBlockSize()
        blocks_to_fit = task.getWCET() // self.getScheduleBlockSize()

        #----   (block for Audsely purposes)
        done = False

        if(to_sched > 0):
            blocks_to_fit = to_sched
        #-----^

        starting_point = time // self.getScheduleBlockSize()
        dead_end_point = min(starting_point + dead_range, len(self.getSchedule()))
        end_point = min(starting_point + max_range, len(self.getSchedule()))

        for block in range(starting_point, end_point):
            if(self.getSchedule(block) == [None,None] and blocks_to_fit > 0):
                self.setSchedule(block, [task.getTaskNumber(), job])
                blocks_to_fit -= 1

        #----- (block for Audsley purposes)
        if(end_point == len(self.getSchedule())):
            blocks_to_fit = -1

        while (blocks_to_fit > 0 and not done):
            self.flagDeadlineMiss(dead_end_point-1, [task.getTaskNumber(), job])
            if(self.getDeadlineType() == "soft"):
                blocks_to_fit = self.scheduleTask(task, job, time + self.getScheduleBlockSize(), blocks_to_fit)

                if(blocks_to_fit == -1):
                    done = True
        #--^
        return blocks_to_fit

    def assignTasksToSlots(self, lowest_priority=None, established_lowest=[]):
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

        else:
            # schedule all except lowest and established_lowest
            for priority in priorities.keys():
                if (priority != lowest_priority) and (priority not in established_lowest):  # MOD after and
                    for task_time in priorities[priority]:
                        self.scheduleTask(task_time[0], task_time[1], task_time[2])

            # schedule lowest
            if(lowest_priority in priorities.keys()):
                for task_time in priorities[lowest_priority]:
                    self.scheduleTask(task_time[0], task_time[1], task_time[2])

            # code = good, but tasks not in system
            #----------------------------------------------------------------------------------
            # schedule established_lowest                                               # added
            #if(established_lowest):
            #    established_lowest = established_lowest[::-1]
            #    for i in range(0, len(established_lowest)):
            #        #print("scehduling " + str(established_lowest[i]))
            #        for task_time in priorities[established_lowest[i]]:
            #            #print("scehduling " + str(established_lowest[i]))
            #            self.scheduleTask(task_time[0], task_time[1], task_time[2])
            #^---------------------------------------------------------------------------------

            #print("----- ----- -----")

    def scheduleDealine(self, task_job, time):
        block = time // self.getScheduleBlockSize()
        if(block < len(self.getDeadlines())):
            self.setDeadline(block, task_job)

    def checkForTaskRelease(self, time):
        for task in self.getTasksFromTaskset():                                 # -- original taskset ?
            if(time % task.getPeriod() == 0) and (time >= task.getOffset()):    # 0 was task.getOffset()
                task_job = task.releaseJob(time)
                self.scheduleRelease(task_job, time)
                self._schedule_queue.append((task, task_job[1], time))

    def checkForTaskDeadline(self, time):                                       # -- original taskset ?
        for task in self.getTasksFromTaskset():
            if(time % task.getDeadline() == 0) and (time >= task.getOffset()):                                 # 0 was task.getOffset()
                task_job = task.endCurrentJob(time)
                self.scheduleDealine(task_job, time)

    def defineScheduleSpace(self, start, end, min_job_run):
        if(min_job_run > 0):
            self._schedule = [[None,None] for i in range((end-start)//min_job_run)]
            self._arrivals = [[] for i in range((end-start)//min_job_run)]
            self._deadlines = [[] for i in range((end-start)//min_job_run + 1)]     # deadlines require more space
            self._misses = [[] for i in range((end-start)//min_job_run)]
            self._schedule_block = min_job_run
        self.clearTaskInformations()

    def buildSystem(self, start, end, lowest_priority=None, established_lowest=[]):
        block_check = gcdlist(self.getTaskSetWCET())                       # gcd all task lengths
        deadline_check = gcdlist(self.getTaskSetDeadlines())               # gcd all deadlines
        period_check = gcdlist(self.getTaskSetPeriods())                   # gcd all periods

        slot_size = gcdlist([block_check, deadline_check, period_check])   # define slot_size
        self.defineScheduleSpace(start, end, slot_size)

        if(slot_size > 0):
            for time in range(start, end + slot_size, slot_size):
                if(time > start):
                    self.checkForTaskDeadline(time)
                if(time != end):
                    self.checkForTaskRelease(time)
            self.assignTasksToSlots(lowest_priority, established_lowest)

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
