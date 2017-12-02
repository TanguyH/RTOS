class Task:
    def __init__(self, offset, period, deadline, WCET):
        self._offset = offset
        self._period = period
        self._deadline = deadline
        self._WCET = WCET

    def getOffset(self):
        return self._offset

    def getPeriod(self):
        return self._period

    def getDeadline(self):
        return self._deadline

    def getWCET(self):
        return self._WCET
