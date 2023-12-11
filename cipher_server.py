import socket

class CipherServer:
    def __init__(self, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', port))
        server_socket.listen(1)

        print(f"Cipher Server now listening on port {port}.")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}.")

            while True:
                data = client_socket.recv(1024)
                print(f"Received data from {client_address}.")
                if not data:
                    client_socket.close()
                    print(f"Connection from {client_address} closed.")
                    break
                client_socket.send(self.cipher(data))
    
    def cipher(self, data):
        data = data.decode('utf-8')
        cipher_data = ""
        for char in data[:-1]:
            cipher_data += chr((ord(char) + 1))
        cipher_data += '\n'
        return cipher_data.encode('utf-8')

if __name__ == "__main__":
    cipher_server = CipherServer(5001)