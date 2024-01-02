import socket
import threading

class ChatClient:
    """
    A class representing a chat client.

    Attributes:
        server_ip (str): The IP address of the chat server.
        server_port (int): The port number of the chat server.
        username (str): The username of the client.
        client_socket (socket.socket): The socket object for communication with the server.
        running (bool): Flag indicating whether the client is running.

    Methods:
        send_message: Sends a message to the chat server.
        receive_response: Receives a response from the chat server.
        close: Closes the client socket.
        receive_thread: Thread function for receiving messages from the server.
        input_thread: Thread function for reading user input and sending messages to the server.
        run: Starts the client by creating and starting the receive and input threads.
    """

    def __init__(self, server_ip, server_port, username):
        self.server_ip = server_ip
        self.server_port = server_port
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_message("==Joining Chatroom==")
        self.running = True

    def send_message(self, message):
        self.client_socket.sendto(f"[({self.server_ip}, {self.server_port}) {self.username}]: {message}".encode(), (self.server_ip, self.server_port))

    def receive_response(self):
        response, server_address = self.client_socket.recvfrom(1024)
        return response.decode()

    def close(self):
        self.client_socket.close()

    def receive_thread(self):
        while self.running:
            response = self.receive_response()
            print(response)

    def input_thread(self):
        while self.running:
            message = input()

            if message == "!q" or message == "!quit":
                self.send_message("==Leaving Chatroom==")
                self.running = False
            else:
                self.send_message(message)


    def run(self):
        receive_thread = threading.Thread(target=self.receive_thread)
        input_thread = threading.Thread(target=self.input_thread)

        receive_thread.start()
        input_thread.start()

        receive_thread.join()
        input_thread.join()
        self.close()
