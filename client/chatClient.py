import socket

class ChatClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, message, username):
        self.client_socket.sendto(f"({self.server_ip}, {self.server_port})[{username}]: {message}".encode(), (self.server_ip, self.server_port))

    def receive_response(self):
        response, server_address = self.client_socket.recvfrom(1024)
        return response.decode()

    def close(self):
        self.client_socket.close()
