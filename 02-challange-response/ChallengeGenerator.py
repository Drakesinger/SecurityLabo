#-*- coding: utf-8 -*-

import string
from random import choice
import os
import datetime
import Global

KEY_LENGHT = 5
CHALLENGE_LENGHT = 8
EXPIRATION_DAYS = 30

def generateKeyword(alphabet, lenght):
    return "".join(choice(alphabet) for _ in range(lenght))

def generateChallenge(username, output_folder="users", entries=10, expiration_date=None):

    if expiration_date is None:
        expiration_date = datetime.datetime.now() + datetime.timedelta(days=EXPIRATION_DAYS)
    alphabet = string.ascii_letters


    keys = [generateKeyword(alphabet, KEY_LENGHT) for k in range(entries)]
    challenges = [generateKeyword(alphabet, CHALLENGE_LENGHT) for k in range(entries)]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(output_folder+"/" + username + ".txt", encoding="UTF-8", mode="w") as file:
        file.write(expiration_date.strftime("%c") + "\n")

        file.write("\n")

        for (key, challenge) in zip(keys, challenges):
            file.write(key + Global.USER_FILE_DELIMITER + challenge + "\n")

if __name__ == '__main__':
    for i in range(5):
        generateChallenge("user" + str((i+1)))


# TODO: It might be interesting to keep the trace of all key/value pair to avoid generating an existing key/value pair