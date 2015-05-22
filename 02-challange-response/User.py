# -*- coding: utf-8 -*-

class User():
    def __init__(self, user):
        self.__user = user
        self.__challenge = None

    def isUserValid(self):
        return True

    def getChallenge(self):
        self.__challenge = "abcdefgh"
        return self.__challenge

    def isChallengeValid(self, value):
        return self.__challenge == value
