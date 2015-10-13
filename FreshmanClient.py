# -*- encoding: latin1 -*-

import socket
import sys
import struct
import pickle
import time
import os

loggedUser = None

def enviar( tipo, origem, destino, mensagem ):    
    # Criar o socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Ligar o socket � porta onde o servidor est� a ouvir
    servidor = ("192.168.1.128", 7000)
    #print("A ligar ao servidor em %s na porta %s" %servidor )
    sock.connect( servidor )
    
    toSend = [ tipo, origem, destino, mensagem ]
    packed_data = pickle.dumps(toSend)
    
    try:
        sock.sendall( packed_data )
        
        #� espera da resposta do servidor
        while True:
            if ( tipo=="R" or tipo=="N"):
                data = sock.recv(1024)
                received = pickle.loads(data)
            else:            
                data = sock.recv(128)
                received = data.decode('latin1')
            if ( data is None ):
                print ("Erro na liga��o")
            else:
                break;
    finally:
        #print("A terminar a liga��o")
        sock.close()
        
    return received
        
def registo():
    global loggedUser
    print("\nEste � o processo de registo no servidor.")
    print("Tamanho M�ximo de 8 caracteres.")
    while True:
        user = input(" O seu username: ")
        if ( len(user) < 8 ):
            yn = enviar("C", user , "N/D", "N/D" )
            if ( yn == "UserAlreadyExists" ):    # O Username j� existia
                print("O Username j� existe")                
                return False
            if ( yn == "UserLogged" ):
                print("Registo efectuado")
                loggedUser = user
                return True
            else:
                print("Ocorreu um erro")
                return False
        else:
            print("Username demasiado comprido. (M�x: 8 caracteres )")

def pedirMensagem():
    print("Qual o username para onde pretende mandar a mensagem?")
    u = input(": ")
    while True:
        print("Qual a mensagem que pretende enviar? (M�x: 40 carateres)")
        m = input(": ")
        if ( len(m) < 40 ):
            break
        else:
            print("Mensagem demasiado longa. O m�ximo s�o 40 carateres.")
    ret = enviar( "W", loggedUser, u, m )
    if ( ret == 'FailedToDeliver' ):
        print("O utilizador para o qual tentou enviar a mensagem n�o est� disponivel.")
    if ( ret == "MessageDelivered" ):
        print("A sua mensagem foi entregue")
    
def lerMensagens():
    
    messages = enviar("R", loggedUser, "N/D", "N/D" )
    i = 0
    while i < len(messages) :
        print("\nEnviado por: %s " % (messages[i][0]) )
        print( messages[i][1] )
        i = i + 1
    
def starter():
    
    print("Bem-vindo ao myChat\n")
    print("Selecione uma op��o\n")
    print(" 1 - Log In ")
    print(" X - Terminar o programa")
    while True:
        opt = input(": ")
        if ( opt == '1' ):
            while True:
                end = registo()
                if end:
                    return True
        if ( opt == 'X' ):
            return False
        else:
            print("Op��o Inv�lida ")
    
def run():
    opt = starter()
    if not opt:
        return 0
    
    
    while True:
        nf = enviar( "N", loggedUser, "N/D", "N/D" )
        print("\nUtilizador atual: %s" %loggedUser )
        print("Selecione uma op��o\n")
        print(" 1 - Enviar uma mensagem " )
        print(" 2 - Ler Mensagens (%s)  " %nf )
        print(" 3 - Atualizar mensagens ")
        print(" X - Terminar o programa")
        opt = input(": ")
        if ( opt == '1' ):
            pedirMensagem()
        elif ( opt == '2' ):
            lerMensagens()
        elif ( opt== '3' ):
            continue
        elif ( opt == 'X' ):
            print("Adeus")
            break
        else:
            print("Op��o Inv�lida")
run()