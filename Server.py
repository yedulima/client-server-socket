import socket
import threading
from time import sleep

class Server:
    clients = []
    messages = []
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_open = True
        self.HOST: str = host
        self.PORT: int = port
        self.ADDR: tuple = (self.HOST, self.PORT)

    def startServer(self):
        print("[SERVER] Connected waiting for clients...")
        self.server.bind(self.ADDR)
        self.server.listen()
        while self.server_open:
            connection, address = self.server.accept()
            Thread = threading.Thread(target=self.handleClient, args=(connection, address))
            Thread.start()
            print(f"[SERVER] {threading.activeCount() - 1} clients connected.")

    def closeServer(self):
        self.server.close()
        self.server_open = False

    @classmethod
    def addNewClient(cls, port: int, name: str):
        cls.clients.append({port: name})
        cls.messages.append({port: None})

    @classmethod
    def replaceClientMessage(cls, port: int, message: str) -> None:
        for client in range(len(cls.messages)):
            if port in cls.messages[client]:
                cls.messages[client][port] = message
                return None

    @classmethod
    def sendChat2Client(cls, connection):
        for client in range(len(cls.messages)):
            client_port = [port for port in cls.messages[client]][0]
            client_name = [cls.clients[name][client_port] for name in range(len(cls.clients)) if client_port in cls.clients[name]][0]
            final_message = f"[{client_name}] {cls.messages[client][client_port]}"
            connection.send(final_message.encode())
            sleep(.2)

    def handleClient(self, connection, address: tuple):
        print(f"[SERVER] {address} conected to the server!")
        client_name = connection.recv(64).decode()
        self.addNewClient(address[1], client_name)
        while True:
            message_lenght = connection.recv(64).decode()
            if message_lenght:
                message_lenght = int(message_lenght)
                message = connection.recv(message_lenght).decode()
                if message == 'quit':
                    break
                self.replaceClientMessage(address[1], message)
                self.sendChat2Client(connection)
                print(f"[{address[1]}] {message}")
        print(f"[SERVER] {[self.clients[client][address[1]] for client in range(len(self.clients)) if address[1] in self.clients[client]]} disconnected to the server.")
        connection.close()

if __name__ == "__main__":
    server = Server()
    server.startServer()
