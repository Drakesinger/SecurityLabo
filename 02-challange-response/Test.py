# -*- coding: utf-8 -*-

# chap test file
testUserName = "test"
testUserChallenges = {
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

import unittest
import ChallengeServer
import IPFailCounter
import Global
from User import User


def writeUserToFile():
    from ChallengeGenerator import generate_challenge
    generate_challenge(testUserName, 0, User.dir)
    with open("%s/%s.txt" % (User.dir, testUserName), "a") as f:
        for i in range(2):
            for k in testUserChallenges:
                f.write("%s%s%s\n" % (k, Global.USER_FILE_DELIMITER, testUserChallenges[k]))


writeUserToFile()


class TestChallengeServer(unittest.TestCase):
    def test_1(self):
        ipFailCounter = IPFailCounter.IPFailCounter(Global.MAX_TRY_BY_IP)
        srv = ChallengeServer.ChallengeServer("1.1.1.1", ipFailCounter)
        msg, keep = srv.receive(Global.get_message(1, "user"))
        self.assertFalse(keep)
        self.assertEqual(msg[0], "3")

    def test_2(self):
        ipFailCounter = IPFailCounter.IPFailCounter(Global.MAX_TRY_BY_IP)
        srv = ChallengeServer.ChallengeServer("1.1.1.1", ipFailCounter)
        msg, keep = srv.receive(Global.get_message(1, testUserName))
        self.assertTrue(keep)
        self.assertEqual(msg[0], "2")
        msg, keep = srv.receive(Global.get_message(4, "abcdefgh"))
        self.assertFalse(keep)
        self.assertEqual(msg[0], "6")

    def test_3(self):
        ipFailCounter = IPFailCounter.IPFailCounter(Global.MAX_TRY_BY_IP)
        srv = ChallengeServer.ChallengeServer("1.1.1.1", ipFailCounter)
        msg, keep = srv.receive(Global.get_message(1, testUserName))
        self.assertTrue(keep)
        self.assertEqual(msg[0], "2")
        msg, keep = srv.receive(Global.get_message(4, testUserChallenges[msg[2:].rstrip()]))

    def test_4(self):
        ipFailCounter = IPFailCounter.IPFailCounter(Global.MAX_TRY_BY_IP)
        srv = ChallengeServer.ChallengeServer("1.1.1.1", ipFailCounter)
        msg, keep = srv.receive("a aasf\n")
        self.assertFalse(keep)
        self.assertIsNone(msg)

    def test_5(self):
        ipFailCounter = IPFailCounter.IPFailCounter(Global.MAX_TRY_BY_IP)
        srv = ChallengeServer.ChallengeServer("1.1.1.1", ipFailCounter)
        msg, keep = srv.receive("1aaasf\n")
        self.assertFalse(keep)
        self.assertIsNone(msg)


class TestIPFailCounter(unittest.TestCase):
    def test_1(self):
        nb = 3
        ip = "1.2.3.4"
        ipFailCounter = IPFailCounter.IPFailCounter(nb)
        for i in range(nb):
            self.assertFalse(ipFailCounter.is_blocked(ip))
            ipFailCounter.fail(ip)
        self.assertTrue(ipFailCounter.is_blocked(ip))
        self.assertFalse(ipFailCounter.is_blocked("1.1.1.1"))
        ipFailCounter.success(ip)
        self.assertFalse(ipFailCounter.is_blocked(ip))
        for i in range(nb * 2):
            self.assertFalse(ipFailCounter.is_blocked(ip))
            ipFailCounter.success(ip)


class TestUser(unittest.TestCase):
    def test_1(self):
        u = User(testUserName)
        self.assertTrue(u.is_user_valid())

    def test_2(self):
        u = User("useR1")
        self.assertTrue(u.is_user_valid())

    def test_3(self):
        u = User("useR")
        self.assertFalse(u.is_user_valid())

    def test_4(self):
        u = User(testUserName)
        self.assertTrue(u.is_user_valid())
        self.assertTrue(u.is_challenge_valid(testUserChallenges[u.get_challenge()]))


if __name__ == '__main__':
    unittest.main()
