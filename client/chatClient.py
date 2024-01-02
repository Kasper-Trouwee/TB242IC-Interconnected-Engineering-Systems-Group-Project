import socket
import threading

class ChatClient:
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
