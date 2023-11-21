import socketserver

class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        self.request.sendall(data.upper())

if __name__ == "__main__":
    server_address = ('localhost', 9090)
    server = socketserver.TCPServer(server_address, MyHandler)
    print("Server listening on {}:{}".format(*server_address))
    server.serve_forever()