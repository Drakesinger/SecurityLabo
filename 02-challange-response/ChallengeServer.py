# -*- coding: utf-8 -*-

import re

REGEX_USER = "^[A-Za-z0-9]{4,}$"
REGEX_CHALLENGE = "^[A-Za-z]{8}$"

class ChallengeServer:
    def __init__(self):
        self.__state = StateWaitUser()

    def receive(self, msg):
        print("recive '%s' state %s" % (msg, self.__state))
        code = msg[0]
        if not self.__state.acceptCode(code) or not msg[1] == " ":
            return None, False
        value = msg[2:]

        response = self.__state.getResponse(value)
        keepOpen = self.__state.keepOpen
        self.__state = self.__state.nextState()
        return response, keepOpen




class StateInterface:
    def __init__(self):
        self.keepOpen = False
    def acceptCode(self, code):
        raise NotImplementedError("This is interface")
    def getResponse(self, message):
        raise NotImplementedError("This is interface")
    def nextState(self):
        raise NotImplementedError("This is interface")


class StateWaitUser(StateInterface):
    def __init__(self):
        StateInterface.__init__(self)
        self.__user = None
    def acceptCode(self, code):
        return code == "1"
    def error(self):
        return "3 user KO"
    def getResponse(self, message):
        if not re.match(REGEX_USER, message):
            return self.error()
        if message == "jules" or True:
            self.keepOpen = True
            self.__user = "jules"
            return "2 userOK"
        else:
            return self.error()

    def nextState(self):
        if self.keepOpen:
            return StateWaitChallenge(self.__user)
        else:
            return None


class StateWaitChallenge(StateInterface):
    def __init__(self, user):
        StateInterface.__init__(self)
        self.__user = user
    def acceptCode(self, code):
        return code == "4"
    def error(self):
        return "6 challenge KO"
    def getResponse(self, message):
        if not re.match(REGEX_CHALLENGE, message):
            return self.error()
        if message == "1234" or True:
            self.keepOpen = True
            return "5 challengeOK"
        else:
            return self.error()

    def nextState(self):
        return None