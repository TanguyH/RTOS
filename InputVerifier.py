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
            if (self.getArgAt(1) == "sim"):
                self.SimValidity()
            elif (self.getArgAt(1) == "audsley"):
                self.AudlseyValidity()
            elif (self.getArgAt(1) == "gen"):
                self.GeneratorValidity()
            else:
                self._error = "CNF"
                self._error_phrase = "Command not found : "+self.getArgAt(1)

        else:
            self._error = "INOA"
            self._error_phrase = "Invalid number of arguments"

    def FIValidity(self):
        if (not self.getArgAt(1) == "interval"):
            self._error = "EF1"
            self._error_phrase = "Error : interval argument"
        elif (not self.getArgAt(2)[-4:] == ".txt"):
            self._error = "EF2"
            self._error_phrase = "Error : file .txt argument"
        else:
            self._action = "FI"

    def SimValidity(self):
            if not (self.getArgAt(2).isnumeric() and  self.getArgAt(3).isnumeric()) or (self.getArgAt(2) > self.getArgAt(3)):
                self._error = "ES1"
                self._error_phrase = "Error : interval argument -- interval must contain two numbers [a,b] s.t. a<=b"
            elif (not self.getArgAt(4)[-4:] == ".txt"):
                self._error = "ES2"
                self._error_phrase = "Error : file .txt argument"
            else:
                self._action = "SIM"

    def AudlseyValidity(self):
            if not (self.getArgAt(2).isnumeric() and self.getArgAt(3).isnumeric()) or (self.getArgAt(2) > self.getArgAt(3)):
                self._error = "EA1"
                self._error_phrase = "Error : interval argument -- interval must contain two numbers [a,b] s.t. a<=b"
            elif (not self.getArgAt(4)[-4:] == ".txt"):
                self._error = "EA2"
                self._error_phrase = "Error : file .txt argument"
            else:
                self._action = "AUDSLEY"

    def GeneratorValidity(self):
            if not (self.getArgAt(2).isnumeric() and self.getArgAt(3).isnumeric()) or (self.getArgAt(2) > self.getArgAt(3)):
                self._error = "EG1"
                self._error_phrase = "Error : interval argument -- interval must contain two numbers [a,b] s.t. a<=b"
            elif (not self.getArgAt(4)[-4:] == ".txt"):
                self._error = "EG2"
                self._error_phrase = "Error : file .txt argument"
            else:
                self._action = "GEN"