# -*- coding: utf-8 -*-

REGEX_USER = "^[A-Za-z0-9]{4,}$"
REGEX_CHALLENGE = "^[A-Za-z]{8}$"

REGEX_HOST = "^[A-Za-z0-9.]{2,}$"

END_LINE = "\r\n"

BUFFER_SIZE = 512

USER_FILE_DELIMITER = "\t"
USER_FILE_FIRST_CHAP_LINE = 2

MAX_TRY_BY_IP = 3

MESSAGE_SEPARATOR = " "

def getMessage(code, value):
    return "%d%s%s%s" % (code, MESSAGE_SEPARATOR, value, END_LINE)

class Message:
    def __init__(self, str):
        self.__valid = False
        self.__code = 0
        self.__content = ""
        self.__raw = str.rstrip()
        try:
            self.__code = int(str[0])
            if not str[1] == MESSAGE_SEPARATOR:
                return
            self.__content = self.__raw[2:]
            self.__valid = True
        except:
            return
    def getContent(self):
        if not self.isValid():
            raise Exception("Message not valid !")
        return self.__content
    def getCode(self):
        if not self.isValid():
            raise Exception("Message not valid !")
        return self.__code
    def isValid(self):
        return self.__valid
    def getRaw(self):
        return self.__raw

