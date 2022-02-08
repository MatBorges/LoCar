from funcionario import Funcionario
from cliente import Cliente
from reserva import Reserva
from veiculo import Veiculo
from datetime import date
import pymysql.cursors
from contextlib import contextmanager


@contextmanager
def conecta():
    conexao = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='',
        db='locar',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    #   Tratamento de exceção (Má Conexão)
    try:
        yield conexao
    finally:
        conexao.close()  # encerra a conexão


def insere(sql):
    with conecta() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            conexao.commit()
            print('\033[1;32mInserido com SUCESSO!!!\033[m')


def consulta(sql):
    with conecta() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            resultado = cursor.fetchone()
            return resultado


while True:
    print('LoCar')
    opc = int(input('1. Cadastrar Usuário'
                    '\n2. Cadastrar Veículo'
                    '\n3. Cadastrar Reserva'
                    '\n4. Consultas'
                    '\n5. Sair'
                    '\n:'))
    if opc == 5:  # Sair
        print('Até Mais!!!')
        break
    # Cadastrar Usuário
    elif opc == 1:
        print('\033[1;33mCadastro de Usuário\033[m')
        while True:
            opcUsuario = int(input('1. Funcionário'
                                   '\n2. Cliente'
                                   '\n3. Voltar'
                                   '\n:'))
            if opcUsuario == 3:
                break

            #   Cadastro de Funcionário
            elif opcUsuario == 1:
                print('\033[1;33mCadastro de Funcionário\033[m')

                #   Instancia da classe funcionário
                funcionario = Funcionario(input('Nome do Funcionário: '),
                                          input('Login do Funcionário: '),
                                          input('Senha do Funcionário: '),
                                          input('Matricula do Funcionário: '))

                #   Conecta e insere FUNCIONARIO no banco
                insere(f"INSERT INTO funcionarios VALUES (DEFAULT, '{funcionario.nome}', '{funcionario.login}', "
                       f"'{funcionario.senha}', '{funcionario.matricula}')")

            elif opcUsuario == 2:
                print('\033[1;33mCadastro de Cliente\033[m')
                cliente = Cliente(input('Nome do Cliente: '),
                                  input('Login do Cliente: '),
                                  input('Senha do Cliente: '),
                                  input('CPF do Cliente: '),
                                  input('CNH do Cliente: '),
                                  input('Número do Cartão do Cliente: '),
                                  input('Telefone do Cliente: '),
                                  input('Endereço do Cliente'))

                #    Conecta e insere CLIENTE no banco
                insere(f"INSERT INTO clientes VALUES (DEFAULT, '{cliente.nome}', '{cliente.login}', '{cliente.senha}', "
                       f"'{cliente.cpf}', '{cliente.cnh}', '{cliente.numero_cartao}', '{cliente.telefone}', "
                       f"'{cliente.endereco}')")
            else:
                print('\033[1;31mOpção inválida!!\033[m')

    # Cadastrar Veículo
    elif opc == 2:
        print('\033[1;33mCadastro de Veículo\033[m')
        veiculo = Veiculo(input('Qual o tipo do Veiculo?: '),
                          input('Qual a marca do Veículo?: '),
                          input('Qual o modelo do Veículo?: '),
                          input('Qual a cor do Veículo?: '),
                          input('Qual o número do chassi do veículo?: '),
                          input('Qual o ano do Veículo?: '),
                          input('Qual a placa do Veículo?: '),
                          input('Qual o valor da diária do Veículo?: '))

        #   Conexão com o banco
        insere(f"INSERT INTO veiculos VALUES (DEFAULT, '{veiculo.tipo}', '{veiculo.marca}', '{veiculo.cor}', "
               f"'{veiculo.modelo}', '{veiculo.ano}', '{veiculo.n_chassi}', '{veiculo.placa}', '{veiculo.valor_diaria}')")

    # Cadastrar Reserva
    elif opc == 3:
        print('\033[1;33mCadastro de Reserva\033[m')
        cpf_cliente = input('Qual o CPF do Cliente da reserva?: ')
        placa_veiculo = input('Qual a placa do Veículo?: ')
        cliente = consulta(f"SELECT id_cliente FROM clientes WHERE cpf = '{cpf_cliente}'")
        veiculo = consulta(f"SELECT * FROM veiculos WHERE numero_placa = '{placa_veiculo}'")
        data_inicio = input('Qual a data de Inicio da Aluguel?: ')
        periodo = int(input('Qual a duração do Aluguel?(em dias): '))

        #   Fazer a consulta do Cliente e Veículo
        reserva = Reserva(cliente['id_cliente'],
                          veiculo['id_veiculo'],
                          date.today(),
                          data_inicio,
                          periodo,
                          (veiculo['valor_diaria'] * periodo))
        insere(f"INSERT INTO reservas VALUES "
               f"(DEFAULT, '{reserva.cliente}', '{reserva.veiculo}', '{reserva.data_agendamento}', '{reserva.data_inicio}', "
               f"'{reserva.periodo}', '{reserva.valor_total}')")

    # Consultas
    elif opc == 4:
        print('\033[1;33mConsultas\033[m')
        while True:
            opcConsulta = int(input('1. Consultar Usuário'
                                    '\n2. Consultar Veículo'
                                    '\n3. Consultar Reserva'
                                    '\n4. Voltar'
                                    '\n:'))
            if opcConsulta == 4:
                break

            #   Consulta USUÁRIO
            if opcConsulta == 1:
                opcConsultaUsuario = int(input('1. Funcionário'
                                               '\n2. Cliente'
                                               '\n3. Voltar'
                                               '\n:'))

                #   CONSULTA FUNCIONÁRIO
                if opcConsultaUsuario == 1:
                    matricula = input('Qual a Matricula do Funcionário?: ')
                    resultado = consulta(f"SELECT * FROM funcionarios WHERE matricula = '{matricula}'")
                    for k, v in resultado.items():
                        print(f'{k}: {v}')

                #   CONSULTA CLIENTE
                elif opcConsultaUsuario == 2:
                    cpf = input('Qual o CPF do Cliente?: ')
                    resultado = consulta(f"SELECT * FROM clientes WHERE cpf = '{cpf}'")
                    for k, v in resultado.items():
                        print(f'{k}: {v}')

                #   SAIR DA CONSULTA DO USUÁRIO
                elif opcConsultaUsuario == 3:
                    break
                else:
                    print('\033[1;31mOpção inválida!!!\033[m')

            #   CONSULTA DE VEÍCULO
            elif opcConsulta == 2:
                placa = input('Qual o número da placa?: ')
                resultado = consulta(F"SELECT * FROM veiculos where numero_placa = '{placa}'")
                for k, v in resultado.items():
                    print(f'{k}: {v}')

            #   CONSULTA RESERVA
            elif opcConsulta == 3:
                pass
            else:
                print('\033[1;31mOpcão inválida!!!\033[m')
