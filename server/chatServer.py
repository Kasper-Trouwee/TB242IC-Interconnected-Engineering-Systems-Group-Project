from email import message
import socket
import time
import datetime
import os

class ChatServer:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.address, self.port))
        self.run()
    
    def send_message(self, message, addr):
        self.sock.sendto(message.encode(), addr)
    
    def receive_message(self):
        data, addr = self.sock.recvfrom(1024)
        return data.decode(), addr
    

    def run(self):
        print('UDP chat server is running on {}:{}'.format(self.address, self.port))
        
        while True:
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            data, addr = self.receive_message()
            message = f"[{time.strftime('%H:%M:%S', time.localtime())}] {data}"
            
            file_path = os.path.join("chat_log", current_date + ".txt")
            
            with open(file_path, "a") as file:
                file.write(message + "\n")
            
            self.send_message(message, addr)

