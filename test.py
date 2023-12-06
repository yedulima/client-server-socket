import socket
import threading
import os
from time import sleep

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connectToServer(self, server_host: str, port: int):

        clean_terminal()

        # Define server address
        ADDR: tuple = (server_host, port)
        
        # Connect to the server
        self.client.connect(ADDR)

        client_name = input("Enter with your name: ").title()
        self.client.send(client_name.encode())

        chat = threading.Thread(target=self.loadChat)
        chatSys = threading.Thread(target=self.chatSystem)
        chat.start()
        chatSys.start()

    def sendMessage(self, message: str):
        message = message.encode()
        send_lenght = str(len(message)).encode()
        send_lenght += b' ' * (64 - len(send_lenght))
        self.client.send(send_lenght)
        self.client.send(message)
        if message.decode() == "quit":
            print("[SERVER] Disconnected.")
            return False
        return True

    def chatSystem(self):
        while True:
            sleep(.5)
            message = input("Enter a message: ")
            self.sendMessage(message)

    def loadChat(self):
        while True:
            message = self.client.recv(64).decode()
            print(message)

if __name__ == "__main__":

    clean_terminal = lambda: os.system("cls") if os.name == 'nt' else os.system("clear")

    client = Client()
    client.connectToServer("127.0.1.1", 8080)