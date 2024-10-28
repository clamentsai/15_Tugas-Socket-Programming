import socket
import threading
import random
from RC4 import encrypt

# Membuat client socket menggunakan protokol UDP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Mengikat client ke alamat localhost dengan port acak antara 8000 hingga 9000
client.bind(("192.168.110.38", random.randint(8000, 9000)))

# Meminta user untuk memasukkan password
password_correct = False
while not password_correct:
    password = input("Enter server password: ")
    client.sendto(f"PASSWORD:{password}".encode(), ("192.168.110.38", 9999))
    message, _ = client.recvfrom(1024)
    if message.decode() == "PASSWORD_OK":
        password_correct = True
        print("Password accepted!")
    else:
        print("Wrong password, please try again.")

# Meminta user untuk memasukkan nickname (username) dan memastikan unik
username_accepted = False
while not username_accepted:
    name = input("Nickname: ")
    client.sendto(f"SIGNUP_TAG:{name}".encode(), ("192.168.110.38", 9999))
    message, _ = client.recvfrom(1024)
    if message.decode() == "USERNAME_TAKEN":
        print("Username already taken, please choose a different one.")
    else:
        print(f"Welcome, {name}!")
        username_accepted = True

# Key untuk enkripsi
Key = "AreaKuning"

# Fungsi untuk menerima pesan dari server
def receive():
    while True:
        try:
            # Menerima pesan dari server, maksimal 1024 bytes
            message, _ = client.recvfrom(1024)
            message_decrypted = encrypt(Key, message)
            # Menampilkan pesan yang diterima (decode untuk mengubah byte ke string)
            print(message_decrypted.decode())
        except:
            pass  # Jika ada error, lewati

# Membuat thread untuk menjalankan fungsi receive
t = threading.Thread(target=receive)
t.start()

# Loop untuk mengirim pesan ke server
while True:
    message = input("")  # Meminta input pesan dari user
    message_ciphertext = encrypt(Key, message)
    if message == "!q":
        exit()  # Keluar dari program jika user mengetik "!q"
    else:
        # Mengirim pesan ke server dengan format "nama: pesan"
        client.sendto(f"{name}: {message_ciphertext}".encode(), ("192.168.110.38", 9999))
