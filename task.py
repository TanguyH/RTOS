class Task:
    def __init__(self, offset, period, deadline, WCET, task_no):
        self._offset = offset
        self._period = period
        self._deadline = deadline
        self._WCET = WCET
        self._task_no = task_no
        self._job_release = 0

    def getOffset(self):
        return self._offset

    def getPeriod(self):
        return self._period

    def getDeadline(self):
        return self._deadline

    def getWCET(self):
        return self._WCET

    def getTaskNumber(self):
        return self._task_no

    def getJobRelease(self):
        return self._job_release

    def clearJobRealease(self):
        self._job_release = 0

    def releaseJob(self, time):
        self._job_release += 1
        return [self.getTaskNumber(), self.getJobRelease()]

    def endCurrentJob(self, time):
        return [self.getTaskNumber(), self.getJobRelease()]

    def reset(self):
        self._job_release = 0
