class Reserva:
    def __init__(self, cliente, veiculo, data_agendamento, data_inicio, periodo, valor_total):
        self.__cliente = cliente
        self.__veiculo = veiculo
        self.__data_agendamento = data_agendamento
        self.__data_inicio = data_inicio
        self.__periodo = periodo
        self.__valor_total = valor_total

    #   getters
    @property
    def cliente(self):
        return self.__cliente

    @property
    def veiculo(self):
        return self.__veiculo

    @property
    def data_agendamento(self):
        return self.__data_agendamento

    @property
    def data_inicio(self):
        return self.__data_inicio

    @property
    def periodo(self):
        return self.__periodo

    @property
    def valor_total(self):
        return self.__valor_total

    #   setters
    @veiculo.setter
    def veiculo(self, novo_veiculo):
        self.__veiculo = novo_veiculo

    @data_inicio.setter
    def data_inicio(self, nova_data_inicio):
        self.__data_inicio = nova_data_inicio

    @periodo.setter
    def periodo(self, novo_periodo):
        self.__periodo = novo_periodo
