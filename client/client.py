import socket
from chatClient import ChatClient

from optionMenu import OptionMenu


def call_option(option, username):
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
    elif option == "download":
        print("download")
    elif option == "upload":
        print("upload")
    elif option == "batch download":
        print("batch download")
    elif option == "chatting":
        # Server IP address and port
        SERVER_IP = 'localhost'
        SERVER_PORT = 8000
        
        # Create a UDP client instance
        client = ChatClient(SERVER_IP, SERVER_PORT, username)
        client.run()
        del client

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
                menu = OptionMenu(client_socket, username)
                menu.choose_option()
                chosenOption = client_socket.recv(1024).decode('utf-8')
                chosenOption = menu.receive_option(chosenOption)
                call_option(chosenOption, username)
            else :
                print("Exiting Program...")
                exit(1)

    except ConnectionError as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    main()
