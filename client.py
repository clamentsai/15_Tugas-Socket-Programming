import socket
import threading
import random
from RC4 import encrypt

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Gunakan IP Address Client sendiri, (memakai randint untuk port dikarenakan server dan client dijalankan di satu device yang sama)
client.bind(("192.168.100.170", random.randint(8000, 9000))) 

# Key untuk enkripsi
Key = "AreaKuning"

# Variabel untuk menyimpan username
username = ""

# Meminta user untuk memasukkan password
password_correct = False
while not password_correct:
    password = input("Enter server password: ")
    client.sendto(f"PASSWORD:{password}".encode(), ("192.168.100.170", 9999)) # Untuk sendto, gunakan IP Address Server dan port Server juga
    message, _ = client.recvfrom(1024)
    if message.decode() == "PASSWORD_OK":
        password_correct = True
        print("Password accepted!")
    else:
        print("Wrong password, please try again.")

# Memilih antara Sign Up atau Sign In
print("Choose an option:")
print("1. Sign Up")
print("2. Sign In")
choice = input("Enter your choice (1/2): ")

if choice == '1':
    # Proses Sign Up
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        client.sendto(f"SIGNUP:{username}:{password}".encode(), ("192.168.100.170", 9999)) # Untuk sendto, gunakan IP Address Server dan port Server juga
        message, _ = client.recvfrom(1024)
        if message.decode() == "USERNAME_TAKEN":
            print("Username already taken, please choose a different one.")
        elif message.decode() == "SIGNUP_SUCCESS":
            print(f"Welcome, {username}! You have successfully registered.")
            break
        else:
            print("Registration failed. Please try again.")

elif choice == '2':
    # Proses Sign In
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        client.sendto(f"SIGNIN:{username}:{password}".encode(), ("192.168.100.170", 9999)) # Untuk sendto, gunakan IP Address Server dan port Server juga
        message, _ = client.recvfrom(1024)
        if message.decode() == "USERNAME_TAKEN":
            print("Username already login, please choose a different one.")
        elif message.decode() == "SIGNIN_SUCCESS":
            print(f"Welcome back, {username}!")
            break
        else:
            print("Login failed. Please check your username and password.")

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            name, encrypted_message = message.decode().split(": ", 1)
            if encrypted_message == "has left the chat":
                print(f"{name} has left the chat")
            elif encrypted_message == "has joined to the server":
                if name != username:
                    print(f"{name} has joined to the server")
            else:
                decrypted_message = encrypt(Key, encrypted_message)
                print(f"{name}: {decrypted_message}")
        except:
            pass  

t = threading.Thread(target=receive)
t.start()

while True:
    message = input("")  
    if message == "quit":
        client.sendto(f"{username}: has left the chat".encode(), ("192.168.100.170", 9999)) # Untuk sendto, gunakan IP Address Server dan port Server juga
        exit()  
    else:
        # Mengirim pesan ke server dengan format "nama: pesan"
        encrypted_message = encrypt(Key, message)
        client.sendto(f"{username}: {encrypted_message}".encode(), ("192.168.100.170", 9999)) # Untuk sendto, gunakan IP Address Server dan port Server juga