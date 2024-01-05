import socket
from chatClient import ChatClient

from menu import Menu
import os


def call_chosen_option(option, client_socket, username):
    """
    Executes the specified option based on the user's input.

    Parameters:
    option (str): The option to execute.
    username (str): The username of the client.

    Returns:
    None
    """
    if option == "logout":
        print("logout")
        exit(1)
    elif option == "download":
        print("download")
        show_files("server")
    elif option == "upload":
        print("upload")
        show_files("local")
    elif option == "batch download":
        batch_download(client_socket)
    elif option == "chatting":
        # Server IP address and port
        SERVER_IP = 'localhost'
        SERVER_PORT = 8000
        
        # Create a UDP client instance
        client = ChatClient(SERVER_IP, SERVER_PORT, username)
        client.run()
        del client
        
def batch_download(client_socket):
    num_files = int(client_socket.recv(1024).decode('utf-8'))  # Get the number of files

    print(f"Downloading {num_files} files...")

    for _ in range(num_files):
        file_info = client_socket.recv(1024).decode('utf-8')
        file_name, file_size = file_info.split(':')
        file_size = int(file_size)
        client_socket.send("ready".encode('utf-8'))  # Tell the server we're ready to receive the file

        # Ensure the client receives the entire file
        data = b''
        while len(data) < file_size:
            packet = client_socket.recv(1024)
            if not packet:
                break
            data += packet

        file_path = os.path.join('local_files', file_name)  # Create the file path within the 'files' folder

        with open(file_path, 'wb') as file:  # Write the file data to a new file
            file.write(data)

    print("All files have been downloaded.")

# Currently not used  
def choose_files():
    print("File options")
    print("1. Local Files")
    print("2. Server Files")

    option = input("Enter 1 for Local Files or 2 for Server Files")

    while option not in ['1', '2']:
        print("Option is invalid. Enter 1 for Local Files or 2 for Server Files")
        option = input("Enter 1 for Local Files or 2 for Server Files")

    return "local" if option == "1" else "server"

def show_files(option):
    if option == 'local':
        local_files_directory = "local_files"
        print("Local Files:")
        files = os.listdir(local_files_directory)
        for filename in files:
            print(filename)
    elif option == 'server':
        server_files_directory = os.path.join("..", "server", "server_files" )
        full_path = os.path.abspath(server_files_directory)
        print("Server Files:")
        files = os.listdir(full_path)
        for filename in files:
            print(filename)

def main():
    """
    Connects to a server, sends username and password, and receives and prints the server's response.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Connect to the server
            server_address = ('127.0.0.1', 5555)
            client_socket.connect(server_address)

            # Input username
            username = input("Enter username: ")
            client_socket.send(username.encode('utf-8'))

            # Input password
            password = input("Enter password: ")
            client_socket.send(password.encode('utf-8'))

            # Receive and print the server's response
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Server response: {response}")
            if response == "Authentication successful!":
                while True:
                    menu = Menu()
                    chosenOption = menu.showMain()
                    client_socket.send(chosenOption.encode('utf-8'))
                    call_chosen_option(chosenOption, client_socket, username)
            else :
                print("Exiting Program...")
                exit(1)

    except ConnectionError as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    main()
