from funcionario import Funcionario
from cliente import Cliente
from reserva import Reserva
from veiculo import Veiculo
from datetime import date
import pymysql.cursors
from contextlib import contextmanager
from PyQt5 import uic, QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidgetItem


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


#   INSERE OS DADOS NO BANCO
def insere(sql):
    with conecta() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            conexao.commit()
            print('\033[1;32mInserido com SUCESSO!!!\033[m')


#   USADO APENAS PARA PREENCHER AS COMBOBOX
def buscaCombobox(sql, chave):
    busca = consultaVarios(sql)
    cb = []
    for v in busca:
        cb.append(v[chave])
    return cb


#   CONSULTA NO BANCO E RETORNA APENAS UMA OCORRÊNCIA
def consulta(sql):
    with conecta() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            return result


#   CONSULTA NO BANCO E RETORNA VARIAS OCORRÊNCIAS
def consultaVarios(sql):
    with conecta() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result


#   LOGOUT
def logout():
    telaLogin.tbLogin.clear()
    telaLogin.tbSenha.clear()
    telaInicial.close()
    telaLogin.show()


#   LOGIN
def login():
    telaLogin.alertaLogin.setText('')
    usuario = telaLogin.tbLogin.text()
    senha = telaLogin.tbSenha.text()
    senha_banco = consulta(f"SELECT senha FROM funcionarios WHERE login = '{usuario}'")
    if senha_banco is None:
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


#   TELA DE MENU INICIAL
def menuInicial(usuario):
    nomeUsuario = consulta(f"SELECT nome FROM funcionarios WHERE login = '{usuario}'")
    telaInicial.show()
    telaInicial.boasVindas.setText(f'Bem-vindo {nomeUsuario["nome"]}')
    telaInicial.btSair.clicked.connect(logout)
    telaInicial.btCad.clicked.connect(menuCadastros)
    telaInicial.btCon.clicked.connect(menuConsultas)


#   TELA MENU DE CADASTROS
def menuCadastros():
    telaCadastros.show()
    telaInicial.close()
    telaCadastros.btCadUsuario.clicked.connect(cadUsuario)
    telaCadastros.btCadVeiculo.clicked.connect(chamaCadVeiculo)
    telaCadastros.btCadReserva.clicked.connect(chamaCadReserva)
    telaCadastros.btVoltar.clicked.connect(voltarCad)


#   TELA MENU DE CONSULTAS
def menuConsultas():
    telaConsultas.show()
    telaInicial.close()
    telaConsultas.btConUsuario.clicked.connect(conUsuario)
    telaConsultas.btConVeiculo.clicked.connect(tConVeiculo)
    telaConsultas.btConReserva.clicked.connect(tConReserva)
    telaConsultas.btVoltar.clicked.connect(voltarCon)


#   TELAS CADASTRO DE USUÁRIOS (FUNCIONÁRIO E CLIENTE)
def cadUsuario():
    telaCadUsuario.show()
    telaInicial.close()
    telaCadUsuario.btCadFuncionario.clicked.connect(telaCadUsuario.frameCadFuncionario.show)
    telaCadUsuario.btCadastrarFuncionario.clicked.connect(cadFuncionario)
    telaCadUsuario.btCadastrarCliente.clicked.connect(cadCliente)
    telaCadUsuario.btCadCliente.clicked.connect(telaCadUsuario.frameCadFuncionario.close)
    telaCadUsuario.btVoltar.clicked.connect(telaCadUsuario.close)


#   EFETUA O CADASTRO DO FUNCIONÁRIO
def cadFuncionario():
    funcionario = Funcionario(telaCadUsuario.tbNomeFuncionario.text(),
                              telaCadUsuario.tbLoginFuncionario.text(),
                              telaCadUsuario.tbSenhaFuncionario.text(),
                              telaCadUsuario.tbMatriculaFuncionario.text())
    insere(f"INSERT INTO funcionarios VALUES (DEFAULT, '{funcionario.nome}', '{funcionario.login}', "
           f"'{funcionario.senha}', '{funcionario.matricula}')")
    telaCadUsuario.tbNomeFuncionario.clear()
    telaCadUsuario.tbLoginFuncionario.clear()
    telaCadUsuario.tbSenhaFuncionario.clear()
    telaCadUsuario.tbMatriculaFuncionario.clear()


#   EFETUA O CADASTRO DO CLIENTE
def cadCliente():
    cliente = Cliente(telaCadUsuario.tbNomeCliente.text(),
                      telaCadUsuario.tbLoginCliente.text(),
                      telaCadUsuario.tbSenhaCliente.text(),
                      telaCadUsuario.tbCPFCliente.text(),
                      telaCadUsuario.tbCNHCliente.text(),
                      telaCadUsuario.tbNCartaoCliente.text(),
                      telaCadUsuario.tbTelefoneCliente.text(),
                      telaCadUsuario.tbEnderecoCliente.text())
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


#   ABRE A JANELA DO CADASTRO DE VEÍCULO
def chamaCadVeiculo():
    telaCadVeiculo.show()
    telaCadVeiculo.btVoltar.clicked.connect(telaCadVeiculo.close)
    telaCadVeiculo.btCadastrarCliente.clicked.connect(cadVeiculo)
    telaCadVeiculo.cbTipoVeiculo.addItems(buscaCombobox('SELECT * FROM tipos', 'tipo'))
    telaCadVeiculo.cbMarcaVeiculo.addItems(buscaCombobox('SELECT * FROM marcas', 'marca'))
    telaCadVeiculo.cbCorVeiculo.addItems(buscaCombobox('SELECT * FROM cores', 'cor'))


#   EFETUA O CADASTRO DO VEÍCULO
def cadVeiculo():
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
    insere(
        f"INSERT INTO veiculos VALUES (DEFAULT, '{tipo['id_tipo']}', '{marca['id_marca']}', '{cor['id_cor']}', "
        f"'{veiculo.modelo}', '{veiculo.n_chassi}', '{veiculo.ano}', '{veiculo.placa}', '{veiculo.valor_diaria}')")
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
    if nomeCli is None:
        telaCadReserva.labelCliente.setText('CLIENTE NÃO EXISTE!')
    else:
        telaCadReserva.labelCliente.setText(f'Cliente: {nomeCli["nome"]} CPF: {nomeCli["cpf"]}')
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
           f"(DEFAULT, '{reserva.cliente}', '{reserva.veiculo}', '{reserva.data_agendamento}', '{reserva.data_inicio}',"
           f" '{reserva.periodo}', '{reserva.valor_total}')")


#   TELA CONSULTA DE CLIENTE
def conUsuario():
    telaConUsuario.show()
    telaConUsuario.btConFuncionario.clicked.connect(telaConUsuario.frameConFuncionario.show)
    telaConUsuario.btConCliente.clicked.connect(telaConUsuario.frameConFuncionario.close)
    telaConUsuario.btVoltar.clicked.connect(telaConUsuario.close)
    telaConUsuario.btExcluir.clicked.connect()
    telaConUsuario.btConsultarFuncionario.clicked.connect(conFuncionario)
    telaConUsuario.btConsultarCliente.clicked.connect(conCliente)


def exFuncionario():
    funcionario = consulta(f"SELECT * FROM funcionarios WHERE matricula = "
                           f"'{telaConUsuario.tbMatricula.text()}'")
    if funcionario is None:
        telaConUsuario.labelNomeFunc.setText('MATRICULA NÃO CADASTRADA')
    else:
        insere(f"DELETE FROM funcionarios WHERE matricula = "
               f"'{telaConUsuario.tbMatricula.text()}'")


#   CONSULTA FUNCIONÁRIO
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
        telaConVeiculo.labelValorDiariaVei.setText('R$ ' + str(veiculo['valor_diaria']))


def tConReserva():
    telaConReserva.show()
    telaConReserva.btVoltar.clicked.connect(telaConReserva.close)
    telaConReserva.btConsultaReserva.clicked.connect(conReserva)


def conReserva():
    cpfReserva = telaConReserva.tbCPFReserva.text()
    resultado = consultaVarios(f"SELECT c.nome, v.modelo, r.data_agendamento, r.data_inicio, r.periodo, r.valor_total "
                               f"FROM reservas AS r "
                               f"JOIN clientes AS c "
                               f"ON c.id_cliente = r.fk_id_cliente "
                               f"JOIN veiculos AS v "
                               f"ON v.id_veiculo = r.fk_id_veiculo "
                               f"WHERE c.cpf = '{cpfReserva}'")

    if resultado == None or (len(resultado) == 0):
        telaConReserva.labelNaoCad.setText('Nenhuma Reserva Cadastrada para esse CPF')
    else:
        for indice, valorL in enumerate(resultado):
            telaConReserva.resultado.insertRow(indice)
            for iDic, valorD in enumerate(valorL.items()):
                telaConReserva.resultado.setItem(indice, iDic, QTableWidgetItem(str(valorD[1])))
    telaConReserva.tbCPFReserva.clear()


app = QtWidgets.QApplication([])
telaLogin = uic.loadUi("telas/telaLogin.ui")
telaInicial = uic.loadUi("telas/telaInicial.ui")
telaCadastros = uic.loadUi("telas/telaCadastros.ui")
telaConsultas = uic.loadUi("telas/telaConsultas.ui")
telaCadUsuario = uic.loadUi("telas/telaCadastroUsuario.ui")
telaConUsuario = uic.loadUi("telas/telaConsultaUsuario.ui")
telaCadVeiculo = uic.loadUi("telas/telaCadastroVeiculo.ui")
telaCadReserva = uic.loadUi("telas/telaCadReserva.ui")
telaConVeiculo = uic.loadUi("telas/telaConsultaVeiculo.ui")
telaConReserva = uic.loadUi("telas/telaConsultaReserva.ui")

telaLogin.botaoLogin.clicked.connect(login)

telaLogin.show()
app.exec()
