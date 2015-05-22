# -*- coding: utf-8 -*-

import os
import os.path
import time
import shutil
import Global

dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),"users")

print("user dir %s" % dir)

class User():
    def __init__(self, user):
        self.__user = user.lower()
        self.__challenge = None
        self.__response = None
        self.__valid = False
        file = os.path.join(dir, "%s.txt" % user)
        fileLock = "%s.lock" % file
        fileTmp = "%s.old" % file
        if os.path.exists(file):
            #whait while lock file exist
            while os.path.exists(fileLock):
                time.sleep(0.01)
            #touch lock file
            with open(fileLock, 'w') as f:
                f.write("")

            #copy file to tmp
            shutil.copyfile(file, fileTmp)
            with open(fileTmp, "r") as fRead, open(file, "w") as fWrite:
                for i, line in enumerate(fRead):
                    if i == 2:
                        tab = line.split(Global.USER_FILE_DELIMITER)
                        print(tab)
                        if len(tab) == Global.USER_FILE_FIRST_CHAP_LINE:
                            self.__valid = True
                            self.__challenge = tab[0]
                            self.__response = tab[1].rstrip()
                    else:
                        fWrite.write(line)

            #remove tmp file
            os.remove(fileTmp)
            #remove lock file
            os.remove(fileLock)

    def isUserValid(self):
        return self.__valid

    def getChallenge(self):
        return self.__challenge

    def isChallengeValid(self, value):
        return self.__response == value and self.isUserValid()
