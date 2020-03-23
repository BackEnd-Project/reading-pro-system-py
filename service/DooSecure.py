"""
 * @author    dooTech
 * @copyright Copyright (c) 2014-2016 DooHolding Inc. (http://www.doo.tech)
"""

import base64
from Crypto.Cipher import AES

# pip install pycryptodome

class DooSecure:
    c_key = b''
    c_iv = b'IB9N75V82Q0KJ3BK'
    Cipher = False

    def __init__(self, key):
        if type(key) is type(''):
            key = key.encode(encoding='utf-8')
        self.c_key = key
        self.Cipher = AES.new(key=self.c_key, mode=AES.MODE_CBC, IV=self.c_iv)
        return

    def pad(self, Str):
        size = 32
        if type(Str) is type(''):
            Str = Str.encode(encoding='utf-8')
        return Str + b"\0" * (size - len(Str) % size)

    # base64 加密
    def encrypt_base64(self, message):
        message = self.pad(message)
        Cipher = AES.new(key=self.c_key, mode=AES.MODE_CBC, IV=self.c_iv)
        encoded = self.c_iv + Cipher.encrypt(message)
        # 转义base64字符串
        base64Str = base64.b64encode(encoded).decode()
        base64Str = base64Str.rstrip('=').replace('+', '-').replace('/', '_')
        return base64Str

    # base64 解密
    def decrypt_base64(self, ciphertext):
        if type(ciphertext) is type(''):
            ciphertext = ciphertext.encode(encoding='utf-8')
        ciphertext = base64.b64decode(ciphertext)
        Cipher = AES.new(key=self.c_key, mode=AES.MODE_CBC, IV=self.c_iv)
        plaintext = Cipher.decrypt(ciphertext[AES.block_size:])
        plaintext = plaintext.rstrip(b"\0")
        return plaintext.decode()

    # 创建签名
    def create_sign(self):
        return ''