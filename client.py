import socket, threading, random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("192.168.100.170", random.randint(8000, 9000))) # Different port

name = input("Nickname: ")

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass

t = threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG:{name}".encode(), ("192.168.100.24", 9999))

while True:
    message = input("")
    if message == "exit":
        exit()
    else:
        client.sendto(f"{name}: {message}".encode(), ("192.168.100.24", 9999))