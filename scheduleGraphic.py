import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from jobGraphic import JobGraphic
from schedule import Schedule

class ScheduleGraphic:
    def __init__(self, max_x, max_y, schedule):
        self._codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY,
        ]
        self._fig = plt.figure()
        self._ax = self._fig.add_subplot(111)   #I, J, and K integer : the subplot is the Ith plot on a grid with J rows and K columns
        self._max_x = max_x
        self._max_y = schedule.getNumberOfTasks()+1
        self._schedule = schedule
        self._ax.set_xlim(0, self._max_x)
        self._ax.set_ylim(0, self._max_y)

    def getMaxX(self):
        return self._max_x

    def getMaxY(self):
        return self._max_y

    def getCurrentTop(self,i):
        return self.getMaxY()-i*20

    def addRectangle(self, job_rectangle):
        path = Path(job_rectangle.getVertices(), self._codes)
        patch = patches.PathPatch(path, facecolor='white', lw=2)

        self._ax.add_patch(patch)
        text_position = job_rectangle.getTextPosition()
        text = job_rectangle.getText()
        self._ax.text(text_position[0], text_position[1], text, horizontalalignment='center', verticalalignment='center')


    def generateView(self):
        current_task = self.getSchedule().getSchedule()[0][0]
        for i in range (len(self.getSchedule().getSchedule())):
            start_slot = self.getSchedule().getSlots()[i][0]
            end_slot = self.getSchedule().getSlots()[i][1]
            nb_task = self.getSchedule().getSchedule()[i][0]
            nb_job = self.getSchedule().getSchedule()[i][1]

            job_rectangle = JobGraphic(start_slot,end_slot,nb_task,nb_job,self.getCurrentTop(nb_task))
            self.addRectangle(job_rectangle)
        plt.show()

