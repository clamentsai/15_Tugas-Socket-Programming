import socket  # Import modul untuk membuat koneksi jaringan
import threading  # Import modul untuk membuat thread (multitasking)
import queue  # Import modul untuk queue, struktur data FIFO (First In, First Out)

# Queue untuk menyimpan pesan yang diterima
messages = queue.Queue()

# Daftar untuk menyimpan alamat dari semua client yang terkoneksi
clients = []

# Daftar untuk menyimpan username yang telah terdaftar
usernames = {}

# Password server (client harus memasukkan ini dengan benar)
SERVER_PASSWORD = "12345"

# Membuat server socket menggunakan protokol UDP (SOCK_DGRAM)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Mengikat server ke alamat localhost dengan port 9999
server.bind(("192.168.110.38", 9999))

# Fungsi untuk menerima pesan dari client
def receive():
    while True:
        try:
            # Menerima pesan dari client, maksimal 1024 bytes
            message, addr = server.recvfrom(1024)
            # Menambahkan pesan dan alamat client ke dalam antrian
            messages.put((message, addr))
        except:
            pass  # Jika ada error, lewati

# Fungsi untuk mengirimkan pesan ke semua client
def broadcast():
    while True:
        # Jika ada pesan di antrian
        while not messages.empty():
            # Mengambil pesan dari antrian
            message, addr = messages.get()
            decoded_message = message.decode()
            print(decoded_message)

            # Jika client baru belum ada di daftar, tambahkan
            if addr not in clients:
                # Memproses pesan pertama (password dan registrasi username)
                if decoded_message.startswith("PASSWORD:"):
                    password = decoded_message.split(":")[1]
                    if password == SERVER_PASSWORD:
                        server.sendto("PASSWORD_OK".encode(), addr)
                    else:
                        server.sendto("PASSWORD_WRONG".encode(), addr)
                elif decoded_message.startswith("SIGNUP_TAG:"):
                    name = decoded_message.split(":")[1]
                    # Cek apakah username sudah digunakan
                    if name in usernames.values():
                        server.sendto("USERNAME_TAKEN".encode(), addr)
                    else:
                        usernames[addr] = name
                        clients.append(addr)
                        server.sendto(f"{name} joined!".encode(), addr)
                        # Kirim pesan ke semua client bahwa user baru telah bergabung
                        for client in clients:
                            server.sendto(f"{name} joined!".encode(), client)
            else:
                # Kirim pesan biasa ke semua client
                for client in clients:
                    try:
                        server.sendto(message, client)
                    except:
                        # Jika ada error saat mengirim ke client tertentu, hapus client dari daftar
                        clients.remove(client) 

# Membuat thread untuk menjalankan fungsi receive dan broadcast secara bersamaan
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

# Memulai kedua thread
t1.start()
t2.start()
