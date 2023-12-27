class OptionMenu:
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
        print("chatting")

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
                switch = {
                    "logout": self.logout,
                    "download": self.download,
                    "upload": self.upload,
                    "batch download": self.batch_download,
                    "chatting": self.chatting
                }
                switch.get(option, lambda: print("Invalid option"))()
                break
            else:
                print("Invalid option number. Please choose a valid option number.")
