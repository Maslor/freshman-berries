# -*- encoding: latin1 -*-

# myChat Server 1.0

import socket
import sys
import struct
import pickle

logged = []
messages = []

def login( username ):
    logged.append(username)
    messages.append([])

def logout( username ):
    u = logged.index(username)
    logged.pop(u)
    messages.pop(u)

def isLogged( username ):
    u = None
    try:
        u = logged.index(username)
    except :
        pass
    return u is not None

def addMessage( username, sender, message ):
    u = logged.index(username)
    messages[u].append( [message, sender, False] )
    
# Só lê messagens não lidas
def readMessages( username, modo ):
    u = logged.index(username)
    unread = []
    leng = len( messages[u]) -1
    i=0
    while i<=leng:
        if not ( messages[u][i][2] ):
            unread.append( [messages[u][i][1], messages[u][i][0]] )
            if ( modo == 0 ):
                messages[u][i][2] = True
        i += 1
    return unread

def run():
    # Cria um socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Liga a socket ao porto de ligação
    servidor = ("192.168.1.128", 7000)
    print("Servidor a correr em %s na porta %s" % servidor)
    sock.bind( servidor )
    
    # Abrir a porta para receber ligações
    sock.listen(1)
    
    # Esperar ligações
    while True :
        print("À espera de ligações")
        ligacao, cliente = sock.accept()
        
        try:
            data = ligacao.recv(1024)
            received = pickle.loads(data)
            
            print("Recebida uma mensagem")
            if ( received[0]=='C' ):
                if isLogged( received[1] ):
                    print( "O utilizador %s já existe" %received[1] )
                    ligacao.sendall( "UserAlreadyExists".encode('latin1') )
                else:
                    login( received[1] )
                    print( "Criado o utilizador %s" %logged[ len(logged)-1])
                    ligacao.sendall( "UserLogged".encode('latin1') )
            if ( received[0]=='W' ):
                if not isLogged( received[2] ): 
                    print( "O utilizador %s não existe" %received[2] )
                    ligacao.sendall( "FailedToDeliver".encode('latin1') )
                else:
                    addMessage( received[2], received[1], received[3] )
                    print( "Mensagem entregue")
                    ligacao.sendall( "MessageDelivered".encode('latin1') )
            if ( received[0]=='R' ):
                print("A enviar as mensagens não lidas")
                mes = readMessages( received[1], 0 )
                mes_string = pickle.dumps(mes)
                ligacao.sendall( mes_string )
            if ( received[0]=="N" ):
                print("A enviar numero de mensagens")
                mes = readMessages( received[1], 1 )
                len_string = pickle.dumps( str(len(mes)) )
                ligacao.sendall( len_string )
            if ( received[0]=='X' ):
                break
            if ( received is None ):
                print("Erro")
            
        finally:
            ligacao.close()        # Fecha a ligação em casos regulares e em casos de erro
            
            
run()
input("Press any button to close")