# -*- coding: utf-8 -*-

import threading


class IPFailCounter:
    def __init__(self, max):
        self.__dic = {}
        self.__max = max
        self.lock = threading.RLock()

    def is_blocked(self, ip):
        with self.lock:
            return self.__dic.get(ip, 0) >= self.__max

    def success(self, ip):
        with self.lock:
            self.__dic[ip] = 0

    def fail(self, ip):
        with self.lock:
            self.__dic[ip] = self.__dic.get(ip, 0) + 1
