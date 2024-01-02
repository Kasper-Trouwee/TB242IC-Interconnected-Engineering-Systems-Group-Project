class OptionMenu:
    """
    Represents a menu of options for a client.

    Attributes:
        client_socket (socket): The client socket used for communication.
        username (str): The username of the client.
    """

    def __init__(self, client_socket, username):
        self.client_socket = client_socket
        self.username = username

    def choose_option(self):
        """
        Displays the available options and prompts the user to choose an option.

        Returns:
            None
        """
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
        """
        Validates and returns the received option.

        Args:
            option (str): The received option.

        Returns:
            str: The validated option or "Invalid option" if the option is not valid.
        """
        options = {
            "logout",
            "download",
            "upload",
            "batch download",
            "chatting"
        }
        return option if option in options else "Invalid option"
