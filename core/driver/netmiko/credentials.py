from hashlib import sha512
from typing import Optional


class Credentials:
    """
    Dead simple object, built simply to hold credential information.
    We need this primarily to prevent printing of credentials in log messages.
    """

    def __init__(self, username: str, password: str, enable: Optional[str] = None) -> None:
        """
        Instantiate our Credentials object
        :param username:
        :param password:
        :param enable:  If not provided, will set to the password.
        """
        self.username = username
        self.password = password
        if enable is None:
            self.enable = ""
        else:
            self.enable = enable

    def __repr__(self):
        return f'{{"username": "{self.username}", "password": "<redacted>", "enable": "<redacted>"}}'

    def __str__(self):
        return self.username + ":<redacted>:<redacted>"

    def salted_hash(self, salt: Optional[str] = None) -> str:
        """
        SHA512 (salted) hash the username/password and return the hexdigest
        :param salt: If not provided, we'll fetch it from Redis
        :return:
        """

        pork = self.username + ":" + self.password + salt
        salt_shaker = sha512(pork.encode())
        salted_pork = salt_shaker.hexdigest()  # Particularly nice
        return salted_pork
