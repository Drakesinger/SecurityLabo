class IPFailCounter:
    def __init__(self, max):
        self.__dic = {}
        self.__max = max
    def isBlocked(self, ip):
        return self.__dic.get(ip, 0) < self.__max
    def success(self, ip):
        self.__dic[ip] = 0
    def fail(self, ip):
        self.__dic[ip] = self.__dic.get(ip, 0) + 1
