from funcionario import Funcionario
from cliente import Cliente
#from reserva import Reserva
from veiculo import Veiculo
#from datetime import date
import pymysql.cursors
from contextlib import contextmanager
from PyQt5 import uic, QtWidgets


def teste():
    print('TESTANDO!!!!!!!!!!!!!')


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


def buscaCombobox(sql, chave):
    busca = consultaVarios(sql)
    cb = []
    for v in busca:
        cb.append(v[chave])
    return cb


def consulta(sql):
    with conecta() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            return result


#   CONSULTA RESERVA
def consultaVarios(sql):
    with conecta() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result


def logout():
    telaLogin.tbLogin.clear()
    telaLogin.tbSenha.clear()
    telaInicial.close()
    telaLogin.show()


def login():
    telaLogin.alertaLogin.setText('')
    usuario = telaLogin.tbLogin.text()
    senha = telaLogin.tbSenha.text()
    senha_banco = consulta(f"SELECT senha FROM funcionarios WHERE login = '{usuario}'")
    if senha_banco == None:
        telaLogin.alertaLogin.setText('USUÁRIO INVÁLIDO')
    else:
        if senha_banco['senha'] == senha:
            telaLogin.close()
            menuInicial(usuario)
        else:
            telaLogin.alertaLogin.setText('SENHA INVÁLIDA')


def voltarCad():
    telaCadastros.close()
    telaInicial.show()


def voltarCon():
    telaConsultas.close()
    telaInicial.show()


def menuInicial(usuario):
    nomeUsuario = consulta(f"SELECT nome FROM funcionarios WHERE login = '{usuario}'")
    telaInicial.show()
    telaInicial.boasVindas.setText(f'Bem-vindo {nomeUsuario["nome"]}')
    telaInicial.btSair.clicked.connect(logout)
    telaInicial.btCad.clicked.connect(menuCadastros)
    telaInicial.btCon.clicked.connect(menuConsultas)


def menuCadastros():
    telaCadastros.show()
    telaCadastros.btCadUsuario.clicked.connect(cadUsuario)
    telaCadastros.btCadVeiculo.clicked.connect(chamaCadVeiculo)
    #telaCadastros.btCadReserva.clicked.connect()
    telaCadastros.btVoltar.clicked.connect(voltarCad)


def menuConsultas():
    telaConsultas.show()
    telaConsultas.btConUsuario.clicked.connect(conUsuario)
    #telaConsultas.btConVeiculo.clicked.connect()
    #telaConsultas.btConReserva.clicked.connect()
    telaConsultas.btVoltar.clicked.connect(voltarCon)


def cadUsuario():
    telaCadUsuario.show()
    telaCadUsuario.btCadFuncionario.clicked.connect(telaCadUsuario.frameCadFuncionario.show)
    telaCadUsuario.btCadastrarFuncionario.clicked.connect(cadFuncionario)
    telaCadUsuario.btCadastrarCliente.clicked.connect(cadCliente)
    telaCadUsuario.btCadCliente.clicked.connect(telaCadUsuario.frameCadFuncionario.close)
    telaCadUsuario.btVoltar.clicked.connect(telaCadUsuario.close)



def cadFuncionario():
    funcionario = Funcionario(telaCadUsuario.tbNomeFuncionario.text(),
                              telaCadUsuario.tbLoginFuncionario.text(),
                              telaCadUsuario.tbSenhaFuncionario.text(),
                              telaCadUsuario.tbMatriculaFuncionario.text())

    #   Conecta e insere FUNCIONARIO no banco
    insere(f"INSERT INTO funcionarios VALUES (DEFAULT, '{funcionario.nome}', '{funcionario.login}', "
           f"'{funcionario.senha}', '{funcionario.matricula}')")

    telaCadUsuario.tbNomeFuncionario.clear()
    telaCadUsuario.tbLoginFuncionario.clear()
    telaCadUsuario.tbSenhaFuncionario.clear()
    telaCadUsuario.tbMatriculaFuncionario.clear()


def cadCliente():
    cliente = Cliente(telaCadUsuario.tbNomeCliente.text(),
                      telaCadUsuario.tbLoginCliente.text(),
                      telaCadUsuario.tbSenhaCliente.text(),
                      telaCadUsuario.tbCPFCliente.text(),
                      telaCadUsuario.tbCNHCliente.text(),
                      telaCadUsuario.tbNCartaoCliente.text(),
                      telaCadUsuario.tbTelefoneCliente.text(),
                      telaCadUsuario.tbEnderecoCliente.text())

    #    Conecta e insere CLIENTE no banco
    insere(f"INSERT INTO clientes VALUES (DEFAULT, '{cliente.nome}', '{cliente.login}', '{cliente.senha}', "
           f"'{cliente.cpf}', '{cliente.cnh}', '{cliente.numero_cartao}', '{cliente.telefone}', "
           f"'{cliente.endereco}')")

    telaCadUsuario.tbNomeCliente.clear()
    telaCadUsuario.tbLoginCliente.clear()
    telaCadUsuario.tbSenhaCliente.clear()
    telaCadUsuario.tbCPFCliente.clear()
    telaCadUsuario.tbCNHCliente.clear()
    telaCadUsuario.tbNCartaoCliente.clear()
    telaCadUsuario.tbTelefoneCliente.clear()
    telaCadUsuario.tbEnderecoCliente.clear()


def chamaCadVeiculo():
    #   ABRE A JANELA DO CADASTRO DE VEÍCULO
    telaCadVeiculo.show()
    telaCadVeiculo.btVoltar.clicked.connect(telaCadVeiculo.close)
    telaCadVeiculo.btCadastrarCliente.clicked.connect(cadVeiculo)
    telaCadVeiculo.cbTipoVeiculo.addItems(buscaCombobox('SELECT * FROM tipos', 'tipo'))
    telaCadVeiculo.cbMarcaVeiculo.addItems(buscaCombobox('SELECT * FROM marcas', 'marca'))
    telaCadVeiculo.cbCorVeiculo.addItems(buscaCombobox('SELECT * FROM cores', 'cor'))


def cadVeiculo():
    #   LÊ OS DADOS
    veiculo = Veiculo(telaCadVeiculo.cbTipoVeiculo.currentText(),
                      telaCadVeiculo.cbMarcaVeiculo.currentText(),
                      telaCadVeiculo.cbCorVeiculo.currentText(),
                      telaCadVeiculo.tbModeloVeiculo.text(),
                      telaCadVeiculo.tbAnoVeiculo.text(),
                      telaCadVeiculo.tbNChassiVeiculo.text(),
                      telaCadVeiculo.tbNPlacaVeiculo.text(),
                      telaCadVeiculo.tbVDiariaVeiculo.text())
    tipo = consulta(f"SELECT id_tipo FROM tipos WHERE tipo = '{veiculo.tipo}'")
    marca = consulta(f"SELECT id_marca FROM marcas WHERE marca = '{veiculo.marca}'")
    cor = consulta(f"SELECT id_cor FROM cores WHERE cor = '{veiculo.cor}'")

    #   INSERE OS DADOS LIDOS NO BANCO
    insere(
        f"INSERT INTO veiculos VALUES (DEFAULT, '{tipo['id_tipo']}', '{marca['id_marca']}', '{cor['id_cor']}', '{veiculo.modelo}', "
        f" '{veiculo.n_chassi}', '{veiculo.ano}', '{veiculo.placa}', '{veiculo.valor_diaria}')")

    #   LIMPA AS TEXTBOX
    telaCadVeiculo.tbModeloVeiculo.clear()
    telaCadVeiculo.tbAnoVeiculo.clear()
    telaCadVeiculo.tbNChassiVeiculo.clear()
    telaCadVeiculo.tbNPlacaVeiculo.clear()
    telaCadVeiculo.tbVDiariaVeiculo.clear()


def conUsuario():
    telaConUsuario.show()
    telaConUsuario.btVoltar.clicked.connect(telaConUsuario.close)


app = QtWidgets.QApplication([])
telaLogin = uic.loadUi("telaLogin.ui")
telaInicial = uic.loadUi("telaInicial.ui")
telaCadastros = uic.loadUi("telaCadastros.ui")
telaConsultas = uic.loadUi("telaConsultas.ui")
telaCadUsuario = uic.loadUi("telaCadastroUsuario.ui")
telaConUsuario = uic.loadUi("telaConsultaUsuario.ui")
telaCadVeiculo = uic.loadUi("telaCadastroVeiculo.ui")


telaLogin.botaoLogin.clicked.connect(login)


telaLogin.show()
app.exec()

'''while True:
    print('LoCar')
    opc = int(input('\033[1;33mCADASTROS\033[m'
                    '\n1. Cadastrar Usuário'
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
        while True:
            opcUsuario = int(input('\033[1;33mCADASTRO DE USUÁRIO\033[m'
                                   '\n1. Funcionário'
                                   '\n2. Cliente'
                                   '\n3. Voltar'
                                   '\n:'))
            if opcUsuario == 3:
                break

            #   Cadastro de Funcionário
            elif opcUsuario == 1:
                print('\033[1;33mCADASTRO DE FUNCIONÁRIO\033[m')
                funcionario = Funcionario(input('Nome do Funcionário: '),
                                          input('Login do Funcionário: '),
                                          input('Senha do Funcionário: '),
                                          input('Matricula do Funcionário: '))

                #   Conecta e insere FUNCIONARIO no banco
                insere(f"INSERT INTO funcionarios VALUES (DEFAULT, '{funcionario.nome}', '{funcionario.login}', "
                       f"'{funcionario.senha}', '{funcionario.matricula}')")

            elif opcUsuario == 2:
                print('\033[1;33mCADASTRO DE CLIENTE\033[m')
                cliente = Cliente(input('Nome do Cliente: '),
                                  input('Login do Cliente: '),
                                  input('Senha do Cliente: '),
                                  input('CPF do Cliente: '),
                                  input('CNH do Cliente: '),
                                  input('Número do Cartão do Cliente: '),
                                  input('Telefone do Cliente: '),
                                  input('Endereço do Cliente: '))

                #    Conecta e insere CLIENTE no banco
                insere(f"INSERT INTO clientes VALUES (DEFAULT, '{cliente.nome}', '{cliente.login}', '{cliente.senha}', "
                       f"'{cliente.cpf}', '{cliente.cnh}', '{cliente.numero_cartao}', '{cliente.telefone}', "
                       f"'{cliente.endereco}')")
            else:
                print('\033[1;31mOPÇÃO INVÁLIDA\033[m')

    # Cadastrar Veículo
    elif opc == 2:
        print('\033[1;33mCADASTRO DE VEÍCULO\033[m')
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
        print('\033[1;33mCADASTRO DE RESERVA\033[m')
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
        while True:
            opcConsulta = int(input('\033[1;33mCONSULTAS\033[m'
                                    '\n1. Consultar Usuário'
                                    '\n2. Consultar Veículo'
                                    '\n3. Consultar Reserva'
                                    '\n4. Voltar'
                                    '\n:'))
            if opcConsulta == 4:
                break

            #   CONSULTA USUÁRIO
            if opcConsulta == 1:
                opcConsultaUsuario = int(input('\033[1;33mCONSULTA DE USUÁRIO\033[m'
                                               '\n1. Funcionário'
                                               '\n2. Cliente'
                                               '\n3. Voltar'
                                               '\n:'))

                #   CONSULTA FUNCIONÁRIO
                if opcConsultaUsuario == 1:
                    print('\033[1;33mCONSULTA DE FUNCIONÁRIO\033[m')
                    matricula = input('Qual a Matricula do Funcionário?: ')
                    resultado = consulta(f"SELECT * FROM funcionarios WHERE matricula = '{matricula}'")
                    print('*=' * 20)
                    for k, v in resultado.items():
                        print(f'{k}: {v}')
                    print('*=' * 20)

                #   CONSULTA CLIENTE
                elif opcConsultaUsuario == 2:
                    print('\033[1;33mCONSULTA DE CLIENTE\033[m')
                    cpf = input('Qual o CPF do Cliente?: ')
                    resultado = consulta(f"SELECT * FROM clientes WHERE cpf = '{cpf}'")
                    print('*=' * 20)
                    for k, v in resultado.items():
                        print(f'{k}: {v}')
                    print('*=' * 20)

                #   SAIR DA CONSULTA DO USUÁRIO
                elif opcConsultaUsuario == 3:
                    break
                else:
                    print('\033[1;31mOPÇÃO INVÁLIDA!!!\033[m')

            #   CONSULTA DE VEÍCULO
            elif opcConsulta == 2:
                print('\033[1;33mCONSULTA DE VEÍCULO\033[m')
                placa = input('Qual o número da placa?: ')
                resultado = consulta(f"SELECT * FROM veiculos where numero_placa = '{placa}'")
                print('*=' * 20)
                for k, v in resultado.items():
                    print(f'{k}: {v}')
                print('*=' * 20)

            #   CONSULTA RESERVA
            elif opcConsulta == 3:
                print('\033[1;33mCONSULTA DE RESERVA\033[m')
                cpf = input('Digite o CPF do cliente para consultar as reservas cadastradas: ')
                #   ids_reservas armazena uma lista de dicionários de todos os ids correspondentes ao cpf digitado
                ids_reservas = consulta_reserva(f"SELECT r.id_reserva FROM reservas AS r "
                                                f"JOIN clientes AS c "
                                                f"ON r.fk_id_cliente = c.id_cliente "
                                                f"WHERE c.cpf = '{cpf}'")
                for valor in ids_reservas:
                    reserva = consulta(f"SELECT * FROM reservas WHERE id_reserva = '{valor['id_reserva']}' ")
                    print('=*' * 20)
                    for k, v in reserva.items():
                        print(f'{k}: {v}')
            else:
                print('\033[1;31mOPÇÃO INVÁLIDA\033[m')'''
