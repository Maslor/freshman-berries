# -*- encoding: latin1 -*-
#FRESHMAN BERRIES
#Servidor
#Version: 8.1
#Author: NEETI

import socket

mensagens = []
users = []

def addMessage( user, mensagem ):
    u = users.index( user )
    mensagens[u].append( mensagem )
    
def login( user ):
    u = None
    try:
        u = users.index(username)
    except :
        pass

    if ( u is None ):
        users.append( user )
        mensagens.append([])

def leMensagens( user ):
    u = users.index( user )
    unread = []
    for m in mensagens[u]:
        unread.append( m )
    mensagens[u] = [] 
    return unread

def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    servidor = ("localhost", 4000 )
    print("Servidor a correr em %s na porta %s" % servidor)
    sock.bind( servidor )
    sock.listen(1)      
    
    while True:
        print("À espera de ligações")
        ligacao, cliente = sock.accept()         
        try :  
            data = ligacao.recv(1024)
            data = data.decode('latin1')            
            splited = data.split()
            modo = splited[0]
            user = splited[1]
            a = len(modo) + len(user) + 2
            mensagem = data[a:]
            
            if ( modo[:2] == "/r" ):
                
                toSend = leMensagens( user )
                print(toSend)
                for m in toSend:
                    ligacao.sendall( m.encode('latin1') )
                ligacao.sendall( "/EOF".encode('latin1') )
            if ( modo[:2] == "/s" ):                
                login( user )
                addMessage( user, mensagem )
            else:
                continue
                
        finally:
            ligacao.close()
            
try:
    run()
except Exception as ex:
    print (ex)
    input()