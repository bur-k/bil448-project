import pyaes
import binascii

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
