// Server side C/C++ program to demonstrate Socket programming 
// Here's some include statements that might be helpful for you
#include <string> 
#include <cstring>
#include <iostream>
#include <stdlib.h>
#include <sys/socket.h> 
#include <netdb.h>
#include <netinet/in.h> 
#include <arpa/inet.h>
#include <unistd.h>

void error(const char *msg)
{
    perror(msg);                                                                                                                                                                 exit(1);
}

int main(int argc, char const *argv[]) 
{ 
	// check to see if user input is valid
	char socket_read_buffer[1024];
	
	// TODO: Fill out the server ip and port

	std::string server_ip = "127.0.0.1";
	std::string server_port = "5600";

	int opt = 1;
	int client_fd = -1;

	// TODO: Create a TCP socket()
	int sockfd = socket(AF_INET,SOCK_STREAM,0);
        int newsockfd,n;
	// Enable reusing address and port
	if (setsockopt(client_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) { 
		return -1;
	}

	// Check if the client socket was set up properly
	if(client_fd == -1){
		printf("Error- Socket setup failed");
		return -1;
	}
	
	// Helping you out by pepping the struct for connecting to the aws server
	struct addrinfo hints;
	struct addrinfo *server_addr;
	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	getaddrinfo(server_ip.c_str(), server_port.c_str(), &hints, &server_addr);
        connect(sockfd,server_addr->ai_addr,server_addr->ai_addrlen);
        listen(sockfd,5);
	socklen_t ai_addrlen = sizeof(server_addr);
	// TODO: Send() the user input to the aws server
        while(1) {
            char buffer[256];
            newsockfd = accept(sockfd,
                        (struct sockaddr *) &server_addr,
                        &ai_addrlen);
            if (newsockfd < 0)
                error("ERROR on accept");
            bzero(buffer,256);

            n = read(newsockfd,buffer,255);
            if (n < 0)
                error("ERROR reading from socket");
            //printf("Here is the message: %s\n",buffer);
            n = write(newsockfd,"I got it",8);
            if (n < 0)
                error("ERROR writing to socket");
            close(newsockfd);
        }
	// TODO: Recieve any messages from the aws server and print it here. Don't forget to make sure the string is null terminated!
	int len = recv(client_fd, socket_read_buffer, sizeof(socket_read_buffer), 0);
	socket_read_buffer[len] = '\0';
	printf("%s\n", socket_read_buffer);
	// TODO: Close() the socket
	close(sockfd);
	return 0; 
} 
