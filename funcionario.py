from usuario import Usuario


class Funcionario(Usuario):
    def __init__(self, nome, login, senha, matricula):
        super().__init__(nome, login, senha)
        self.__matricula = matricula

    @property
    def matricula(self):
        return self.__matricula

    @matricula.setter
    def matricula(self, nova_matricula):
        self.__matricula = nova_matricula
