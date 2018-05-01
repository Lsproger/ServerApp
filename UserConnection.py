
class Connection:

    def __init__(self, sock, addr, name):
        self.__connection = sock
        self.__address = addr
        self.__username = name

    @property
    def sock(self):
        return self.__connection

    @property
    def addr(self):
        return self.__address

    @property
    def username(self):
        return self.__username
