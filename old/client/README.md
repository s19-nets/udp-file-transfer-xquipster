# Client
Last modification date: 4/14/18

## How to run the program:
    "python client.py"
### Additional notes on how to run program:
    This program does not take in any parameters. So the only way to start the client is by running the command above.
    The program will ask the user to enter the number of clients, followed by the filename and choice for each client.

## Background:
 This program is the client portion of a File Transfer Protocol. There is a server program that interacts with the client program to make the File transfer protocol possible. The client side will send a request to either retrieve a File(GET) or to save a file(PUT/SEND) to the server.
 Both the server and client programs use TCP to communicate with one another and they send packets. The first packet comes with a specific packet structure that contains the filename and choice. The rest of the packets contain messages.

### Protocol Description:
	 Packet structure for first packet:
	 	----------------------
		| File Name : Choice |
		----------------------
		* PUT(SEND) REQUEST
		  - Choice = PUT
          
		* GET REQUEST
		  - Choice = GET

### Program Description:
	This code implements the client side of a file transfer protocol using TCP. The way I created the client was implementing both PUT(SEND) and GET.

	For the PUT(SEND), the program did the following:
	    * Open the file that will be sent
        * Read the entire file and store it in a string
        * Send the string through the client socket to the server
        * Print a success message if it went through.
        * If file is not found, send an error message and close connection.
        
        For the GET, the program did the following:
	    * Create a new file with the specified file name
        * Start receiving messages from the server with the file content
        * Continously check if one of the messages contains an error message
        * If an error message is found, then the file was not found and the connection must be closed.
        * Print every message received
        * Print a success message is the entire file was received correctly.
        
    Since the server allows multiple connections, the program asks the user to input the number of clients, and filename and choice for each client.

## Author

* **Alejandro Davila** - [adavilamurra](https://github.com/adavilamurra)

