# RC4 Encryption

def keys(key):
    """ Key-scheduling algorithm (KSA) """

    s = [x for x in range(256)]
    j = 0

    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) % 256
        s[i], s[j] = s[j], s[i]  # Swap values

    return s


def prga(s):
    """ Pseudo-random generation algorithm (PRGA) """
    i = 0
    j = 0

    while True:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]  # Swap values
        yield s[(s[i] + s[j]) % 256]


def encrypt(key, plaintext):
    """Encrypt/Decrypt with RC4 using the given key."""

    key = [ord(c) for c in key]
    s = keys(key)
    keystream = prga(s)
    #ciphertext = [chr(ord(c) ^ next(keystream)) for c in plaintext]

    output = ""
    for c in plaintext:
        output += (chr(ord(c) ^ next(keystream)))

    return output

"""
# Example usage
key = "AreaKuning"
plaintext = "saya anak teknik"
ciphertext = encrypt(key, plaintext)
print("Ciphertext:", ciphertext)

# Untuk Dekripsi, cukup enkripsi ciphertext dengan key
decrypted_text = encrypt(key, ciphertext)
print("Decrypted text:", decrypted_text)
"""

