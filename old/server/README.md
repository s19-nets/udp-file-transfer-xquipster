# Server
Last modification date: 4/14/18

## How to run the program:
    "python server.py"
### Additional notes on how to run program:
    This program does not take in any parameters. So the only way to start the client is by running the command above.

## Background:
 This program is the server portion of a File Transfer Protocol. There is a client program that interacts with the server program to make the File transfer protocol possible. The client side will send a request to either retrieve a File(GET) or to save a file(PUT/SEND) to the server.
 Both the server and client programs use TCP to communicate with one another and they send packets. The first packet comes with a specific packet structure that contains the file name and choice. The rest of the packets contain messages.

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
	This code implements the server side of a file transfer protocol using TCP. The way I created the server was implementing both PUT(SEND) and GET.

	For the PUT(SEND), the program did the following:
	    * Open the file that will be sent.
        * Read the entire file and store it in a string.
        * Send the string through the client socket to the server.
        * Print a success message if it went through.
        * If file is not found, send an error message and close connection.
        
        For the GET, the program did the following:
	    * Create a new file with the specified file name.
        * Start receiving messages from the client with the file content.
        * Continously check if one of the messages contains an error message.
        * If an error message is found, then the file was not found and the connection must be closed.
        * Print every message received.
        * Print a success message is the entire file was received correctly.
        
    The server allows connection for multiple clients, so after connecting with the first client, it will start looking to accept connections. The first client will let the server know how many other clients there are, and the server will look to make that many connections.
## Author

* **Alejandro Davila** - [adavilamurra](https://github.com/adavilamurra)

