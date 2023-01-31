from binascii import a2b_hex, b2a_hex

from Crypto.Cipher import AES

from core.settings import settings


class CryptoUtils:
    @staticmethod
    def encrypt(text):
        text = text.encode("utf-8")
        cryptor = AES.new(settings.secret_key, AES.MODE_CBC, b"0000000000000000")
        # 这里密钥key 长度必须为16（AES-128）,
        # 24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用
        length = 16
        count = len(text)
        if count < length:
            add = length - count
            # \0 backspace
            # text = text + ('\0' * add)
            text = text + ("\0" * add).encode("utf-8")
        elif count > length:
            add = length - (count % length)
            # text = text + ('\0' * add)
            text = text + ("\0" * add).encode("utf-8")
        ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(ciphertext)

    @staticmethod
    def decrypt(text):
        cryptor = AES.new(settings.secret_key, AES.MODE_CBC, b"0000000000000000")
        plain_text = cryptor.decrypt(a2b_hex(text))
        return bytes.decode(plain_text).rstrip("\0")
