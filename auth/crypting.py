import base64
import json

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# key = get_random_bytes(16)
key = b'u\xfa\x1f\x9a\x14\x19&\xe7b#\x86\xdd\x94\x0f[N'
cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce


class WrongUserError(Exception):
    message = 'Error during decryption'


def aes_encrypt(data: str) -> str:
    """
    Encrypt data with AES crypto algorithm.

    :param data: string to encrypt with AES
    :return: encrypted string
    """
    length = 16 - (len(data) % 16)
    data += chr(length) * length

    cipher_new = AES.new(key, AES.MODE_EAX, nonce=nonce)
    ciphertext = cipher_new.encrypt(data.encode('utf-8'))
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext.decode('utf-8')


def aes_decrypt(ciphertext: str) -> str:
    cipher_new = AES.new(key, AES.MODE_EAX, nonce=nonce)
    ciphertext = ciphertext.encode()
    ciphertext = base64.b64decode(ciphertext)
    data = cipher_new.decrypt(ciphertext)
    data = data.decode()
    # crop extra tildes on the right
    return data[:-ord(data[-1])]


