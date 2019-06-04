import socket
import os
import sys
import _thread
import time
import pickle
import random

def recebe():
    #print('teste\n')
    HOST = '127.0.0.1'              # Endereco IP do Servidor
    PORT = 5000 + id                # Porta que o Servidor esta ouvindo, 5000 mais o id
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(10)

    while 1:

        con, cliente = tcp.accept()
        recebe = con.recv(1024)
        msg = pickle.loads(recebe)

        if msg['flag'] == 1:#recebe pedido de inserção
            a = msg['rg']
            a = (a % 10) + 1
            insere(msg, a)

        elif msg['flag'] == 2:#recebe mensagem para fazer consulta, faz consulta e responde
            #print('Requisição de consulta.\n')
            for z in memoria:
                if msg['rg'] == z['rg']:
                    #print('achou', z['nome'])
                    msg['nome'] = z['nome']
                    msg['flag'] = 3
                    envia(msg)

        elif msg['flag'] == 3:#recebe mensagem da consulta e exibe resultado
            print('Resposta da consulta.\n')
            print('Nome encontrado:',msg['nome'])
            time.sleep(1)


###############fim recebe#################################################################
def envia(reg):
    #print('teste\n')
    HOST = '127.0.0.1'
    PORT = 5000 + dest
    destino = (HOST, PORT)
    tcp1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp1.connect(destino)
    data=pickle.dumps(reg)
    tcp1.send(data)
    tcp1.close()

def insere(tupla, hash):
    #memoria[hash] = tupla
    while hash <= end:#tenta inserir ate chegar ao fim da memoria
        d = memoria[hash]
        if d['rg'] == 0:#se estiver vazia, insere aqui
            memoria[hash] = tupla
            break
        else:
            hash += 1


def consulta(con):
    print('Consulta...\n')
    for s in memoria:
        if s['rg'] == con:
            print('Nome encontrado no Banco local:',s['nome'])
    time.sleep(2)

def vermemoria():

    for l_num, r in enumerate(memoria, 0):
        if r['rg'] != 0:
            print('índice:',l_num,' RG:', r['rg'],' Nome:', r['nome'])
    time.sleep(5)


################################################################################

#start thread
try:
    _thread.start_new_thread(recebe, ())
except:
    print('Erro ao criar thread')

################################################################################

id = int(sys.argv[1])
dest = int(input('informe o ID do nodo vizinho.\n'))
start = ((id - 1) * 5) + 1
end = (id * 5)

memoria = [0,0,0,0,0,0,0,0,0,0]
x = {'rg': 0, 'nome': '#', 'flag': 0}
y = 0
while y < 10:
    memoria[y] = x
    y = y + 1
#print(memoria)

while 1:

    os.system('clear')
    print('Alocação de memória de ',start, 'até ', end)
    print('-----------------------------')
    op = int(input('Digite 1 para inserir dados.\nDigite 2 para fazer consulta.\nDigite 3 para ver memoria local.\n'))

    if op == 1:#inserir
        print('Inserção:\n')
        rg = int(input('infome o RG\n'))
        nome = input('informe o Nome\n')
        registro = {'rg':rg, 'nome':nome, 'flag': 1}
        indice = (rg % 10) + 1

        if indice >= start and indice <= end:
            insere(registro, indice)
        else:
            print('Enviando pra outro nodo...\n')
            envia(registro)
            time.sleep(1)

    elif op == 2:#consultar
        print('Consulta:\n')
        cons = int(input('Informe o RG para consulta:\n'))
        indice = (cons % 10) + 1

        if indice >= start and indice <= end:
            consulta(cons)
        else:
            #print('dado em outro nodo.\n')
            c = {'rg': cons, 'nome': '#', 'flag': 2}
            envia(c)
            time.sleep(2)

    elif op == 3:
        vermemoria()

    else:
        print('opção inválida')
        time.sleep(1)
