import unittest
import ChallengeServer
import IPFailCounter
import Global
from User import User

class TestChallengeServer(unittest.TestCase):
    def test_1(self):
        ipFailCounter = IPFailCounter.IPFailCounter(Global.MAX_TRY_BY_IP)
        srv = ChallengeServer.ChallengeServer("1.1.1.1", ipFailCounter)
        msg, keep = srv.receive(Global.getMessage(1, "user"))
        print("test_1.1 %s %s" % (msg.rstrip(), keep))
        self.assertFalse(keep)
        self.assertEqual(msg[0], "3")

    def test_2(self):
        ipFailCounter = IPFailCounter.IPFailCounter(Global.MAX_TRY_BY_IP)
        srv = ChallengeServer.ChallengeServer("1.1.1.1", ipFailCounter)
        msg, keep = srv.receive(Global.getMessage(1, "user1"))
        print("test_2.1 %s %s" % (msg.rstrip(), keep))
        self.assertTrue(keep)
        self.assertEqual(msg[0], "2")
        msg, keep = srv.receive(Global.getMessage(4, "abcdefgh"))
        print("test_2.2 %s %s" % (msg.rstrip(), keep))
        self.assertFalse(keep)
        self.assertEqual(msg[0], "6")

    def test_3(self):
        ipFailCounter = IPFailCounter.IPFailCounter(Global.MAX_TRY_BY_IP)
        srv = ChallengeServer.ChallengeServer("1.1.1.1", ipFailCounter)
        msg, keep = srv.receive(Global.getMessage(1, "user1"))
        print("test_3.1 '%s' %s" % (msg.rstrip(), keep))
        self.assertTrue(keep)
        self.assertEqual(msg[0], "2")
        msg, keep = srv.receive(Global.getMessage(4, Global.user1[msg[2:].rstrip()]))
        print("test_3.2 %s %s" % (msg.rstrip(), keep))

class TestIPFailCounter(unittest.TestCase):
    def test_1(self):
        nb = 3
        ip = "1.2.3.4"
        ipFailCounter = IPFailCounter.IPFailCounter(nb)
        for i in range(nb):
            self.assertFalse(ipFailCounter.isBlocked(ip))
            ipFailCounter.fail(ip)
        self.assertTrue(ipFailCounter.isBlocked(ip))
        self.assertFalse(ipFailCounter.isBlocked("1.1.1.1"))
        ipFailCounter.success(ip)
        self.assertFalse(ipFailCounter.isBlocked(ip))
        for i in range(nb * 2):
            self.assertFalse(ipFailCounter.isBlocked(ip))
            ipFailCounter.success(ip)

class TestUser(unittest.TestCase):
    def test_1(self):
        u = User("user1")
        self.assertTrue(u.isUserValid())
    def test_2(self):
        u = User("useR1")
        self.assertTrue(u.isUserValid())
    def test_3(self):
        u = User("useR")
        self.assertFalse(u.isUserValid())
    def test_4(self):
        u = User("user1")
        self.assertTrue(u.isUserValid())
        self.assertTrue(u.isChallengeValid(Global.user1[u.getChallenge()]))

if __name__ == '__main__':
    unittest.main()
