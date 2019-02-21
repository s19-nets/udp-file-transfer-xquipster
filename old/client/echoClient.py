import random
import sys
import traceback
from select import *
from socket import *

import re
import params

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50000"),
    (('-n', '--numClients'), 'numClients', "4"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    (('-f', '--file'), 'file_name', "file.txt"),
    (('-c', '--choice'), 'choice', "GET")
    )

paramMap = params.parseParams(switchesVarDefaults)
server, usage, debug, file_name, choice = paramMap["server"], paramMap["usage"], paramMap["debug"], paramMap["file_name"], paramMap["choice"]
numClients = int(paramMap["numClients"])


if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print "Can't parse server:port from '%s'" % server
    sys.exit(1)


sockNames = {}               # from socket to name
nextClientNumber = 0     # each client is assigned a unique id

            
    
liveClients, deadClients = set(), set()

class Client:
    def __init__(self, af, socktype, saddr, file_name, choice):
        global nextClientNumber
        global liveClients, deadClients
        self.saddr = saddr # addresses
        self.file_name, self.choice = "",""
        self.allSent = 0
        self.error = 0
        self.isDone = 0
        self.clientIndex = clientIndex = nextClientNumber
        nextClientNumber += 1
        self.clientSocket = clientSocket = socket(af, socktype)
        print "New client #%d to %s" % (clientIndex, repr(saddr))
        sockNames[clientSocket] = "C%d:ToServer" % clientIndex
        clientSocket.setblocking(False)
        try:
            self.clientSocket.connect(saddr)
            print "Connected to server."
        except error:
            print "Error. Server not found."
            sys.exit()
        self.sendBasicInfoToServer()
        self.determineChoice()
        liveClients.add(self)
    def doSend(self):
        try:
            with open(self.file_name, "r") as clientFile:
                print "Sending file..."
                data = clientFile.read()
                self.clientSock.send(data)
                clientFile.close()
        except IOError as e:
            print "No such file or directory. Try again."
            self.clientSock.send("File not found. Try again.")
            return
        print "Successfuly sent file to server."
        return
    
    def doRecv(self):
        with open(self.file_name, "w") as clientFile:
            while True:
                print "Receiving data..."
                data = self.clientSock.recv(1024)
                if data == "File not found. Try again.":
                    print data
                    return
                if not data:
                    break
                print "data =" + data
                # write data to a file
                clientFile.write(data)    
        clientFile.close()
        print "Successfully get file from server."
        return

    def determineChoice(self):
        if(self.choice == "PUT"):
            self.sendFileToServer()
        elif(self.choice == "GET"):
            self.getFileFromServer()
        else:
            print "Invalid choice. Choices: PUT or GET."
        return
    
    def sendBasicInfoToServer(self):
        self.clientSock.send(self.file_name + ":" + self.choice + ":" + str(self.numClients))     #send file name and choice to server
        return
    
    def doErr(self, msg=""):
        error("socket error")
    def checkWrite(self):
        if self.allSent:
            return None
        else:
            return self.clientSocket
    def checkRead(self):
        if self.isDone:
            return None
        else:
            return self.clientSocket
    def done(self):
        self.isDone = 1
        self.allSent =1
        if self.numSent != self.numRecv: self.error = 1
        try:
            self.clientSocket(close)
        except:
            pass
        print "client %d done (error=%d)" % (self.clientIndex, self.error)
        deadClients.add(self)
        try: liveClients.remove(self)
        except: pass
            
    def errorAbort(self, msg):
        self.allSent =1
        self.error = 1
        print "FAILURE client %d: %s" % (self.clientIndex, msg)
        self.done()
        
                  
def lookupSocknames(socks):
    return [ sockName(s) for s in socks ]
    
for i in range(numClients):
    liveClients.add(Client(AF_INET, SOCK_STREAM, (serverHost, serverPort), file_name, choice))


while len(liveClients):
    rmap,wmap,xmap = {},{},{}   # socket:object mappings for select
    for client in liveClients:
        sock = client.checkRead()
        if (sock): rmap[sock] = client
        sock = client.checkWrite()
        if (sock): wmap[sock] = client
        xmap[client.clientSocket] = client
    if debug: print "select params (r,w,x):", [ repr([ sockNames[s] for s in sset] ) for sset in [rmap.keys(), wmap.keys(), xmap.keys()] ]
    rset, wset, xset = select(rmap.keys(), wmap.keys(), xmap.keys(),60)
    #print "select r=%s, w=%s, x=%s" %
    if debug: print "select returned (r,w,x):", [ repr([ sockNames[s] for s in sset] ) for sset in [rset,wset,xset] ]
    for sock in xset:
        xmap[sock].doErr()
    for sock in rset:
        rmap[sock].doRecv()
    for sock in wset:
        wmap[sock].doSend()


numFailed = 0
for client in deadClients:
    err = client.error
    print "Client %d Succeeded=%s, Bytes sent=%d, rec'd=%d" % (client.clientIndex, not err, client.numSent, client.numRecv)
    if err:
        numFailed += 1
print "%d Clients failed." % numFailed

