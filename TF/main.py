import socket
import os
import sys
import _thread
import time
import pickle
import random

def recebe():
    HOST = '127.0.0.1'              # Endereco IP do Servidor
    PORT = 5000 + id                # Porta que o Servidor esta ouvindo, 5000 mais o id
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(50)

    while 1:

        con, cliente = tcp.accept()
        recebe = con.recv(1024)
        msg = pickle.loads(recebe)
        #####
        if msg['flag'] == 1:#se for um aviso de atividade
            if msg['id'] not in vetor_vizinhos:#se o vizinho não é conhecido
                vetor_vizinhos.append(msg['id'])#cria lista de vizinhos
                aux = msg['id'] + 5000 #utiliza o id da msg, como destino da resposta
                msg1 = msg.copy()#cria uma nova msg para responder
                msg1['id'] = id #insere seu proprio id na resposta
                envia(msg1, aux)# envia a resposta para o nodo avisou estar ativo
                #fim
        if msg['flag'] == 2:#se for uma att de memoria
            atualiza()
            #caso receba essa mensagem, atualiza os endereços de memoria compartilhada
        if msg['flag'] == 3: # se for uma inserção
            r = msg['rg'] % tam_memoria
            r = r % 5 #normaliza o indice
            insere(msg, r) #insere localmente os dados
            #time.sleep(5)
        if msg['flag'] == 4:
            try:
                c = consulta(msg['rg'])
                dest_con = msg['id'] + 5000 #endereço de quem requisitou a consulta
                c['flag'] = 5 #altera para resposta da consulta
                envia(c, dest_con)
                #print(c['nome'])
            except:
                pass
        if msg['flag'] == 5: #mostra consulta na tela
            print('\nRegistro encontrado: RG:',msg['rg'], 'Nome:', msg['nome'])
            time.sleep(2)
            #
        if msg['flag'] == 6:
            #remoção
            rm = remove(msg['rg'])
            if rm == True: #se removeu, aviso o requisitante que removeu
                m = msg.copy()
                m['flag'] = 7
                envia(m, m['id']+5000)
        if msg['flag'] == 7: #confirmação de remoção
            print('Removido.\n')
            time.sleep(2)

def envia(reg, dest):#reg = mensagem, dest = destino da mensagem # função usa socket para enviar mensagem.
    HOST = '127.0.0.1'
    PORT = dest
    destino = (HOST, PORT)
    tcp1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp1.connect(destino)
    data=pickle.dumps(reg)
    tcp1.send(data)
    tcp1.close()


def alive():
    m = {'id': id, 'rg': 0, 'nome': '@', 'flag': 1}#cria msg generica
    x = 5000
    while x < 5010:#loop em uma faixa de portas #broadcast
        if x != myport:#não manda para si mesmo
            try:
                envia(m, x)#envia mensagem com flag 1 para o destino x
                pass
            except:
                pass
        x+=1


def indices():#cira um vetor de indices de memoria, do mesmo tamanho do vetor de vizinhos
    y = vetor_vizinhos.copy()
    tam = len(y)
    b = 1
    while b <= tam:
        if b not in v_indices:
            v_indices.append(b)
        b+=1
    #print('indices de memoria', v_indices)
    return v_indices

def atualiza():
    global my_indice
    global share
    share = 1
    #atualiza compartilhamento de memória
    vetor_vizinhos.sort()
    v_indices = indices()#cria o vetor de indices baseado no numero de nodos ativos
    #print('vet indices test', v_indices)
    #acha o indice
    x = 0
    while x < len(vetor_vizinhos):
        if id == vetor_vizinhos[x]:
            #print('meu indice é:', v_indices[x])
            my_indice = v_indices[x]
            break
        x+=1
    #print('\n\nindice na memoria total:', my_indice)
    global tam_memoria
    global start
    global end
    tam_memoria = len(v_indices) * 5#define o tamaho da memoria total, baseado no numero de nodos compartilhando memoria
    start = ((my_indice - 1) * 5) + 1
    end = (my_indice * 5)
    #print('\ninicio da memoria local:',start)
    #print('fim da memoria local:',end)


def send_to_all(data):
    #global vetor_vizinhos
    for x in vetor_vizinhos:
        x = x + 5000
        if x != myport:
            try:
                envia(data, x)
                pass
            except:
                pass

def insere(tupla, hash): # função que insere localmente

    try:#usa try para evitar erro de fim de memória

        while hash <= end:#tenta inserir ate chegar ao fim da memoria local
            d = memoria[hash]
            if d['rg'] == 0:#se estiver vazia, insere aqui
                memoria[hash] = tupla
                break
            else:
                hash += 1
    except: #uma exceção significa que a memoria local está cheia e então é necessário reenviar os dados para outro nodo
        #print('Nodo Sem memoria')
        vetor_vizinhos.sort()
        if vetor_vizinhos[len(vetor_vizinhos)-1] == id: #se eu sou o mais a direita, manda pro primeiro
            envia(tupla, vetor_vizinhos[0]+5000)
        else:# caso nao seja o ultimo, manda pro nodo da direita (f+1)
            f = 0
            while f < len(vetor_vizinhos):
                if vetor_vizinhos[f] == id:
                    f = vetor_vizinhos[f+1] + 5000
                    envia(tupla, f)
                    break

def consulta(dado):
    for n in memoria:
        if n['rg'] == dado:
            return n

def remove(rg):
    for n in memoria:
        if n['rg'] == rg:
            n['id'] = 0
            n['rg'] = 0
            n['nome'] = '#'
            n['flag'] = 0
            return True

#########MAIN##########################

#start thread
try:
    _thread.start_new_thread(recebe, ())
except:
    print('Erro ao criar thread')

id = int(sys.argv[1])
myport = 5000 + id
share = 0
vetor_vizinhos = []
vetor_vizinhos.append(id)#adiciona o proprio id ao vetor de vizinhos
v_indices = []
tam_memoria = 0#valores provisórios
start = 0
end = 0
my_indice = 0

memoria = [0,0,0,0,0]
k = {'id': 0, 'rg': 0, 'nome': '#', 'flag': 0}
l = 0
while l < 5:
    memoria[l] = k
    l = l + 1
#print(memoria)

alive()#faz broadcast nos para os possiveis vizinhos, também requisita uma resposta com o id de quem recebeu a msg

while 1:

    os.system('clear')
    print('NODO:', id)
    print('\nDigite 1 para limpar a tela\nDigite 2 para compartilhar memória\nDigite 3 para ver o status da memória')
    print('Digite 4 para inserir dados\nDigite 5 para consultar dados\nDigite 6 para remover dados')
    op = int(input())

    if op == 1:
        os.system('clear')

    elif op == 2:
        print('Compartilhando memória\n')
        ##
        atualiza()#chama a função que atualiza o compartilhamento de memoria
        m = {'id': id, 'rg': 0, 'nome': '@', 'flag': 2}
        send_to_all(m)
        time.sleep(2)

    elif op == 3:
        print('\nStatus da memória:\n')
        print('Lista de Nodos ativos:', vetor_vizinhos)
        if share == 1:
            print('\nIndices de memória dos nodos:', v_indices)
            print('Tamanho total da memória compartilhada:', tam_memoria)
            print('inicio:', start, 'fim:', end)
            print('\nMemória Local:\n')
            for a in memoria:
                print('RG:', a['rg'], ' Nome:', a['nome'])
        time.sleep(5)

    elif op == 4:#opção para inserir dados na memória
        if share == 0:#não permite inserir caso nao esteja compartilhando memória
            print('Nodo não integra o sistema de memória.\n')
            time.sleep(2)
        else:
            print('\nInserção:\n')
            rg = int(input('infome o RG\n'))
            nome = input('informe o Nome\n')
            registro = {'rg':rg, 'nome':nome, 'flag': 3}
            #print(registro['rg'], registro['nome'])
            data_indice = rg % tam_memoria #calcula o valor hash baseado no tamaho total atual da memoria compartilhada
            if data_indice >= (start - 1) and data_indice <= (end - 1):#verifica se os dados devem ser inseridos localmente
                #calcula o mod de novo para normalizar o indice
                h = data_indice % 5
                insere(registro, h)#chama a  função de inserção, passando o registro e o indice
            else:#envia o registro para outro nodo
                v = int(data_indice / 5) + 1 #faz cast para descobrir nodo para qual deve enviar a msg
                b = vetor_vizinhos[v-1] + 5000 # -1 pra usar indices desde o zero
                envia(registro, b) #envia para o nodo que controla a hash calculada
            print('OK')
            time.sleep(1)

    elif op == 5:
        if share == 0:#não permite consultar caso nao esteja compartilhando memória
            print('Nodo não integra o sistema de memoria.\n')
            time.sleep(2)
        else:
            print('Consulta:\n')
            cons = int(input('Informe o RG para a consulta:\n'))
            try: #tenta consultar localmente os dados
                con_result = consulta(cons)
                print('Registro local encontrado: RG:',con_result['rg'], 'Nome:', con_result['nome'])
                time.sleep(4)
            except: # caso não encontre localmente cria uma mensagem de consulta (4) e envia para todos os vizinhos
                #print('nao ta aqui')
                registro = {'id':id, 'rg':cons, 'nome':'#', 'flag': 4}
                send_to_all(registro)
                time.sleep(4)

    elif op == 6:
        if share == 0: #não permite remoção caso não faça parte do sistema de memoria
            print('Nodo não integra o sistema de memoria.\n')
            time.sleep(2)
        else:
            print('Remoção:')
            rem = int(input('Informe o RG para ser removido:\n'))
            #remove local
            rm = remove(rem)
            if rm == True: #remoção local, se deu certo, avisa na tela
                print('Removido.')
                time.sleep(1)
            else:# se nao removeu local, manda para os outros nodos
            #cria mensagem de remoção
                registro = {'id':id, 'rg':rem, 'nome':'#', 'flag': 6}
                send_to_all(registro)
            time.sleep(2)
            #fim

    else:
        print('opção inválida')
        time.sleep(1)
