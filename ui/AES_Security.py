# AES_Security.py
# This is an AES Encryption file to secure data passing by means of socket

import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode


class AESCipher(object):

    print("CONNECTED TO ~~~ AES_Security.py")

    # constructor will run the statements as soon as the object of the class is instantiated.
    # initializing block size and key
    def __init__(self, key):
        self.block_size = AES.block_size  # block size is 128 bits
        self.key = hashlib.sha256(key.encode()).digest()  # generating a 256 bit hash from the key

    def encrypt(self, plain_text):
        # print("IN ENCRYPT FUNCTION")
        plain_text = self.__pad(plain_text)  # pad "plain_text" in order to encrypt it
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)  # creating an AES cipher with key, mode CBC, and iv
        encrypted_text = cipher.encrypt(
            plain_text.encode())  # encrypting using the encrypt function while passing it "plain_text"
        return b64encode(iv + encrypted_text).decode("utf-8")

    def decrypt(self, encrypted_text):
        # print("IN DECRYPT FUNCTION")
        encrypted_text = b64decode(encrypted_text)
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
        return self.__unpad(plain_text)

    #  this function will receive "plain_text", which will be encrypted.
    #  it will then add a number bytes for the text to be a multiple of 128 bits
    def __pad(self, plain_text):
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)  # generate the padding character
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str  # adding "padding_str" to the end of "plain_text" to make it a multiple of 128 bits
        return padded_plain_text

    # this function will receive the decrypted text "plain_text" and will remove the extra added characters that was added from method "__pad"
    @staticmethod
    def __unpad(plain_text):
        last_character = plain_text[len(plain_text) - 1:]  # identifying the last character in "plain_text"
        bytes_to_remove = ord(last_character)  # storing the last character
        return plain_text[:-bytes_to_remove]  # trimming the end of "plain_text"
