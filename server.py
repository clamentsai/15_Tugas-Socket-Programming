import socket
import threading
import queue
from users import register_user, login_user, check_username_exists

messages = queue.Queue()

clients = []

usernames = {}

SERVER_PASSWORD = "12345"

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Gunakan IP Address Local device dengan cara ambil di ipconfig, dan port setting 
server.bind(("192.168.100.170", 9999))

# File untuk menyimpan riwayat pesan
chat_file = "chat.txt"

def save_message_to_file(message):
    with open(chat_file, "a") as file:
        file.write(message + "\n")

def load_chat_history():
    try:
        with open(chat_file, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []  

def send_chat_history(addr):
    history = load_chat_history()
    for line in history:
        server.sendto(line.strip().encode(), addr)

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass 

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            decoded_message = message.decode()

            if addr not in clients:
                if decoded_message.startswith("PASSWORD:"):
                    password = decoded_message.split(":")[1]
                    if password == SERVER_PASSWORD:
                        server.sendto("PASSWORD_OK".encode(), addr)
                    else:
                        server.sendto("PASSWORD_WRONG".encode(), addr)
                
                elif decoded_message.startswith("SIGNUP:"):
                    _, username, password = decoded_message.split(":")
                    if check_username_exists(username):
                        server.sendto("USERNAME_TAKEN".encode(), addr)
                    else:
                        if register_user(username, password):
                            usernames[addr] = username
                            clients.append(addr)
                            print(f"{username} has registered to the server")
                            server.sendto("SIGNUP_SUCCESS".encode(), addr)
                        else:
                            server.sendto("SIGNUP_FAILED".encode(), addr)
                
                elif decoded_message.startswith("SIGNIN:"):
                    _, username, password = decoded_message.split(":")
                    if login_user(username, password):
                        if username in usernames.values():
                            server.sendto("USERNAME_TAKEN".encode(), addr)
                        else:
                            usernames[addr] = username
                            clients.append(addr)
                            print(f"{username} has logged in to the server")
                            server.sendto("SIGNIN_SUCCESS".encode(), addr)
                            send_chat_history(addr) # Kirim pesan ke semua client bahwa user baru telah bergabung
                            for client in clients:
                                server.sendto(f"{username}: has joined to the server".encode(), client)
                    else:
                        server.sendto("SIGNIN_FAILED".encode(), addr)

                elif decoded_message.endswith("has left the chat"):
                    clients.remove(client)                        

            else:
                # Proses ketika client meninggalkan chat
                if decoded_message.endswith("has left the chat"):
                    name = usernames[addr]
                    print(f"{name} has left the chat")
                    # Hapus client dari daftar clients dan usernames
                    del usernames[addr]
                    clients.remove(addr)
                    for client in clients:
                        server.sendto(f"{name}: has left the chat".encode(), client)
                # Kirim pesan biasa ke semua client
                else:  
                    # Mencetak pesan yang dikirim client ke layar                      
                    print(decoded_message)
                    save_message_to_file(decoded_message) # Menyimpan pesan ke txt
                    for client in clients:
                        try:
                            server.sendto(message, client)
                        except:
                            clients.remove(client) 

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

print("ArKun server is listening...")
t1.start()
t2.start()