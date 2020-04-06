import pyaes
import binascii
import hmac
import hashlib
import base64


def encryptAES(key, plaintext):
    counter = pyaes.Counter(initial_value = 5)
    aes = pyaes.AESModeOfOperationCTR(bytearray.fromhex(key), counter = counter)
    ciphertext = aes.encrypt(plaintext)
    return binascii.hexlify(ciphertext)


def decryptAES(key, ciphertext):
    counter = pyaes.Counter(initial_value = 5)
    aes = pyaes.AESModeOfOperationCTR(bytearray.fromhex(key), counter = counter)
    strCipherText = "".join([chr(int(ciphertext[x:x+2], 16)) for x in range(0, len(ciphertext), 2)])
    return aes.decrypt(strCipherText)


def getHmac(key, message):
    #signature = hmac.new(key.encode('utf-8'), message.encode(), hashlib.sha256).hexdigest()
    signature = (base64.b64encode(hmac.new(key.encode('utf-8'), message.encode(), digestmod=hashlib.sha256).digest())).decode()

    return signature




