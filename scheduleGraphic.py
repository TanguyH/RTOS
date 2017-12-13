import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from jobGraphic import JobGraphic
from schedule import Schedule

class ScheduleGraphic:
    def __init__(self, max_x, schedule, taskset):
        self._codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY,
        ]
        self._fig = plt.figure(figsize=(10,7))
        self._ax = self._fig.add_subplot(111)   #I, J, and K integer : the subplot is the Ith plot on a grid with J rows and K columns
        self._ax.set_title("Schedule")
        self._max_x = max_x
        self._max_y = (schedule.getNumberOfTasks()+1)*20
        self._schedule = schedule

        self._ax.set_xlim(0, self._max_x)
        self._ax.set_ylim(0, self._max_y)
        self._taskset = taskset

    def getMaxX(self):
        return self._max_x

    def getMaxY(self):
        return self._max_y

    def getCurrentTop(self,i):
        return self.getMaxY()-i*20

    def addRectangle(self, job_rectangle):
        path = Path(job_rectangle.getVertices(), self._codes)
        patch = patches.PathPatch(path, facecolor='green', lw=1)

        self._ax.add_patch(patch)
        text_position = job_rectangle.getTextPosition()
        text = job_rectangle.getText()
        self._ax.text(text_position[0], text_position[1], text, horizontalalignment='center', verticalalignment='center')

    def addSlots(self):
        index_schedule = 0
        previous_end = 0
        for i in range (len(self._schedule.getSlots())):
            start_slot = self._schedule.getSlots()[i][0]
            end_slot = self._schedule.getSlots()[i][1]
            if (start_slot != previous_end):
                index_schedule+= start_slot-previous_end

            nb_task = self._schedule.getSchedule()[index_schedule][0]
            nb_job = self._schedule.getSchedule()[index_schedule][1]

            print("Task : "+str(nb_task))
            print("Job : "+str(nb_job))
            print("Top rectangle = "+str(self.getCurrentTop(nb_task)))
            print("slot index : "+str(i))
            print("schedule index : "+str(index_schedule))
            job_rectangle = JobGraphic(start_slot*10,end_slot*10,nb_task,nb_job,self.getCurrentTop(nb_task))
            self.addRectangle(job_rectangle)
            index_schedule += end_slot - start_slot
            previous_end = end_slot  # to detect the empty spots in the slots

    def addBlocksView(self):
        line_codes = [
            Path.MOVETO,
            Path.LINETO,
        ]
        for i in range (0,self._max_x,self._schedule.getScheduleBlockSize()):
            for j in range (0, self._max_y, 10):
                line_vertices = [
                    (i,j),          #Start of vertical line
                    (i, j+5)        #goes up
                ]
                line = Path(line_vertices, line_codes)
                patch = patches.PathPatch(line, facecolor='orange', lw=1)
                self._ax.add_patch(patch)

    def addDeadLinesView(self):

        for task in self._taskset.getTasks():
            for i in range (0,self._max_x+1,task.getDeadline()):
                y = self.getCurrentTop(task.getTaskNumber())
                circle = plt.Circle((i, y),2, color="black",clip_on=False,fill=False)
                self._ax.add_artist(circle)

    def generateView(self):
        current_task = self._schedule.getSchedule()[0][0]
        print("block size : "+str(self._schedule.getScheduleBlockSize()))
        print("len slots : "+str(len(self._schedule.getSlots())))
        print("len schedule : "+str(len(self._schedule.getSchedule())))
        print("schedule list : " + str(self._schedule.getSchedule()))
        print("slots list : " + str(self._schedule.getSlots()))

        self.addSlots()
        self.addBlocksView()
        self.addDeadLinesView()
        plt.show()

