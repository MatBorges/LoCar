class Reserva:
    def __init__(self, cliente, veiculo, data_agendamento, data_inicio, periodo):
        self.__cliente = cliente
        self.__veiculo = veiculo
        self.__data_agendamento = f'{data_agendamento.day}/{data_agendamento.month}/{data_agendamento.year}'
        self.__data_inicio = data_inicio
        self.__periodo = periodo
        self.__valor_total = None

    #   getters
    @property
    def cliente(self):
        return self.cliente

    @property
    def veiculo(self):
        return self.veiculo

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
