import socket

class ChatClient:
    def __init__(self, server_ip, server_port, username):
        self.server_ip = server_ip
        self.server_port = server_port
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_message("==Joining Chatroom==")
        self.receive_response()

    def send_message(self, message):
        self.client_socket.sendto(f"[({self.server_ip}, {self.server_port}) {self.username}]: {message}".encode(), (self.server_ip, self.server_port))

    def receive_response(self):
        response, server_address = self.client_socket.recvfrom(1024)
        return response.decode()

    def close(self):
        self.client_socket.close()
        
    def run(self):
        while True:
            # Get user input
            message = input("Enter message: ")

            # Send the message to the server
            if (message == "!q" or message == "!quit"):
                self.send_message("==Leaving Chatroom==")
                self.close()
                break
            else:
                self.send_message(message)

            # Receive response from the server
            response = self.receive_response()
            print(response)
