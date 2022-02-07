class Usuario:
    def __init__(self, nome, login, senha):
        self.__nome = nome
        self.__login = login
        self.__senha = senha

    def valida_usuario(self, login, senha):
        if login == self.__login and senha == self.__senha:
            return True
        else:
            return False

    #   Getters
    @property
    def nome(self):
        return self.__nome

    @property
    def login(self):
        return self.__login

    @property
    def senha(self):
        return self.__senha

    #   Setters
    @nome.setter
    def nome(self, novo_nome):
        self.__nome = novo_nome

    @login.setter
    def login(self, novo_login):
        self.__login = novo_login

    @senha.setter
    def senha(self, nova_senha):
        self.__senha = nova_senha
