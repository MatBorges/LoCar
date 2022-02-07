from usuario import Usuario


class Cliente(Usuario):
    def __init__(self, nome, login, senha, cpf, cnh, numero_cartao, telefone, endereco):
        super().__init__(nome, login, senha)
        self.__cpf = cpf
        self.__cnh = cnh
        self.__numero_cartao = numero_cartao
        self.__telefone = telefone
        self.__endereco = endereco

    @property
    def cpf(self):
        return self.__cpf

    @property
    def cnh(self):
        return self.__cnh

    @property
    def numero_cartao(self):
        return self.__numero_cartao

    @property
    def telefone(self):
        return self.__telefone

    @property
    def endereco(self):
        return self.__endereco

    @cpf.setter
    def cpf(self, novo_cpf):
        self.__cpf = novo_cpf

    @cnh.setter
    def cnh(self, nova_cnh):
        self.__cnh = nova_cnh

    @numero_cartao.setter
    def numero_cartao(self, novo_numero_cartao):
        self.__numero_cartao = novo_numero_cartao

    @telefone.setter
    def telefone(self, novo_telefone):
        self.__telefone = novo_telefone

    @endereco.setter
    def endereco(self, novo_endereco):
        self.__endereco = novo_endereco
