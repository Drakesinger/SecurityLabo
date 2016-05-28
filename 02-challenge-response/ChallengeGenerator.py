#!/usr/bin/python3
# -*- coding: utf-8 -*-

import string
from random import choice
import os
from _datetime import datetime, timedelta
import Global


def generate_keyword(alphabet, length):
    return "".join(choice(alphabet) for _ in range(length))


def generate_challenge(username, entries=Global.DEFAULT_KEY_NUMBER, output_folder="users", expiration_date=None):
    if expiration_date is None:
        expiration_date = datetime.now() + timedelta(days=Global.EXPIRATION_DAYS)
    alphabet = string.ascii_letters

    keys = [generate_keyword(alphabet, Global.KEY_LENGTH) for k in range(entries)]
    challenges = [generate_keyword(alphabet, Global.CHALLENGE_LENGTH) for k in range(entries)]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(output_folder + "/" + username + ".txt", encoding="UTF-8", mode="w") as file:
        file.write(expiration_date.strftime(Global.DATE_FORMAT) + "\n")

        file.write("\n")

        for (key, challenge) in zip(keys, challenges):
            file.write(key + Global.USER_FILE_DELIMITER + challenge + "\n")


def validate_regex(regexp):
    import re
    def inner(user):
        if not re.match(regexp, user):
            raise argparse.ArgumentTypeError("Invalid format")
        return user

    return inner


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("user", help="username", type=validate_regex(Global.REGEX_USER))
    parser.add_argument("-n", "--number", help="number of challenge", type=int, default=Global.DEFAULT_KEY_NUMBER)
    args = parser.parse_args()

    generate_challenge(args.user, args.number)
