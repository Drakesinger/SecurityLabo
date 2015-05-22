#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import ChallengeServer
import Global

ipFailCounter = None

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer): pass

class TCPHandler(socketserver.BaseRequestHandler):
    END_LINE = Global.END_LINE
    def send(self, msg):
        response = (msg + self.END_LINE).encode(encoding="UTF-8")
        self.request.sendall(response)
    def handle(self):
        print("%s connected" % (self.client_address[0]))
        if ipFailCounter.isBlocked()
        challengeServer = ChallengeServer.ChallengeServer()
        line = ""
        keepOpen = True
        try:
            while(keepOpen):
                # read data
                data = self.request.recv(Global.BUFFER_SIZE)
                line += data.decode(encoding="UTF-8")
                if self.END_LINE in line:
                    lines = line.split(self.END_LINE)
                    print(lines)
                    for i in range(len(lines) -1):
                        response, keepOpen = challengeServer.receive(lines[i])
                        if response:
                            self.send(response)

                    line = lines[-1]
        except Exception as e:
            print("Error with client, disconnect\n%s" % e)



def main():
    host = ""
    port = 7777
    print("Start server on %s:%d" % (host, port))
    print("Press Ctrl+C to exit server")
    import IPFailCounter
    global ipFailCounter
    ChallengeServer.ipFailCounter = ipFailCounter = IPFailCounter.IPFailCounter()

    server = socketserver.ThreadingTCPServer((host, port), TCPHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutdown server")
        server.shutdown()

if __name__ == '__main__':
    main()
