import socket
import logging
import json
import threading
import signal
import os
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

def send_all_files(client_socket, files_directory):
    files = os.listdir(files_directory)  # Get a list of file names
    client_socket.send(str(len(files)).encode('utf-8'))  # Send the number of files

    for file_name in files:
        file_path = os.path.join(files_directory, file_name)
        if os.path.isfile(file_path):  # Ensure it's a file
            with open(file_path, 'rb') as file:
                data = file.read()
                client_socket.send(f"{file_name}:{len(data)}".encode('utf-8'))  # Send file name and size
                status = client_socket.recv(1024)  # Wait for client to be ready
                print(status.decode('utf-8'))
                client_socket.send(data)  # Send file data

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
        logging.info(f"Received username: {username} from {client_socket.getpeername()}")

        # Receive password
        password = client_socket.recv(1024).decode('utf-8')
        logging.info(f"Received password: {password} from {client_socket.getpeername()}")

        # Authenticate
        if authenticate(username, password):
            client_socket.send("Authentication successful!".encode('utf-8'))
        else:
            client_socket.send("Authentication failed!".encode('utf-8'))
            
        option = client_socket.recv(1024).decode('utf-8')
        logging.info(f"Received option: {option} from {client_socket.getpeername()}")
        if option == "logout":
            logging.info(f"{client_socket.getpeername()} logging out")
            return
        elif option == "download":
            logging.info(f"{client_socket.getpeername()} downloading")
        elif option == "upload"	:
            logging.info(f"{client_socket.getpeername()} uploading")
        elif option == "batch download":
            logging.info(f"{client_socket.getpeername()} batch downloading")
            current_directory = os.path.dirname(os.path.abspath(__file__))
            files_directory = os.path.join(current_directory, 'files')
            send_all_files(client_socket, files_directory)
        elif option == "chatting":
            logging.info(f"{client_socket.getpeername()} chatting")
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
            client_thread.join()
            logging.info(f"Closed connection from {addr}")

        except socket.error as e:
            logging.error(f"Socket error: {e}")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL) # allows Ctrl-C to interrupt
    main()
