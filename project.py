import sys
from task import Task
from taskset import TaskSet
from schedule import Schedule
from InputVerifier import InputVerifier
from generator import Generator

def lowestPriorityViable(taskset, begin, end, task_number, established_priorities=[]):
    schedule = Schedule(taskset)

    print("\nschedule pre-status : ")
    print(schedule.getSchedule())
    print(schedule.getRelease())
    print(schedule.getDeadlines())
    print()

    schedule.buildSystem(begin, end, task_number, established_priorities)

    print("\nschedule post-status : ")
    print(schedule.getSchedule())
    print(schedule.getRelease())
    print(schedule.getDeadlines())
    print()

    task_misses = schedule.checkForMisses(task_number)
    return not task_misses

def FIAction(source_file):
    taskset = TaskSet(source_file)
    fi = taskset.findFeasibilityInterval()
    print(fi)

def SIMAction(source_file, start, end):
    taskset = TaskSet(source_file)
    schedule = Schedule(taskset)
    schedule.simulate(start, end)

def Audsley(taskset, start, end, low_priorities = []):
    viability = []
    feasable = False
    to_remove = None

    for task in taskset.getTasks():
        viable = lowestPriorityViable(taskset, int(start), int(end), task.getTaskNumber(), low_priorities)
        for i in range(len(low_priorities)):
            print("\t", end="")
        print("Task " + str(task.getTaskNumber()) + " is", end=" ")
        if(not viable):
            print("not", end=" ")
        print("lowest priority viable")
        viability.append(viable)

    i = 0
    while (i < len(viability)) and not feasable:
        if(viability[i]):
            feasable = True
            to_remove = taskset.getTasks(i)
            low_priorities.append(to_remove.getTaskNumber())
        i += 1

    if feasable:
        # new TaskSet
        taskset.removeTask(to_remove)
        return Audsley(taskset, start, end, low_priorities)
    else:
        return False




# not done ..
def AUDSLEYAction(source_file, start, end):

    start_taskset = TaskSet(source_file)
    viability = Audsley(start_taskset, int(start), int(end))

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
