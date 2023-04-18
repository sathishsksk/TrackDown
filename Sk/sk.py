import base64
from Crypto.Cipher import DES

def decrypt_url(url):
    key = b"38346591"
    iv = b"\0\0\0\0\0\0\0\0"
    cipher = DES.new(key, DES.MODE_CBC, iv)
    enc_url = base64.b64decode(url.strip())
    dec_url = cipher.decrypt(enc_url)
    dec_url = dec_url[:-dec_url[-1]]
    dec_url = dec_url.decode('utf-8')
    dec_url = dec_url.replace("_96.mp4", "_320.mp4")
    return dec_url

encrypted_url = "ID2ieOjCrwfgWvL5sXl4B1ImC5QfbsDyFNsfQCO91T0dC9btMN5x/FlZmbA/MpEGc30F7gTMuUdelA8wZuh/oRw7tS9a8Gtq"
decrypted_url = decrypt_url(encrypted_url)
print(decrypted_url)
