import socket
HOST = ''              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
orig = (HOST, PORT)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socket tcp
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#zera o time wait do socket
tcp.bind(orig)
tcp.listen(10)#limite de conexões
while True:
    print('Aguardando Cliente...\n')
    con, cliente = tcp.accept()
    print('Conectado por', cliente)
    recebe = con.recv(1024)
    print('Mensagem recebida: ',recebe.decode())
    print('Finalizando conexao do cliente', cliente)
    con.close()
