# -*- encoding: latin1 -*-
#FRESHMAN BERRIES
#Cliente
#Version: 8.1
#Author: NEETI

import socket

def enviar( mensagem ):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor=('neetiproj.tagus.ist.utl.pt', 4000)
    sock.connect( servidor )
    mensagens = []
    
    try: 
        msg = mensagem.encode('latin1')        
        sock.sendall( msg )
                
        if ( mensagem[:2] == "/r" ):
            while True:
                data = sock.recv(2048)
                data = data.decode('latin1')
                if ( data is not None ):
                    mensagens.append(data)
                    break;
                    
    finally:
        sock.close()
        
    return mensagens
        
def menu():
    a = None
    while ( a is not "/x" ):
        a = str(input(": "))
        d = enviar(a)
        if ( d is not None ):
            for m in d:
                print(m)
   
''' try:
    menu()
except Exception as ex:
    print (ex)
    input() '''