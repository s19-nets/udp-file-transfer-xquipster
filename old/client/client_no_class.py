from socket import *
import sys

def getFileFromServer(clientSocket, file_name):
    with open(file_name, "w") as clientFile:
        while True:
            print "Receiving data..."
            data = clientSocket.recv(1024)
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

def sendFileToServer(clientSocket, file_name):
    try:
        with open(file_name, "r") as clientFile:
            print "Sending file..."
            data = clientFile.read()
            clientSocket.send(data)
            clientFile.close()
    except IOError as e:
        print "No such file or directory. Try again."
        clientSocket.send("File not found. Try again.")
        return
    print "Successfuly sent file to server."
    return

def determineChoice(clientSocket, choice, file_name):
    if(choice == "PUT"):
        sendFileToServer(clientSocket, file_name)
    elif(choice == "GET"):
        getFileFromServer(clientSocket, file_name)
    else:
        print "Invalid choice. Choices: PUT or GET."
    return

def connectSocket():
    clientSocket = socket()                 #create a socket object
    clientAddr = ("127.0.0.1", 50000)       #set address and reserve port
    try:
        clientSocket.connect(clientAddr)
        print "Connected to server."
    except:
        print "Error. Server not found."
        sys.exit()
    return clientSocket

def startClient():
    try:
        file_name = sys.argv[1]                 #get file name from argument
        choice = sys.argv[2]                    #get user choice
    except:
        print "Wrong parameters."
        sys.exit()
    clientSocket = connectSocket()
    clientSocket.send(file_name + ":" + choice)     #send file name and choice to server
    determineChoice(clientSocket, choice, file_name)
    clientSocket.close()
    print "Connection closed."

startClient()
