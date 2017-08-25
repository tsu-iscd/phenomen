import threading
from datetime import datetime
from hashlib import sha256


class User:
    def __init__(self, name, password) -> None:
        self.name = name
        self.password = sha256(password.encode()).hexdigest()
        self.reg_date = None


class UserManager:
    def __init__(self) -> None:
        self.users = {}
        self.mutex = threading.Lock()

    def add_users(self, *users) -> None:
        with self.mutex:
            for user in users:
                self.users[user.name] = user
                user.reg_date = "{:%B %d, %Y}".format(datetime.now())

    def get_user(self, name) -> User:
        with self.mutex:
            return self.users.get(name, None)
