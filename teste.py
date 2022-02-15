import pymysql.cursors
from contextlib import contextmanager
from datetime import date

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


def consultaVarios(sql):
    with conecta() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

def buscaCombobox(sql, chave):
    busca = consultaVarios(sql)
    cb = []
    for v in busca:
        cb.append(v[chave])
    return cb

dataHj = str(date.today())
ano = dataHj[0:4]
mes = dataHj[5:7]
dia = dataHj[8:]
print('ano: ' + ano)
print('mes: ' + mes)
print('dia: ' + dia)
print(dataHj)
