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

#for test only
user1 = {
    "RKhcK": "DztGhRcp",
    "oBTqK": "EcIQgNKQ",
    "zZTDl": "iiDirjEj",
    "nTTbg": "uwdiFNBl",
    "MkvYj": "OlBgChSu",
    "ZwuwP": "BazNVEby",
    "mecTP": "lsRiNgAE",
    "kfnTq": "bDfDWuTb",
    "ckRyA": "NSfoYOdD",
    "IGDMC": "DNHeIYAU",
}
