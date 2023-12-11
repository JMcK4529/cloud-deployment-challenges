import socket

class HTTPServer:
    def __init__(self, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', port))
        server_socket.listen(1)
        self.request = []

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}.")
            
            while True:
                print("Request so far: ", [entry for entry in self.request])
                input = client_socket.recv(1024)
                print(f"Received data from {client_address}.")
                if not input:
                    client_socket.close()
                    break
                
                print("input: ", input.decode("utf-8"))
                if "\r\n".encode("utf-8") in input:
                    print("split: ", [line.decode("utf-8") for line in input.split("\r\n".encode("utf-8"))])
                    [self.request.append(line.decode("utf-8")) for line in input.split("\r\n".encode("utf-8")) if line.decode("utf-8") != ""]
                    if (method:= self.request[0].split(" ")[0]) == "GET":
                        print("GET detected.")
                        client_socket.send(self.respond())
                    else:
                        print(f"method: //{method}//")
                # if input.decode('utf-8').strip() == "":
                #     print("Double return captured.")
                #     if (method:= self.request[0].decode('utf-8').split(" ")[0]) == "GET":
                #         print("GET detected.")
                #         client_socket.send(self.respond())
                #     else:
                #         print(f"method: //{method}//")

                # else:
                #     self.request.append(input)
                #     print("Data appended to response list.")


    def respond(self):
        request_line = self.request[0].split(" ")
        print("request line: ", request_line)
        if request_line[2] != "HTTP/1.1":
            return "HTTP/1.1 500 Internal Server Error\r\n".encode("utf-8")
        if request_line[0] == "GET":
            return self.get(request_line[1]).encode("utf-8")
        else:
            return "HTTP/1.1 400 Bad Request\r\n".encode("utf-8")

    def get(self, address):
        try:
            if (address := address[1:]) == "":
                address = "index"
            with open(f"html/{address}.html", "r") as file:
                lines = file.readlines()
            response = ["HTTP/1.1 200 OK\r\n\r\n"]
            for line in lines:
                response.append(line)
            return "\r".join(response) + "\r\n"
        except:
            return "HTTP/1.1 400 Bad Request\r\n"
# Request
# Request-Line   = Method SP Request-URI SP HTTP-Version CRLF
# Method         = "GET" or "POST"

# Response
# Status-Line = HTTP-Version SP Status-Code SP Reason-Phrase CRLF
# Status-Codes
# "100" : Continue
# "200" : OK
# "300" : Multiple Choices
# "400" : Bad Request
# "500" : Internal Server Error

if __name__ == "__main__":
    server = HTTPServer(5001)