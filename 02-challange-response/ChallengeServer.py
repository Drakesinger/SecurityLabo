# -*- coding: utf-8 -*-

import re
import User
import Global
import enum

class State(enum.Enum):
    StateError = 0
    StateWaitUser = 1
    StateWaitChallenge = 2
    StateConnected = 3

class ChallengeServer:
    errorUser = Global.getMessage(3, "user KO")
    errorBadFormat = None
    errorBadProtocol = None
    errorChallenge = Global.getMessage(6, "challenge KO")
    def __init__(self, clientIp, ipFailCounter):
        self.__clientIp = clientIp
        self.__ipFailCounter = ipFailCounter
        self.__state = State.StateWaitUser
        self.__user = None
    def error(self, message = None):
        self.__state = State.StateError
        self.__ipFailCounter.fail(self.__clientIp)
        return message, False
    def receive(self, msg):
        print("recive '%s' state %s" % (msg.rstrip(), self.__state))
        message = Global.Message(msg)
        if not message.isValid():
            return self.error(self.errorBadFormat)
        if message.getCode() == 1 and self.__state == State.StateWaitUser:
            if not re.match(Global.REGEX_USER, message.getContent()):
                return self.error(self.errorUser)
            self.__user = User.User(message.getContent())
            if self.__user.isUserValid():
                self.__state = State.StateWaitChallenge
                return Global.getMessage(2, self.__user.getChallenge()), True
            else:
                return self.error(self.errorUser)
        elif message.getCode() == 4 and self.__state == State.StateWaitChallenge:
            if not re.match(Global.REGEX_USER, message.getContent()):
                return self.error(self.errorChallenge)
            if self.__user.isChallengeValid(message.getContent()):
                self.__state = State.StateConnected
                return Global.getMessage(5, "Challenge ok"), True
            else:
                return self.error(self.errorChallenge)
        return self.error(self.errorBadProtocol)
