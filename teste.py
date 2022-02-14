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

comboTipos = buscaCombobox('SELECT * FROM tipos', 'tipo')
comboMarcas = buscaCombobox('SELECT * FROM marcas', 'marca')
comboCores = buscaCombobox('SELECT * FROM cores', 'cor')

print(comboTipos)
print(comboMarcas)
print(comboCores)
