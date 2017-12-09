import sys
from task import Task
from taskset import TaskSet
from InputVerifier import InputVerifier

# not sure if working
def lowestPriorityViable(taskset, begin, end, task_number):
    taskset.buildSystem(begin, end, task_number)
    task_misses = taskset.checkForMisses(task_number)
    return not task_misses

def FIAction(source_file):
    taskset = TaskSet(source_file)
    fi = taskset.findFeasibilityInterval()
    print(fi)

def SIMAction(source_file, start, end):
    taskset = TaskSet(source_file)
    taskset.simulate(start, end)

# not done ..
def AUDSLEYAction(source_file, start, end):
    taskset = TaskSet(source_file)

    for task in taskset.getTaskSet():
        viable = lowestPriorityViable(taskset, int(start), int(end), task.getTaskNumber())
        print(viable)

def GENAction(source_file):
    taskset = TaskSet(source_file)


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
            source_file = arguments[4]
            print("action : GEN")
            GENAction(source_file)
