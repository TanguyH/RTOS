class InputVerifier:
    def __init__(self, arguments):
        self._arguments = arguments
        self._arguments_size = len(arguments)
        self._action = None
        self._error = None
        self._error_phrase = None
        self.checkArguments();

    def getArguments(self):
        return self._arguments

    def getArgumentsSize(self):
        return self._arguments_size

    def getArgAt(self, index):
        return self._arguments[index]

    def getAction(self):
        return self._action

    def getError(self):
        return self._error

    def getErrorPhrase(self):
        return self._error_phrase

    def checkArguments(self):

        if (self.getArgumentsSize() == 3):
            self.FIValidity()
        elif (self.getArgumentsSize()  == 5):
            type = self.getArgAt(1)
            if (type == "sim"):
                self.SimValidity()
            elif (type == "audsley"):
                self.AudlseyValidity()
            elif (type == "gen"):
                self.GeneratorValidity()
            else:
                self._error = "CNF"
                self._error_phrase = "Command not found : "+type

        else:
            self._error = "INOA"
            self._error_phrase = "Invalid number of arguments"

    def FIValidity(self):
        type = self.getArgAt(1)
        filename = self.getArgAt(2)
        if (not type == "interval"):
            self._error = "EF1"
            self._error_phrase = "Error : interval argument"
        elif (not filename[-4:] == ".txt"):
            self._error = "EF2"
            self._error_phrase = "Error : file .txt argument"
        else:
            self._action = "FI"

    def SimValidity(self):
        interval_start = self.getArgAt(2)
        interval_end = self.getArgAt(3)
        filename = self.getArgAt(4)
        if not (interval_start.isnumeric() and interval_end.isnumeric()) or (int(interval_start) > int(interval_end)):
            self._error = "ES1"
            self._error_phrase = "Error : interval argument -- interval must contain two numbers [a,b] s.t. a<=b"
        elif (not filename[-4:] == ".txt"):
            self._error = "ES2"
            self._error_phrase = "Error : file .txt argument"
        else:
            self._action = "SIM"

    def AudlseyValidity(self):
        interval_start = self.getArgAt(2)
        interval_end = self.getArgAt(3)
        filename = self.getArgAt(4)
        if not (interval_start.isnumeric() and interval_end.isnumeric()) or (int(interval_start) > int(interval_end)):
            self._error = "EA1"
            self._error_phrase = "Error : interval argument -- interval must contain two numbers [a,b] s.t. a<=b"
        elif (not filename[-4:] == ".txt"):
            self._error = "EA2"
            self._error_phrase = "Error : file .txt argument"
        else:
            self._action = "AUDSLEY"

    def GeneratorValidity(self):
        nb_tasks = self.getArgAt(2)
        utilization = self.getArgAt(3)
        filename = self.getArgAt(4)
        if (not nb_tasks.isnumeric() or int(nb_tasks)<=0):
            self._error = "EG1"
            self._error_phrase = "Error : number of tasks arguments -- must be a number > 0"
        elif (not utilization.isnumeric() or float(utilization) <=0 or float(utilization) >100):
            self._error = "EG2"
            self._error_phrase = "Error : utilization factor -- must be a number in ]0,100]"
        elif (not filename[-4:] == ".txt"):
            self._error = "EG3"
            self._error_phrase = "Error : file .txt argument"
        else:
            self._action = "GEN"