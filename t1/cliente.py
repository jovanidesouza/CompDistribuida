import socket
import time
import pickle

HOST = '127.0.0.1'
PORT = 4002
dest = (HOST, PORT)
id = 0
vclock=[0,0,0]

y = {'id':0, 'vc':[0,0,0], 'msg':'oloa'}
data=pickle.dumps(y)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect(dest)
print('Para sair use CTRL+Z\n')
msg = input("Digite a mensagem para o servidor\n")
#mensagem = msg.encode()

tcp.send(data)
time.sleep(5)
tcp.close()
