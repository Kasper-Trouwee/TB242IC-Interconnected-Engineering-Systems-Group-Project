import os

class UploadDownloadClient:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def download_file(self, filename_on_server):
        print(f"Downloading {filename_on_server}...")
        self.client_socket.send(filename_on_server.encode('utf-8'))
        file_info = self.client_socket.recv(1024).decode('utf-8')
        file_name, file_size = file_info.split(':')
        file_size = int(file_size)
        self.client_socket.send("ready".encode('utf-8'))  # Tell the server we're ready to receive the file

        # Ensure the client receives the entire file
        data = b''
        while len(data) < file_size:
            packet = self.client_socket.recv(1024)
            if not packet:
                break
            data += packet

        file_path = os.path.join('local_files', file_name)  # Create the file path within the 'files' folder

        with open(file_path, 'wb') as file:  # Write the file data to a new file
            file.write(data)
        self.client_socket.send("done".encode('utf-8'))  # Tell the server we're done to receive the file

    def upload_file(self, filename_local):
        print(f"Uploading {filename_local}...")
        self.send_file_data(filename_local)

    def receive_file_data(self):
        data, _ = self.client_socket.recvfrom(1024)
        return data

    def save_file_locally(self, filename, file_data):
        local_file_path = os.path.join('local_files', filename)
        with open(local_file_path, 'wb') as file:
            file.write(file_data)
        print(f"{filename} downloaded successfully.")

    def read_local_file(self, filename):
        local_file_path = os.path.join('local_files', filename)
        with open(local_file_path, 'rb') as file:
            return file.read()

    def send_file_data(self, file_name):
        file_path = os.path.join('local_files', file_name)
        if os.path.isfile(file_path):  # Ensure it's a file
            file_size = os.path.getsize(file_path)
            if file_size > 10 * 1024 * 1024:  # Check if file size is larger than 10MB
                print(f"File {file_name} is too large to send.")
                self.client_socket.send(f"{file_name}:{-1}".encode('utf-8'))  # Send file name and size
                status = self.client_socket.recv(1024).decode('utf-8')  # Wait for client to be ready
            else :
                with open(file_path, 'rb') as file:
                    data = file.read()
                    self.client_socket.send(f"{file_name}:{len(data)}".encode('utf-8'))  # Send file name and size
                    
                    status = self.client_socket.recv(1024).decode('utf-8')  # Wait for client to be ready
                    if status == "ready":
                        self.client_socket.send(data)  # Send file data
                    else:
                        print(f"Client not ready: {status}")
                        return

            status = self.client_socket.recv(1024).decode('utf-8') # wait for client to be done
            print("File uploaded successfully.")

    def batch_download(self):
        num_files = int(self.client_socket.recv(1024).decode('utf-8'))  # Get the number of files

        print(f"Downloading {num_files} files...")

        for _ in range(num_files):
            file_info = self.client_socket.recv(1024).decode('utf-8')
            file_name, file_size = file_info.split(':')
            print(f"Downloading {file_name}...")
            file_size = int(file_size)
            self.client_socket.send("ready".encode('utf-8'))  # Tell the server we're ready to receive the file

            # Ensure the client receives the entire file
            if file_size == -1: # File is too large
                print(f"File {file_name} is too large to recieve.")
            else:
                data = b''
                while len(data) < file_size:
                    packet = self.client_socket.recv(1024)
                    if not packet:
                        break
                    data += packet

                file_path = os.path.join('local_files', file_name)  # Create the file path within the 'files' folder

                with open(file_path, 'wb') as file:  # Write the file data to a new file
                    file.write(data)
                    print(f"{file_name} downloaded successfully.")
                
            self.client_socket.send("done".encode('utf-8'))  # Tell the server we're done receiving the file

        print("All files have been downloaded.")

    def choose_files(self, option):
        if option == 'local':
            local_files_directory = "local_files"
            print("Local Files:")
            return self.show_files(local_files_directory)

        elif option == 'server':
            server_files_directory = os.path.join("..", "server", "server_files" )
            full_path = os.path.abspath(server_files_directory)
            print("Server Files:")
            return self.show_files(full_path)

    def show_files(self, files_directory):
        files = [filename for filename in os.listdir(files_directory) if not filename.startswith('.')]
        for i, filename in enumerate(files):
            print(f"{i+1}. {filename}")
        while True:
            selected_file = input("Enter the number of the file: ")
            if selected_file.isdigit() and 1 <= int(selected_file) <= len(files):
                return files[int(selected_file) - 1]
            else:
                print("Invalid file number. Please enter a valid number.")
                
