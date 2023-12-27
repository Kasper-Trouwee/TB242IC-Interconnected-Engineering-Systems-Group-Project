import socket
import logging
import json

def authenticate(username, password):
    users = json.load(open("authentication.json"))
    
    # loop every user
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True
    return False

def handle_client(client_socket):
    try:
        # Receive username
        username = client_socket.recv(1024).decode('utf-8')
        logging.info(f"Received username: {username}")

        # Receive password
        password = client_socket.recv(1024).decode('utf-8')
        logging.info(f"Received password: {password}")

        # Authenticate
        if authenticate(username, password):
            client_socket.send("Authentication successful!".encode('utf-8'))
        else:
            client_socket.send("Authentication failed!".encode('utf-8'))

    except socket.error as e:
        logging.error(f"Socket error: {e}")
        client_socket.send("An error occurred during authentication.".encode('utf-8'))

    finally:
        # Close the connection
        client_socket.close()

def main():
    logging.basicConfig(level=logging.INFO)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 5555))
    server_socket.listen(1)  # Listen for one incoming connection

    logging.info("Server listening on port 5555...")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            logging.info(f"Accepted connection from {addr}")

            handle_client(client_socket)

        except socket.error as e:
            logging.error(f"Socket error: {e}")

if __name__ == "__main__":
    main()
