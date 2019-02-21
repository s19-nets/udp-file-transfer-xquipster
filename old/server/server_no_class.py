from socket import *
import sys

def getFileFromClient(conn, file_name, restOfBuffer):
    if restOfBuffer == "File not found. Try again.":
        print restOfBuffer
        return
    with open(file_name, "w") as serverFile:
        serverFile.write(restOfBuffer)
        while True:
            print "Receiving data..."
            data = conn.recv(1024)
            if restOfBuffer == "File not found. Try again.":
                return
            if not data:
                break
            print "Data = " + data
            # write data to a file
            serverFile.write(data)    
    serverFile.close()
    print "Successfully get file from client."
    return

def sendFileToClient(conn, file_name):
    try:
        with open(file_name, "r") as serverFile:
            print "Sending file..."
            data = serverFile.read()
            conn.send(data)
            serverFile.close()
    except IOError as e:
        print "No such file or directory. Try again."
        conn.send("File not found. Try again.")
        conn.close()
        return
    print "Successfuly sent file to client."
    conn.close()
    return

def determineChoice(conn, c, file_name):
    choice = c[:3]
    if(choice == "PUT"):
        restOfBuffer = c[3:]
        getFileFromClient(conn, file_name, restOfBuffer)
    elif(choice == "GET"):
        sendFileToClient(conn, file_name)
    else:
        print "Invalid choice."
    return
def getNameAndChoice(conn):
    nameChoice = conn.recv(1024).split(":")
    file_name = nameChoice[0]
    choice = nameChoice[1]
    return file_name, choice

def socketListen():
    serverAddr = ("127.0.0.1", 50000)           #set host and address
    serverSocket = socket()                     #create a socket object
    serverSocket.bind(serverAddr)               #bind to the port
    serverSocket.listen(1)                      #wait for client connection.
    print "Server listening...."
    return serverSocket

def startServer():
    serverSocket = socketListen()
    while True:
        conn, addr = serverSocket.accept()      #establish connection with client.
        print "Got connection from", addr
        file_name, choice = getNameAndChoice(conn)
        determineChoice(conn, choice, file_name)
        serverSocket.close()
        print "Connection closed."
        sys.exit()
startServer()
