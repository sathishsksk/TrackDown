import base64
from Crypto.Cipher import DES
import binascii

def decrypt_url(url):
    key = b"38346591"
    iv = b"01234567"
    cipher = DES.new(key, DES.MODE_CBC, iv)
    encrypted_data = base64.b64decode(url)
    decrypted_data = cipher.decrypt(encrypted_data)
    padding_size = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding_size]
    return decrypted_data.decode('utf-8')

url = "ID2ieOjCrwfgWvL5sXl4B1ImC5QfbsDyFNsfQCO91T0dC9btMN5x/FlZmbA/MpEGc30F7gTMuUdelA8wZuh/oRw7tS9a8Gtq"
decrypted_url = decrypt_url(url)
print(decrypted_url)
