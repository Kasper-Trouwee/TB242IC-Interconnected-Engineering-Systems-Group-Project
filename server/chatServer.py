from email import message
import socket

class ChatServer:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.address, self.port))
    
    def send_message(self, message, addr):
        self.sock.sendto(message.encode(), addr)
    
    def receive_message(self):
        data, addr = self.sock.recvfrom(1024)
        return data.decode(), addr
    
    def run(self):
        print('UDP chat server is running on {}:{}'.format(self.address, self.port))
        
        while True:
            data, addr = self.receive_message()
            print(data)
            
            self.send_message(data, addr)
