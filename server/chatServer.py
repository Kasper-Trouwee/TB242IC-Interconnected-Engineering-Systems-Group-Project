import socket
import time
import datetime
import os
import logging

class ChatServer:
    """
    Represents a UDP chat server that allows clients to send and receive messages.

    Attributes:
        address (str): The IP address of the server.
        port (int): The port number on which the server is listening.
        client_address (list): A list of client addresses that are connected to the server.
        sock (socket.socket): The socket object used for communication.
    """

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.client_address = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.address, self.port))
        self.run()

    def send_message(self, message, addr):
        """
        Sends a message to a specific client.

        Args:
            message (str): The message to be sent.
            addr (tuple): The address of the client to send the message to.
        """
        self.sock.sendto(message.encode(), addr)

    def receive_message(self):
        """
        Receives a message from a client.

        Returns:
            tuple: A tuple containing the received message (str) and the address (tuple) of the client.
        """
        data, addr = self.sock.recvfrom(1024)
        return data.decode(), addr

    def send_message_to_all(self, message):
        """
        Sends a message to all connected clients.

        Args:
            message (str): The message to be sent.
        """
        for client in self.client_address:
            self.send_message(message, client)
            
    def send_log_data_to_client(self, addr, file_path):
        """
        Sends the contents of the log file to the client as individual lines.

        Args:
            addr (tuple): The address of the client to send the file data to.
        """
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    self.send_message(line.strip(), addr)

    def run(self):
        """
        Runs the chat server and handles incoming messages from clients.
        """
        logging.info('UDP chat server is running on {}:{}'.format(self.address, self.port))

        while True:
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")

            data, addr = self.receive_message()

            message = f"[{time.strftime('%H:%M:%S', time.localtime())}] {data}"

            file_path = os.path.join("chat_log", current_date + ".txt")

            if addr not in self.client_address:
                self.client_address.append(addr) # Add client address to list of connected clients
                self.send_log_data_to_client(addr, file_path) # Send log data to client

            self.send_message_to_all(message)  # Send message to all connected clients
            
            with open(file_path, "a") as file: # Append message to log file
                file.write(message + "\n")
                
            if "==Leaving Chatroom==" in data:
                self.client_address.remove(addr) # Remove client address from list of connected clients

