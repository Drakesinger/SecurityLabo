# -*- coding: utf-8 -*-

import os
import os.path
import time
import shutil
from datetime import datetime
import Global


class User:
    """
    Class representing a User that needs to responde to a challenge.
    The user's challenges and responses are defined in the users folder by
    a file [user_name].txt containing rows of:
    [challenge]\t[response]

    The challenge must be of a length of 4 characters minimum and contains only letters.
    The response must be of a length of 8 characters minimum and contains only letters.
    """
    dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "users")
    print("Dir", dir)

    def __init__(self, user):
        self.__user = user.lower()
        self.__challenge = None
        self.__response = None
        self.__valid = False

        file = os.path.join(self.dir, "%s.txt" % user)
        file_locked = "%s.lock" % file
        file_tmp = "%s.old" % file

        if os.path.exists(file):

            # Wait while locked file exists.
            while os.path.exists(file_locked):
                time.sleep(0.01)

            # Touch locked file.
            with open(file_locked, 'w') as f:
                f.write("")

            # Copy the file to a temporary file.
            shutil.copyfile(file, file_tmp)

            # All data is invalid at the start.
            user_valid = False
            date_valid = False

            # Open both files and copy every line int tmp to the normal file.
            with open(file_tmp, "r") as fRead, open(file, "w") as fWrite:
                # Get the number of lines within the file and the line itself.
                for index_line, line in enumerate(fRead):

                    # Check if the file is not expired.
                    if index_line == Global.USER_FILE_EXPIRATION_DATE_LINE:
                        date_valid = datetime.now() < datetime.strptime(line.rstrip(), Global.DATE_FORMAT)
                        print("Valid Date:", date_valid)

                    # We use the first line where we have a chap.
                    if index_line == Global.USER_FILE_FIRST_CHAP_LINE:
                        # Split the line.
                        tab = line.split(Global.USER_FILE_DELIMITER)

                        # Check if the line is valid.
                        if len(tab) == 2:
                            # Get the challenge and response.
                            user_valid = True
                            self.__challenge = tab[0]
                            self.__response = tab[1].rstrip()

                            # Since we don't compute anything, the expected response
                            # is displayed server-side.
                            print("Challege | Response:",self.__challenge,self.__response)

                    else:
                        fWrite.write(line)

            self.__valid = date_valid and user_valid

            # Remove tmp file.
            os.remove(file_tmp)

            # Remove locked file.
            os.remove(file_locked)

    def is_user_valid(self):
        return self.__valid

    def get_challenge(self):
        return self.__challenge

    def is_challenge_valid(self, value):
        return self.__response == value and self.is_user_valid()
