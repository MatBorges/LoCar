class Veiculo:
    def __init__(self, tipo, marca, modelo, cor, n_chassi, ano, placa, valor_diaria):
        self.__tipo = tipo
        self.__marca = marca
        self.__modelo = modelo
        self.__cor = cor
        self.__n_chassi = n_chassi
        self.__ano = ano
        self.__placa = placa
        self.__valor_diaria = valor_diaria

    #   getters
    @property
    def tipo(self):
        return self.__tipo

    @property
    def marca(self):
        return self.__marca

    @property
    def cor(self):
        return self.__cor

    @property
    def modelo(self):
        return self.__modelo

    @property
    def ano(self):
        return self.__ano

    @property
    def n_chassi(self):
        return self.__n_chassi

    @property
    def placa(self):
        return self.__placa

    @property
    def valor_diaria(self):
        return self.__valor_diaria

    #   setters
    @tipo.setter
    def tipo(self, novo_tipo):
        self.__tipo = novo_tipo

    @marca.setter
    def marca(self, nova_marca):
        self.__marca = nova_marca

    @modelo.setter
    def modelo(self, novo_modelo):
        self.__modelo = novo_modelo

    @cor.setter
    def cor(self, nova_cor):
        self.__cor = nova_cor

    @n_chassi.setter
    def n_chassi(self, novo_n_chassi):
        self.__n_chassi = novo_n_chassi

    @ano.setter
    def ano(self, novo_ano):
        self.__ano = novo_ano

    @placa.setter
    def placa(self, nova_placa):
        self.__placa = nova_placa

    @valor_diaria.setter
    def valor_diaria(self, novo_valor_diaria):
        self.__valor_diaria = novo_valor_diaria
