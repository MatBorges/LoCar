from usuario import Usuario


class Cliente(Usuario):
    def __init__(self, nome, login, senha, cpf, cnh):
        super().__init__(nome, login, senha)
        self.__cpf = cpf
        self.__cnh = cnh

    @property
    def cpf(self):
        return self.__cpf

    @property
    def cnh(self):
        return self.__cnh

    @cpf.setter
    def cpf(self, novo_cpf):
        self.__cpf = novo_cpf

    @cnh.setter
    def cnh(self, nova_cnh):
        self.__cnh = nova_cnh
