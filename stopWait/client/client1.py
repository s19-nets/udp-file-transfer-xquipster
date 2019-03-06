from socket import *
import sys

class Client:
    def __init__(self, af, socktype, file_name, choice, numClients):
        self.numClients = numClients
        self.sAddr = sAddr = ("127.0.0.1", 50000)                #set address and reserve port
        self.file_name, self.choice = file_name, choice
        self.clientSock = clientSock = socket(af, socktype)      #create client socket
        try:
            self.clientSock.connect(sAddr)          #connect to Server
            print("Connected to server.")
        except error:
            print("Error. Server not found.")
            sys.exit()
        self.sendNumClients()               #send number of clients to server
        self.sendBasicInfoToServer()        #send file name and choice to server
        self.determineChoice()              #determine if put or get
        self.closeConnection()              #close connection

    #get file from server        
#    def getFileFromServer(self):
#        with open(self.file_name, "w") as clientFile:
#            while True:
#                print("Receiving data...")
#                data = self.clientSock.recv(1024)
#                if data == "File not found. Try again.":
#                    print(data)
#                    return
#                if not data:
#                    break
#                print("data =" + data)
#                # write data to a file
#                clientFile.write(data)    
#        clientFile.close()
#        print("Successfully get file from server.")
#        return
#
    #put file to server
    def sendFileToServer(self):
        try:
            with open(self.file_name, "r") as clientFile:
                print("Sending file...")
                data = clientFile.read()
                self.clientSock.send(data)
                clientFile.close()
        except IOError as e:
            print("No such file or directory. Try again.")
            self.clientSock.send("File not found. Try again.")
            return
        print("Successfuly sent file to server.")
        return

    def determineChoice(self):
        if(self.choice == "PUT" or self.choice == "put"):
            self.sendFileToServer()
        elif(self.choice == "GET" or self.choice == "get"):
            self.getFileFromServer()
        else:
            print("Invalid choice. Choices: PUT or GET.")
        return
    
    def sendBasicInfoToServer(self):
        while True:
            #send file name and choice and if the ack is not received, send again
            self.clientSock.send((self.file_name + ":" + self.choice).encode())     #send file name and choice to server
            ack = self.clientSock.recv(4)
            if ack == "Done":
                return

    def sendNumClients(self):
        self.clientSock.send((str(self.numClients)).encode())     #send number of Clients to server
        return
    
    def closeConnection(self):
        self.clientSock.close()
        print("--- Connection closed. --- \n")
        return

def startClients():
    numClients = input('Enter the number of clients: ')
    clients = []
    #iterate with the number of clients
    #for i in range(int(numClients)):
    #print("Client " + str(i+1) + ".")
    file_name = "test.txt" #input('Enter file name: ')
    choice = "PUT" #input('Enter choice (PUT or GET): ')
    Client(AF_INET,SOCK_STREAM,file_name,choice, 1) #clients.append(Client(AF_INET, SOCK_STREAM, file_name, choice, numClients))
        
startClients()
