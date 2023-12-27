import socket
import time

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

    except ConnectionError as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    main()
