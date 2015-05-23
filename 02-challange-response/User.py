# -*- coding: utf-8 -*-

import os
import os.path
import time
import shutil
import Global

class User:
    dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "users")
    def __init__(self, user):
        self.__user = user.lower()
        self.__challenge = None
        self.__response = None
        self.__valid = False
        file = os.path.join(self.dir, "%s.txt" % user)
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
            #open both files (copy every line on tmp to normail file)
            with open(fileTmp, "r") as fRead, open(file, "w") as fWrite:
                #enumerace for the no of line
                for i, line in enumerate(fRead):
                    #we use the first chap of line
                    if i == Global.USER_FILE_FIRST_CHAP_LINE:
                        #split
                        tab = line.split(Global.USER_FILE_DELIMITER)
                        # if valid line
                        if len(tab) == 2:
                            # get information
                            self.__valid = True
                            self.__challenge = tab[0]
                            self.__response = tab[1].rstrip()
                    else: # if not first chap, write line to dest
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
