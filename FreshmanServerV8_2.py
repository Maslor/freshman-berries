# -*- encoding: latin1 -*-
#FRESHMAN BERRIES
#Servidor
#Version: 8.2
#Author: NEETI

import socket

# Variáveis Globais:

utilizadores = []
mensagens = []

#IP = "localhost"
IP = "neetiproj.tagus.ist.utl.pt"
PORTA = 4000 

# Funções Auxiliares:

# Coloca uma mensagem no array de mensagens correspondente ao utilizador
def adicionaMensagem( utilizador, mensagem ):
	u = utilizadores.index( utilizador )
	mensagens[u].append( mensagem )

# Adiciona um utilizador ao array de utilizadores
def login( utilizador ):
	u = None
	try:
		u = utilizadores.index( utilizador )
	except:
		pass

	if ( u is None ):
		utilizadores.append( utilizador )
		mensagens.append([])

# Retorna as mensagens que um utilizador tem por ler
def leMensagens( utilizador ):
	u = utilizadores.index( utilizador )
	porLer = []					
	for m in mensagens[u]:
		porLer.append( m )
	mensagens[u] = [] 			# Apaga as mensagens que o utilizador tinha para não voltarem a ser lidas
	return porLer

# Função main:
def main():
	# Cria uma socket TCP
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Inicia o servidor no IP e PORTA indicados
	servidor = ( IP, PORTA )
	print("Servidor a correr em %s na porta %s" % servidor)
	sock.bind( servidor )
	sock.listen(1)   

	#Fica à espera de ligações
	while True:
		print("� espera de liga��es")
		ligacao, cliente = sock.accept()
		try:
			data = ligacao.recv(2048)
			data = data.decode('latin1')    # Descodificação de bytes para texto
			argumentos = data.split()       # Separa a mensagem a cada espaço
			modo = argumentos[0] 			# Modo de execução (/r ou /s)
			utilizador = argumentos[1]			# O utilizador a quem é direcionado o comando
			mensagem = data[ (len(modo) + len(utilizador) + 2):]     # A mensagem original menos os primeiros 2 carateres, o nome do utilizador e os 2 espaços.
			if ( modo == "/r" ):
				paraEnviar = leMensagens ( utilizador )
				for m in paraEnviar :
					ligacao.sendall( m.encode('latin1') )
				ligacao.sendall( "/EOF".encode('latin1') )

			if ( modo == "/s" ):
				login( utilizador )
				adicionaMensagem( utilizador, mensagem )
			else:
				continue

		finally:
			ligacao.close()

try:
    main()
except Exception as ex:
    print (ex)
    input()