from auth.crypting import aes_encrypt, aes_decrypt


class UnauthorizedMethod(Exception):
    pass


class BaseUser:
    def __init__(self, url=''):
        self.url = aes_encrypt(url)

    def is_authenticated(self):
        raise UnauthorizedMethod


class User(BaseUser):
    def is_authenticated(self):
        return True


class AnonymousUser(BaseUser):
    def __init__(self):
        super().__init__('')

    def is_authenticated(self):
        return False