from funcionario import Funcionario
from cliente import Cliente
from reserva import Reserva
from veiculo import Veiculo
from datetime import date
import pymysql.cursors
from contextlib import contextmanager
from PyQt5 import uic, QtWidgets
from PyQt5 import QtCore


def teste(teste):
    print(f'\033[1;32mTESTANDO: {teste}\033[m')


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
    telaCadastros.btCadReserva.clicked.connect(chamaCadReserva)
    telaCadastros.btVoltar.clicked.connect(voltarCad)


def menuConsultas():
    telaConsultas.show()
    telaConsultas.btConUsuario.clicked.connect(conUsuario)
    telaConsultas.btConVeiculo.clicked.connect(tConVeiculo)
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
        f"INSERT INTO veiculos VALUES (DEFAULT, '{tipo['id_tipo']}', '{marca['id_marca']}', '{cor['id_cor']}', "
        f"'{veiculo.modelo}', '{veiculo.n_chassi}', '{veiculo.ano}', '{veiculo.placa}', '{veiculo.valor_diaria}')")

    #   LIMPA AS TEXTBOX
    telaCadVeiculo.tbModeloVeiculo.clear()
    telaCadVeiculo.tbAnoVeiculo.clear()
    telaCadVeiculo.tbNChassiVeiculo.clear()
    telaCadVeiculo.tbNPlacaVeiculo.clear()
    telaCadVeiculo.tbVDiariaVeiculo.clear()

#   TELA DE CADASTRO DE RESERVA
def chamaCadReserva():
    telaCadReserva.show()
    telaCadReserva.labelCliente.setText('')
    telaCadReserva.labelVeiculo.setText('')
    dataHj = str(date.today())
    ano = int(dataHj[0:4])
    mes = int(dataHj[5:7])
    dia = int(dataHj[8:])
    telaCadReserva.dateReserva.setDate(QtCore.QDate(ano, mes, dia))
    telaCadReserva.btVoltar.clicked.connect(telaCadReserva.close)
    telaCadReserva.btConCliente.clicked.connect(conCliRes)
    telaCadReserva.btConVeiculo.clicked.connect(conVeiRes)
    telaCadReserva.btCadastrarCliente.clicked.connect(cadReserva)


#   CONSULTA SE CPF DO CLIENTE ESTÁ CADASTRADO
def conCliRes():
    nomeCli = consulta(f"SELECT id_cliente, nome, cpf FROM clientes WHERE cpf = '{telaCadReserva.tbCliente.text()}'")
    if nomeCli == None:
        telaCadReserva.labelCliente.setText('CLIENTE NÃO EXISTE!')
    else:
        telaCadReserva.labelCliente.setText(f'Cliente: {nomeCli["nome"]} CPF: {nomeCli["cpf"]}')
    #telaCadReserva.tbCliente.clear()
    return nomeCli['id_cliente']

#   CONSULTA DE PLACA DO VEÍCULO ESTÁ CADASTRADA
def conVeiRes():
    modeloVei = consulta(f"SELECT id_veiculo, fk_id_marca, modelo, ano, fk_id_cor FROM veiculos WHERE numero_placa = "
                         f"'{telaCadReserva.tbVeiculo.text()}'")
    if modeloVei == None:
        telaCadReserva.labelVeiculo.setText('VEÌCULO NÃO EXISTE!')
    else:
        cor = consulta(f"SELECT c.cor FROM cores AS c "
                       f"JOIN veiculos AS v "
                       f"ON c.id_cor = v.fk_id_cor "
                       f"WHERE c.id_cor = {modeloVei['fk_id_cor']}")
        marca = consulta(f"SELECT m.marca FROM marcas AS m "
                         f"JOIN veiculos AS v "
                         f"ON m.id_marca = v.fk_id_marca "
                         f"WHERE m.id_marca = {modeloVei['fk_id_marca']}")
        telaCadReserva.labelVeiculo.setText(f'Veículo: {marca["marca"]} {modeloVei["modelo"]} '
                                            f'{modeloVei["ano"]}, {cor["cor"]}')
    #telaCadReserva.tbVeiculo.clear()
    return modeloVei['id_veiculo']


def cadReserva():
    idVei = conVeiRes()
    idCli = conCliRes()
    periodo = telaCadReserva.tbPeriodo.text()
    valor_diaria = consulta(f"SELECT valor_diaria FROM veiculos WHERE id_veiculo = '{idVei}'")
    valor_diaria = float(valor_diaria['valor_diaria'])
    data = str(telaCadReserva.dateReserva.date())

    #   Formata a saída de .date()
    data = data[19:]
    dataForm = ''
    for i in data:
        if i in '0123456789':
            dataForm = (dataForm + i)
        elif i == ',':
            dataForm = (dataForm + '-')

    #   conCliRes() retorna id_cliente e conVeiRes retorna id_veiculo
    reserva = Reserva(idCli,
                      idVei,
                      date.today(),
                      dataForm,
                      telaCadReserva.tbPeriodo.text(),
                      (valor_diaria * int(periodo)))
    insere(f"INSERT INTO reservas VALUES "
           f"(DEFAULT, '{reserva.cliente}', '{reserva.veiculo}', '{reserva.data_agendamento}', '{reserva.data_inicio}', "
           f"'{reserva.periodo}', '{reserva.valor_total}')")


def conUsuario():
    telaConUsuario.show()
    telaConUsuario.btConFuncionario.clicked.connect(telaConUsuario.frameConFuncionario.show)
    telaConUsuario.btConCliente.clicked.connect(telaConUsuario.frameConFuncionario.close)
    telaConUsuario.btVoltar.clicked.connect(telaConUsuario.close)
    telaConUsuario.btConsultarFuncionario.clicked.connect(conFuncionario)
    telaConUsuario.btConsultarCliente.clicked.connect(conCliente)


def conFuncionario():
    telaConUsuario.labelNomeFunc.clear()
    telaConUsuario.labelLoginFunc.clear()
    telaConUsuario.labelMatriculaFunc.clear()
    funcionario = consulta(f"SELECT * FROM funcionarios WHERE matricula = "
                           f"'{telaConUsuario.tbMatricula.text()}'")
    if funcionario == None:
        telaConUsuario.labelNomeFunc.setText('MATRICULA NÃO CADASTRADA')

    else:
        telaConUsuario.labelNomeFunc.setText(funcionario['nome'])
        telaConUsuario.labelLoginFunc.setText(funcionario['login'])
        telaConUsuario.labelMatriculaFunc.setText(funcionario['matricula'])
        telaConUsuario.tbMatricula.clear()


def conCliente():
    telaConUsuario.labelNomeCli.clear()
    telaConUsuario.labelLoginCli.clear()
    telaConUsuario.labelCPFCli.clear()
    telaConUsuario.labelCNHCli.clear()
    telaConUsuario.labelTelefoneCli.clear()
    telaConUsuario.labelEnderecoCli.clear()
    cliente = consulta(f"SELECT * FROM clientes WHERE cpf = "
                       f"'{telaConUsuario.tbCPF.text()}'")
    if cliente == None:
        telaConUsuario.labelNomeCli.setText('CPF NÃO CADASTRADO')
    else:
        telaConUsuario.labelNomeCli.setText(cliente['nome'])
        telaConUsuario.labelLoginCli.setText(cliente['login'])
        telaConUsuario.labelCPFCli.setText(cliente['cpf'])
        telaConUsuario.labelCNHCli.setText(cliente['cnh'])
        telaConUsuario.labelTelefoneCli.setText(cliente['telefone'])
        telaConUsuario.labelEnderecoCli.setText(cliente['endereco'])
        telaConUsuario.tbCPF.clear()


def tConVeiculo():
    telaConVeiculo.show()
    telaConVeiculo.btVoltar.clicked.connect(telaConVeiculo.close)
    telaConVeiculo.btConsultarVeiculo.clicked.connect(conVeiculo)

def conVeiculo():
    telaConVeiculo.labelMarcaVei.clear()
    telaConVeiculo.labelModeloVei.clear()
    telaConVeiculo.labelAnoVei.clear()
    telaConVeiculo.labelCorVei.clear()
    telaConVeiculo.labelTipoVei.clear()
    telaConVeiculo.labelPlacaVei.clear()
    telaConVeiculo.labelChassiVei.clear()
    telaConVeiculo.labelValorDiariaVei.clear()

    veiculo = consulta(f"SELECT * FROM veiculos WHERE numero_placa = '{telaConVeiculo.tbNumeroPlaca.text()}'")

    if veiculo == None:
        telaConVeiculo.labelMarcaVei.setText('PLACA NÃO CADASTRADA')
    else:
        marca = consulta(f"SELECT marca FROM marcas AS m "
                         f"JOIN veiculos AS v "
                         f"ON v.fk_id_marca = m.id_marca "
                         f"WHERE v.numero_placa = {veiculo['numero_placa']}")
        cor = consulta(f"SELECT cor FROM cores AS c "
                         f"JOIN veiculos AS v "
                         f"ON v.fk_id_cor = c.id_cor "
                         f"WHERE v.numero_placa = {veiculo['numero_placa']}")
        tipo = consulta(f"SELECT tipo FROM tipos AS t "
                         f"JOIN veiculos AS v "
                         f"ON v.fk_id_tipo = t.id_tipo "
                         f"WHERE v.numero_placa = {veiculo['numero_placa']}")

        telaConVeiculo.labelMarcaVei.setText(marca['marca'])
        telaConVeiculo.labelModeloVei.setText(veiculo['modelo'])
        telaConVeiculo.labelAnoVei.setText(veiculo['ano'])
        telaConVeiculo.labelCorVei.setText(cor['cor'])
        telaConVeiculo.labelTipoVei.setText(tipo['tipo'])
        telaConVeiculo.labelPlacaVei.setText(veiculo['numero_placa'])
        telaConVeiculo.labelChassiVei.setText(veiculo['numero_chassi'])
        telaConVeiculo.labelValorDiariaVei.setText(veiculo['valor_diaria'])


app = QtWidgets.QApplication([])
telaLogin = uic.loadUi("telaLogin.ui")
telaInicial = uic.loadUi("telaInicial.ui")
telaCadastros = uic.loadUi("telaCadastros.ui")
telaConsultas = uic.loadUi("telaConsultas.ui")
telaCadUsuario = uic.loadUi("telaCadastroUsuario.ui")
telaConUsuario = uic.loadUi("telaConsultaUsuario.ui")
telaCadVeiculo = uic.loadUi("telaCadastroVeiculo.ui")
telaCadReserva = uic.loadUi("telaCadReserva.ui")
telaConVeiculo = uic.loadUi("telaConsultaVeiculo.ui")


telaLogin.botaoLogin.clicked.connect(login)


telaLogin.show()
app.exec()

'''        #   CONSULTA DE VEÍCULO
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
