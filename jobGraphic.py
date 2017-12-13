class JobGraphic:

    def __init__(self, arrival, deadline, nb_task, nb_job, top_rect):
        self._arrival = arrival
        self._deadline = deadline
        self._nb_task = nb_task
        self._nb_job = nb_job
        self._top_rect  = top_rect
        self._vertices = []
        self.setVertices()

    def getArrival(self):
        return self._arrival

    def getDeadLine(self):
        return self._deadline

    def getNbTask(self):
        return self._nb_task

    def getNbJob(self):
        return self._nb_job

    def getTopRect(self):
        return self._top_rect

    def getBottomRect(self):
        return self._top_rect-20

    def getVertices(self):
        return self._vertices

    def setVertices(self):
        self._vertices = [
            (self._arrival, self.getBottomRect()),  # left, bottom
            (self._arrival, self._top_rect),  # left, top
            (self._deadline, self._top_rect),  # right, top
            (self._deadline, self.getBottomRect()),  # right, bottom
            (self._arrival, self.getBottomRect()),  # ignored - used to close to rectangle
        ]

    def getText(self):
        return "T"+str(self.getNbTask())+"J"+str(self.getNbJob())

    def getTextPosition(self):
        x = 0
        y = 0
        for i in range(len(self._vertices) - 1):
            x += self._vertices[i][0]
            y += self._vertices[i][1]

        x_position = x / (len(self._vertices) - 1)
        y_position = y / (len(self._vertices) - 1)
        return x_position, y_position
