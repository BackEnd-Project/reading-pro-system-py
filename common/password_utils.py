"""
 * @author    dooTech
 * @copyright Copyright (c) 2014-2016 DooHolding Inc. (http://www.doo.tech)
 *
 * May you do good and not evil
 * May you find forgiveness for yourself and forgive others
 * May you share freely, never taking more than you give.  -- SQLite source code
 *
 * As we enjoy great advantages from the inventions of others, we should be glad
 * of an opportunity to serve others by an invention of ours, and this we should
 * do freely and generously.  -- Ben Franklin
 *
 *     (\
 *     (  \  /(o)\     caw!
 *     (   \/  ()/ /)
 *      (   `;.))'".)
 *       `(/////.-'
 *    =====))=))===()
 *      ///'
 *     //
 *    '
"""

import os
import base64
from hashlib import sha256
from hmac import HMAC
from Crypto.Cipher import AES
import hashlib
from Crypto import Random
from binascii import b2a_hex, a2b_hex


def encrypt_password(password, salt=None):
    """
    密码加密
    :param password:
    :param salt:
    :return:
    """
    if salt is None:
        salt = os.urandom(8)  # 64 bits.

    assert 8 == len(salt)
    assert isinstance(salt, bytes)
    assert isinstance(password, str)

    if isinstance(password, str):
        password = password.encode('UTF-8')

    assert isinstance(password, bytes)

    result = password
    for i in range(10):
        result = HMAC(result, salt, sha256).digest()
    return bytes.decode(base64.b64encode(salt + result))


def validate_password(hashed, input_password):
    """
    密码验证
    :param hashed: 存储在数据库的哈希值
    :param input_password: 用户输入的密码明文
    :return:
    """
    try:
        hashed_bytes = base64.b64decode(bytes(hashed, encoding="utf8"))
        return hashed == encrypt_password(
            input_password, salt=hashed_bytes[:8])
    except Exception:
        return False


def hash_md5(raw_str):
    """
    hash('md5') 加密
    :param raw_str:
    :return:
    """
    if raw_str is None or raw_str == "":
        return raw_str
    hl = hashlib.md5()
    hl.update(raw_str.encode(encoding='utf-8'))
    return hl.hexdigest()


def shal(raw_str):
    """
    hash_shal 加密
    :param raw_str:
    :return:
    """
    result = hashlib.sha1(raw_str.encode('utf-8')).hexdigest()
    return result


# 对应Util::commonEncrypt与Util::commonDecrypt
class CommonAESCipher:
    BS = 16

    def __init__(self, key):
        self.key = key + (32 - len(key)) * chr(0)
        self.key = self.key.encode('utf-8')

    def pad(self, s):
        """
        #这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.
        #目前AES-128足够用
        :param s:
        :return:
        """
        return s + (self.BS - len(s) % self.BS) * \
            chr(self.BS - len(s) % self.BS)

    def unpad(self, s):
        """
        :param s:
        :return:
        """
        return s[:-ord(s[len(s) - 1:])]

    def common_encrypt(self, raw):
        """
        加密
        :param raw:
        :return:
        """
        if raw is None or raw == "":
            return raw
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.urlsafe_b64encode(
            iv + cipher.encrypt(raw.encode())).decode()

    def common_decrypt(self, enc):
        """
        解密
        :param enc:
        :return:
        """
        if enc is None or enc == "":
            return enc
        try:
            enc = base64.urlsafe_b64decode(enc)
            iv = enc[:16]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return self.unpad(cipher.decrypt(enc[16:])).decode()
        except Exception as Err:
            print(Err)
            return enc


class AESCipher:
    def __init__(self, key):
        self.key = key
        self.key = key + (32 - len(key)) * chr(0)
        self.key = self.key.encode('utf-8')
        self.iv = "IB9N75V82Q0KJ3BK".encode('utf-8')
        self.BLOCK_SIZE = 16  # Bytes
        self.pad = lambda s: s + (self.BLOCK_SIZE - len(s.encode('utf-8')) %
                                  self.BLOCK_SIZE) * chr(self.BLOCK_SIZE - len(s.encode('utf-8')) %
                                                         self.BLOCK_SIZE)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def encrypt(self, raw):
        """
        加密
        :param raw:
        :return:
        """
        raw = self.pad(raw)
        raw = raw.encode('utf-8')
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw))

    def decrypt(self, enc):
        """
        解密
        :param enc:
        :return:
        """
        try:
            enc = enc + "=="
            enc = base64.urlsafe_b64decode(enc)
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            return self.unpad(cipher.decrypt(enc)).decode('utf-8')
        except Exception as Err:
            print(Err)
            return None
