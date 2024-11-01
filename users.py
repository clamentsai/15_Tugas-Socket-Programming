import csv
from RC4 import encrypt

USER_FILE = 'users.csv'

def initialize_user_file():
    """Membuat file CSV untuk menyimpan user jika belum ada"""
    try:
        with open(USER_FILE, 'r') as file:
            pass  # File sudah ada
    except FileNotFoundError:
        with open(USER_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'encrypted_password'])

def register_user(username, password, key='AreaKuning'):
    """Mendaftarkan user baru"""
    # Cek apakah username sudah ada
    if check_username_exists(username):
        return False
    
    # Enkripsi password menggunakan RC4
    encrypted_password = encrypt(key, password)
    
    # Tambahkan user ke file CSV
    with open(USER_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, encrypted_password])
    
    return True

def login_user(username, password, key='AreaKuning'):
    """Autentikasi user"""
    # Enkripsi password yang diinput
    encrypted_input_password = encrypt(key, password)
    
    # Baca file CSV untuk verifikasi
    with open(USER_FILE, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Lewati header
        for row in reader:
            if row[0] == username and row[1] == encrypted_input_password:
                return True
    
    return False

def check_username_exists(username):
    """Cek apakah username sudah ada"""
    with open(USER_FILE, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Lewati header
        for row in reader:
            if row[0] == username:
                return True
    return False

# Inisialisasi file saat modul diimpor
initialize_user_file()
