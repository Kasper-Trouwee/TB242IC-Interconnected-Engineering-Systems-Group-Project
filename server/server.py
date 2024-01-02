import socket
import logging
import json
import threading

from chatServer import ChatServer

def authenticate(username, password):
    """
    Authenticates the user by checking if the provided username and password match any user in the authentication database.

    Args:
        username (str): The username to authenticate.
        password (str): The password to authenticate.

    Returns:
        bool: True if the authentication is successful, False otherwise.
    """
    users = json.load(open("authentication.json"))
    
    # loop every user
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True
    return False

def handle_client(client_socket):
    """
    Handle a client connection by performing authentication.

    Args:
        client_socket (socket): The client socket object.

    Returns:
        None
    """
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
            
        option = client_socket.recv(1024).decode('utf-8')
        logging.info(f"Received option: {option}")
        if option == "logout":
            logging.info("Client logging out")
        elif option == "download":
            logging.info("Client downloading")
        elif option == "upload"	:
            logging.info("Client uploading")
        elif option == "batch download":
            logging.info("Client batch downloading")
        elif option == "chatting":
            logging.info("Client chatting")
            client_socket.send("chatting".encode('utf-8'))

    except socket.error as e:
        logging.error(f"Socket error: {e}")
        client_socket.send("An error occurred during authentication.".encode('utf-8'))
    finally:
        # Close the connection
        client_socket.close()

def main():
    """
    Main function that starts the server and listens for incoming connections.

    This function initializes a server socket, binds it to a specific address and port,
    and listens for incoming connections. Once a connection is established, it calls
    the handle_client function to handle the client's requests.

    Raises:
        socket.error: If there is an error with the socket.

    """
    logging.basicConfig(level=logging.INFO)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 5555))
    server_socket.listen(1)  # Listen for one incoming connection

    logging.info("Server listening on port 5555...")
    
    chat_tread = threading.Thread(target=ChatServer, args=('localhost', 8000))
    chat_tread.start()

    
    while True:
        try:
            client_socket, addr = server_socket.accept()
            logging.info(f"Accepted connection from {addr}")

            # Create a new thread for each client connection
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

        except socket.error as e:
            logging.error(f"Socket error: {e}")

if __name__ == "__main__":
    main()
