from chatClient import ChatClient


class OptionMenu:
    
    def __init__(self, client_socket, username):
        self.client_socket = client_socket
        self.username = username
        pass

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
        options = {
            "logout",
            "download",
            "upload",
            "batch download",
            "chatting"
        }
        return option if option in options else "Invalid option"
