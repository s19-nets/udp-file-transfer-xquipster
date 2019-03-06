from socket import *
import sys

class Server:
    def __init__(self):
        self.listenerSocket = listenerSocket = self.socketListen()  #create listen socket
        self.connSocket, self.addr = connSocket, addr = None, ""
        self.file_name, self.choice, self.restOfBuffer = file_name, choice, restOfBuffer = "", "", ""
        self.numClients = numClients = 0
        self.serverAddr = serverAddr = ("", 0)
        self.fileNameLength = fileNameLength = 0
        self.acceptConnection()     #accept connection from client
        self.getNumberOfClients()   #get the number of clients

    #put file from client to server   
    def getFileFromClient(self):
        if self.restOfBuffer == "File not found. Try again.":
            return
        with open(self.file_name, "w") as serverFile:
            serverFile.write(self.restOfBuffer)
            while True:
                print("Receiving data...")
                data = self.connSocket.recv(1024)
                if self.restOfBuffer == "File not found. Try again." or data == "File not found. Try again.":
                    return
                if not data:
                    break
                print("Data Received = " + data)
                # write data to a file
                serverFile.write(data)    
        serverFile.close()
        print("Successfully get file from client.")
        return

    #get file from server to client
#    def sendFileToClient(self):
#        try:
#            with open(self.file_name, "r") as serverFile:
#                print("Sending file...")
#                data = serverFile.read()
#                self.connSocket.send(data)
#                serverFile.close()
#        except IOError as e:
#            print("No such file or directory. Try again.")
#            self.connSocket.send("File not found. Try again.")
#            self.connSocket.close()
#            return
#        print("Successfuly sent file to client.")
#        return
#
#    def determineChoice(self):
#        if(self.choice == "PUT" or self.choice == "put"):
#            self.getFileFromClient()
#        elif(self.choice == "GET" or self.choice == "get"):
#            self.sendFileToClient()
#        else:
#            print("Invalid choice.")
#        return
#
    def getNameAndChoice(self, clientNum):
        while True:
            nameChoice = (self.connSocket.recv(1024)).decode().split(":")
            if clientNum == 0:
                self.file_name = nameChoice[0]
            else:
                self.file_name = nameChoice[0][1:]
            try:
                if(len(nameChoice[1]) > 3):
                    self.choice = nameChoice[1][:3]
                    self.restOfBuffer = nameChoice[1][3:]
                else:
                    self.choice = nameChoice[1]
                    self.restOfBuffer = ""
                if (self.choice.lower()) == "put" or (self.choice.lower()) == "get":
                    self.connSocket.send("Done") 
                return
            except:
                print("Error. Data did not arrive correctly.")
                self.connSocket.send("error".encode())
            print(nameChoice)

    def getNumberOfClients(self):
        self.numClients = 1 #int(self.connSocket.recv(16))
        return
    
    def acceptConnection(self):
        while True:
            self.connSocket, self.addr = self.listenerSocket.accept()      #establish connection with client.
            print("Got connection from", self.addr)
            return 

    def socketListen(self):
        self.serverAddr = ("127.0.0.1", 50000)      #set host and address
        listenerSocket = socket()              #create a socket object
        listenerSocket.bind(self.serverAddr)        #bind to the port
        listenerSocket.listen(1)               #wait for client connection.
        print("Server listening....")
        return listenerSocket

    def closeConnection(self):
        self.listenerSocket.close()
        self.connSocket.close()
        print("Connection closed.")
        return

def startServer():
    server = Server()
    #check for connections depending on the number of clients
    for i in range(server.numClients):
        if(i > 0):
            server.acceptConnection()
        server.getNameAndChoice(i)
        server.determineChoice()
    server.closeConnection()

startServer()
