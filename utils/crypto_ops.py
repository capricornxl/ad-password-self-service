from cryptography.fernet import Fernet


class Crypto(object):
    """docstring for ClassName"""
    def __init__(self, key):
        self.factory = Fernet(key)

    # 加密
    def encrypt(self, string):
        token = str(self.factory.encrypt(string.encode('utf-8')), 'utf-8')
        return token

    # 解密
    def decrypt(self, token):
        string = self.factory.decrypt(bytes(token.encode('utf-8'))).decode('utf-8')
        return string
