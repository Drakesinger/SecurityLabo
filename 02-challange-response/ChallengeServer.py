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
    errorUser = Global.get_message(3, "user KO")
    errorBadFormat = None
    errorBadProtocol = None
    errorChallenge = Global.get_message(6, "challenge KO")

    def __init__(self, clientIp, ipFailCounter):
        self.__clientIp = clientIp
        self.__ipFailCounter = ipFailCounter
        self.__state = State.StateWaitUser
        self.__user = None

    def error(self, message=None):
        self.__state = State.StateError
        self.__ipFailCounter.fail(self.__clientIp)
        return message, False

    def receive(self, msg):
        print("receive '%s' state %s" % (msg.rstrip(), self.__state))
        message = Global.Message(msg)

        # Check validity of the message.
        if not message.is_valid():
            print("Invalid message received.")
            return self.error(self.errorBadFormat)

        if message.get_code() == 1 and self.__state == State.StateWaitUser:

            if not re.match(Global.REGEX_USER, message.get_content()):
                print("Error991")
                return self.error(self.errorUser)

            self.__user = User.User(message.get_content())

            if self.__user.is_user_valid():
                self.__state = State.StateWaitChallenge
                return Global.get_message(2, self.__user.get_challenge()), True
            else:
                print("Error992")
                return self.error(self.errorUser)

        elif message.get_code() == 4 and self.__state == State.StateWaitChallenge:

            if not re.match(Global.REGEX_CHALLENGE, message.get_content()):
                print("Error993")
                return self.error(self.errorChallenge)

            if self.__user.is_challenge_valid(message.get_content()):
                self.__state = State.StateConnected
                return Global.get_message(5, "Challenge ok"), True
            else:
                print("Error994")
                return self.error(self.errorChallenge)

        print("Error995")
        return self.error(self.errorBadProtocol)
