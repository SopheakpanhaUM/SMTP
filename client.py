import socket
import threading
from colorama import Fore

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"\nNew message: {message}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            client_socket.close()
            break

def send_messages(client_socket, client_name):
    while True:
        message = input(f"{client_name}: ")
        if message:
            full_message = f"{client_name}: {message}"
            client_socket.send(full_message.encode('utf-8'))

def start_client():
    print(Fore.GREEN + "Welcome To Chat Message!!")
    client_name = input(Fore.MAGENTA + "Enter your name: ")  

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    send_messages(client_socket, client_name)

if __name__ == "__main__":
    start_client()
