import socket
import os
import sys
import _thread
import time
import pickle
import random


def acordo():
    #abre o arquivo e obtem a lista de nodos
    with open('status.txt', 'r') as arq:
        nodos = arq.read().splitlines()
    nodos = list(map(int, nodos))
    maior = 0
    for y in nodos:
        if y > maior:
            maior = y
    lider[0] = maior
    #print('lider é',lider[0])

def mostralider():

    if lider[0] == 0:
        print('Lider indefinido.\n')
    else:
        print('O Lider é o Nodo:', lider[0])

def insere(tupla):
        tabela.append(tupla)

def mostratabela():
    for y in tabela:
        print('Mensagem:', y['msg'], 'De:',y['id'],'Enviada Por:', y['sid'])

def acha_impostor():
    for y in tabela:
        if y['msg'] == 'Não atacar base Sul':
            impostores.append(y['sid'])
    print('O/os impostor/es são:', impostores)


def recebe():

    HOST = '127.0.0.1'              # Endereco IP do Servidor
    PORT = 5000 + id            # Porta que o Servidor esta ouvindo, 5000 mais o id
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(10)

    while 1:

        time.sleep(1)
        con, cliente = tcp.accept()
        recebe = con.recv(1024)
        msg = pickle.loads(recebe)

        if msg['flag'] == 1:
            print('\nAcordo de liderança requisitado.\n')
            acordo()
        elif msg['flag'] == 2:#recebe e retransmite mensagem
            print('Mensagem recebida:', msg['msg'],'De:', msg['sid'])
            msg1 = msg.copy()
            insere(msg1)
            ###prepara retrasmissão
            msg['flag'] = 3#define como retrasmissão
            msg['sid'] = id #atribui id para identificar mensagem
            a = random.randrange(1, 11, 1)
            if a > 5:#probabilidade de mensagem falsa
                msg['msg'] = 'Não atacar base Sul'
            else:#mensagem verdadeira
                msg['msg'] = 'Atacar base Sul'
            envia(msg)
        elif msg['flag'] == 3:#recebe mensagem retrasmitida
            insere(msg)
            print('R: Mensagem recebida:', msg['msg'],'De:', msg['sid'])

def envia(dict):#obtem lista de nodos, e envia para todos, menos para o lider e pra si memsmo

    dict1 = dict

    with open('status.txt', 'r') as arq:
        linhas = arq.read().splitlines()
    linhas = list(map(int, linhas))#obtem lista de vizinos

    HOST = '127.0.0.1'
    for x in linhas:#envia solicitação de acorodo  para todos
        if x != id: #nao manda para si mesmo
            if x != lider[0]:#nao manda para o lider
                PORT = 5000 + x
                destino = (HOST, PORT)
                tcp1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp1.connect(destino)
                data=pickle.dumps(dict1)
                tcp1.send(data)
                tcp1.close()


#########################MAIN############
id = int(sys.argv[1])
lider = [0]
tabela = []
impostores = []
mensagem = {'msg': 'Acordo', 'id': id, 'flag': 0, 'sid' : id}

#start thread
try:
    _thread.start_new_thread(recebe, ())
except:
    print('Erro ao criar thread')

with open('status.txt', 'a') as arq:
    print(id, file=arq)

#print(dict)

while 1:

    #time.sleep(1)
    os.system('clear')
    print('Nodo:',id)
    entrada = int(input("\nDigite 1 para iniciar acordo de lider.\nDigite 2 para enviar mensagem.\nDigite 3 para mostrar tabela de mensagens.\nDigite 4 para exibir Lider\n\n"))

    if entrada == 1:#
        mensagem['flag'] = 1
        envia(mensagem)
        acordo()
    elif entrada == 2:
        if id != lider[0]:
            print('Apenas o lider pode iniciar uma trasmissão de mensagens.\n')
            time.sleep(2)
        else:
            mensagem['flag'] = 2
            #mensagem['sid'] = id
            a = random.randrange(1, 11, 1)
            if a > 8:#probabilidade baixa, mensagem falsa
                mensagem['msg'] = 'Não atacar base Sul'
            else:#mensagem verdadeira
                mensagem['msg'] = 'Atacar base Sul'
            envia(mensagem)
    elif entrada == 3:
        #print(tabela)
        mostratabela()
        acha_impostor()
        time.sleep(10)
        os.system('clear')
        #mostrar tabela e achar impostor
    elif entrada == 4:
        mostralider()
        time.sleep(2)
    else:
        print('erro de entrada')
