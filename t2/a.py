import socket
import os
import sys
import _thread
import time
import pickle

id=0
vclock = [0,0,0]

####
# with open('log.txt', 'w') as arq:
#         print(vclock, file=arq)
################################################################
#função de recebimento da _thread
def recebe():

    HOST = '127.0.0.1'              # Endereco IP do Servidor
    PORT = 5000            # Porta que o Servidor esta ouvindo
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(10)

    while True:
        print('Aguardando Conexão\n')
        con, cliente = tcp.accept()
        print('Conectado por', cliente)
        recebe = con.recv(1024)
        vclock[id] += 1
        msg = pickle.loads(recebe)
        print('Mensagem recebida: ', msg['msg'])
        print('vetor de relógios ', msg['vc'])
        print('Finalizando conexão com o vizinho ', msg['id'])

        aux = msg['vc']
        i = 0
        while i < 3:
            if aux[i] > vclock[i]:
                vclock[i] = aux[i]
            i += 1
        print('vetor atualizado ', vclock)

        con.close()
######FIM DA RECEBE############################################
try:
    _thread.start_new_thread(recebe, ())
except:
    print('Erro ao criar thread')

###############################################################

while 1:
    time.sleep(2)
    send_flag = int(input("Digite o destino da mensagem\n\n"))
    if id == send_flag:
        print('erro, o destino é o mesmo que a origem\n')

    if send_flag == 1:
        HOST = '127.0.0.1'
        PORT = 5001
    elif send_flag == 2:
        HOST = '127.0.0.1'
        PORT = 5002
    else:
        print('Servidor não conhecido\n')

    destino = (HOST, PORT)
    tcp1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp1.connect(destino)
    msg = input("Digite a mensagem para o servidor\n")
    y = {'id':0, 'vc':[0,0,0], 'msg':'ola'}
    y['msg'] = msg
    vclock[id] += 1
    y['vc'] = vclock
    data=pickle.dumps(y)
    tcp1.send(data)
    time.sleep(3)
    tcp1.close()
