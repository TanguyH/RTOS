import sys
from task import Task
from taskset import TaskSet
from InputVerifier import InputVerifier


def retrieveTaskSet(source_file):
    """
    Method who will analyze a given .txt file to get all information about the task set
    """
    source_file = open(source_file, "r")
    taskset = TaskSet()
    for line in source_file:
        offset, period, deadline, WCET = line.split(" ")
        task = Task(int(offset), int(period), int(deadline), int(WCET))
        taskset.addTask(task)
    return taskset

def FIAction(source_file):
    taskset = retrieveTaskSet(source_file)
    fi = taskset.findFeasibilityInterval()
    print(fi)

def SIMAction(source_file):
    taskset = retrieveTaskSet(source_file)

def AUDSLEYAction(source_file):
    taskset = retrieveTaskSet(source_file)

def GENAction(source_file):
    taskset = retrieveTaskSet(source_file)


if __name__ == "__main__":

    arguments = list(sys.argv)
    inputCheck = InputVerifier(arguments)
    if (inputCheck.getError()):
        print(inputCheck.getError()+" --- "+inputCheck.getErrorPhrase())
    else:

        action = inputCheck.getAction()
        if (action == "FI"):
            source_file = arguments[2]
            print("source : " + source_file)
            FIAction(source_file)
        elif (action == "SIM"):
            source_file = arguments[4]
            print ("action : SIM")
            SIMAction(source_file)
        elif (action == "AUDSLEY"):
            source_file = arguments[4]
            print("action : AUDSLEY")
            AUDSLEYAction(source_file)
        elif (action == "GEN"):
            source_file = arguments[4]
            print("action : GEN")
            GENAction(source_file)

