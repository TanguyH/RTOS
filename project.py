import sys
from task import Task
from taskset import TaskSet

def FIValidity(arguments):
    if(not arguments[1] == "interval"):
        return "EF1"                                                            # error : interval argument
    elif(not arguments[2][-4:] == ".txt"):
        return "EF2"                                                            # error : file .txt argument
    return "FI"

def SimValidity(arguments):
    if not(arguments[2].isnumeric() and arguments[3].isnumeric()) or (arguments[2] > arguments[3]):
        return "ES1"
    if(arguments[4][-4:] == ".txt"):
        return "ES2"
    return "SIM"

def AudlseyValidity(arguments):
    if not(arguments[2].isnumeric() and arguments[3].isnumeric()) or (arguments[2] > arguments[3]):
        return "EA1"
    if(arguments[4][-4:] == ".txt"):
        return "EA2"
    return "AUDSLEY"

def GeneratorValidity(arguments):
    if not(arguments[2].isnumeric() and arguments[3].isnumeric()) or (arguments[2] > arguments[3]):
        return "EG1"
    if(arguments[4][-4:] == ".txt"):
        return "EG2"
    return "GEN"

def verifyCommandLineValidity(arguments):
    """
    Function designed to verify validity of arguments, and stop execution if not valid
    """
    if(len(arguments) == 3):
        return FIValidity(arguments)

    elif(len(arguments) == 5):
        if(arguments[1] == "sim"):
            return SimValidity(arguments)
        elif(arguments[1] == "audsley"):
            return AudlseyValidity(arguments)
        elif(arguments[1] == "gen"):
            return GeneratorValidity(arguments)
        else:
            return "CNF"                                                        # command not found
    else:
        return "INOA"                                                           # invalid number of arguments




if __name__ == "__main__":
    #
    #   argument verification
    #
    arguments = list(sys.argv)
    case = verifyCommandLineValidity(arguments)

    #if(verif.getAction()[0] != "E" and request == "interval")

    #
    #   argument retrieval
    #
    request = arguments[1]
    source_file = arguments[2]
    print("interval : " + request)
    print("source : " + source_file)


    #
    #   task & taskset extraction
    #
    source_file = open(source_file, "r")
    taskset = TaskSet()
    for line in source_file:
        offset, period, deadline, WCET = line.split(" ")
        task = Task(int(offset), int(period), int(deadline), int(WCET))
        taskset.addTask(task)

    fi = taskset.findFeasibilityInterval()
    print(fi)

    
