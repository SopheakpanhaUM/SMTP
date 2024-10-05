import socket
import threading
import os
from dotenv import load_dotenv
from colorama import Fore

load_dotenv()

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000
clients = []

def broadcast_message(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message: {e}")

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                broadcast_message(message, client_socket)
                send_email_notification(message, client_socket)
        except Exception as e:
            print(f"Error: {e}")
            clients.remove(client_socket)
            client_socket.close()
            break

def send_email_notification(message, client_socket):
    import smtplib
    from email.mime.text import MIMEText
    

    sender_email = os.getenv("Sender_Email")
    sender_password = os.getenv("Sender_Password")
    recipient_email = os.getenv("Recipient_Email")
    
    msg = MIMEText(f"New message received: {message}")
    msg['Subject'] = "New Message Notification"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print(Fore.BLUE + "Server started, waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"{Fore.GREEN}New connection from {addr}")
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
