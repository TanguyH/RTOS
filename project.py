import sys
from task import Task
from taskset import TaskSet
from schedule import Schedule
from InputVerifier import InputVerifier
from generator import Generator
from scheduleGraphic import ScheduleGraphic

def lowestPriorityViable(taskset, begin, end, task_number, established_priorities=[]):
    schedule = Schedule(taskset)
    schedule.buildSystem(begin, end, task_number, established_priorities)
    task_misses = schedule.checkForMisses()
    return not task_misses

def FIAction(source_file):
    taskset = TaskSet(source_file)
    fi = taskset.findFeasibilityInterval()
    print(fi)

def SIMAction(source_file, start, end):
    taskset = TaskSet(source_file)
    for task in taskset.getTasks():
        print(task.getOffset(), end=" | ")
        print(task.getPeriod(), end=" | ")
        print(task.getDeadline(), end=" | ")
        print(task.getWCET())
    schedule = Schedule(taskset)
    schedule.simulate(start, end)
    print(end)
    graphic = ScheduleGraphic(int(end), schedule,taskset)
    graphic.generateView()
    #graphic.testRect()

def Audsley(taskset, start, end, low_priorities = []):
    #viability = []
    #feasable = False
    to_remove = None

    for task in taskset.getTasks():
        viable = lowestPriorityViable(taskset, int(start), int(end), task.getTaskNumber(), low_priorities)

        for i in range(len(low_priorities)):
            print("\t", end="")
        print("Task " + str(task.getTaskNumber()) + " is", end=" ")

        if(not viable):
            print("not", end=" ")
        print("lowest priority viable")

        if(viable):
            # Audsley
            low_priorities.append(task.getTaskNumber())
            taskset.removeTask(task)
            Audsley(taskset, start, end, low_priorities)

# not done ..
def AUDSLEYAction(source_file, start, end):

    start_taskset = TaskSet(source_file)
    Audsley(start_taskset, int(start), int(end))

    #for lowest_priority_viability in viability:
    #    if(lowest_priority_viability):
    #        print("next round")

def GENAction(nb_tasks, utilization, output_file):
    gen = Generator(nb_tasks, utilization, output_file)
    gen.generateSystem()
    gen.generateFile()


if __name__ == "__main__":

    arguments = list(sys.argv)
    inputCheck = InputVerifier(arguments)
    if (inputCheck.getError()):
        print(inputCheck.getError() + " --- " + inputCheck.getErrorPhrase())
    else:

        action = inputCheck.getAction()
        if (action == "FI"):
            source_file = arguments[2]
            FIAction(source_file)
        elif (action == "SIM"):
            start = arguments[2]
            end = arguments[3]
            source_file = arguments[4]
            SIMAction(source_file, start, end)
        elif (action == "AUDSLEY"):
            start = arguments[2]
            end = arguments[3]
            source_file = arguments[4]
            AUDSLEYAction(source_file, start, end)
        elif (action == "GEN"):
            nb_tasks = arguments[2]
            utilization = arguments[3]
            output_file = arguments[4]
            print("action : GEN")
            GENAction(nb_tasks, utilization, output_file)
