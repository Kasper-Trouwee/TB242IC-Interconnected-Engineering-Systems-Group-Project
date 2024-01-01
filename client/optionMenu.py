from chatClient import ChatClient


class OptionMenu:
    
    def __init__(self, client_socket, username):
        self.client_socket = client_socket
        self.username = username
        pass
    
    """
    Represents a menu of options for the user to choose from.
    """

    def logout(self):
        print("logout")

    def download(self):
        print("download")

    def upload(self):
        print("upload")

    def batch_download(self):
        print("batch download")

    def chatting(self):
        # Server IP address and port
        SERVER_IP = 'localhost'
        SERVER_PORT = 8000
        
        # Create a UDP client instance
        client = ChatClient(SERVER_IP, SERVER_PORT)
        
        while True:
            # Get user input
            message = input("Enter message: ")

            # Send the message to the server
            client.send_message(message, self.username)

            # Receive response from the server
            response = client.receive_response()
            print(response)

    def choose_option(self):
        options = {
            1: "logout",
            2: "download",
            3: "upload",
            4: "batch download",
            5: "chatting"
        }

        print("Options:")
        for num, option in options.items():
            print(f"{num}. {option}")

        while True:
            option_input = input("Choose an option number: ")

            if not option_input.isdigit():
                print("Invalid input. Please enter a valid option number.")
                continue

            option_num = int(option_input)
            option = options.get(option_num)
            

            if option:
                self.client_socket.send(option.encode('utf-8'))
                break
            else:
                print("Invalid option number. Please choose a valid option number.")
                
    def receive_option(self, option):
        switch = {
            "logout": self.logout,
            "download": self.download,
            "upload": self.upload,
            "batch download": self.batch_download,
            "chatting": self.chatting
        }
        switch.get(option, lambda: print("Invalid option"))()
