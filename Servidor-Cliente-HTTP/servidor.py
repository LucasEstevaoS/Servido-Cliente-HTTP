#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import pickle
import argparse
import sys
import os
import _thread

# Endereco IP do Servidor
HOST = 'localhost'
# Porta que o Servidor esta
PORT = 80
class Servidor(object):
    def __init__(self, porta, tamBuffer):
        self.origem = ('', porta)
        self.porta = porta
        self.tamBuffer = tamBuffer
        self.conexao = None
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, con, cliente):
        print ('Conetado por', cliente)
        while True:
            dados_byte = self.conexao.recv(self.tamBuffer)
            msg = str(dados_byte).split(" ")
            print(msg[1])
            self.navegadorDir(msg[1])
            if not msg: break
        print ('Finalizando conexao do cliente', cliente)
        con.close()
        _thread.exit()

    def rodar(self):
        try:
            self.tcp.bind(self.origem)
        except PermissionError:
            print("Erro de permissao de porta")
            exit(0)

        self.tcp.listen(1)
        while True:
            con, cliente = self.tcp.accept()
            self.conexao = con
            _thread.start_new_thread(self.connect, tuple([con, cliente]))
        self.tcp.close()


    #Metodos para navegar nos diretorios
    def navegadorDir(self, msg):
        if type(msg) == 'NoneType':
            print ("error")

        #tira a / do final
        if msg[-1] == "/":
            msg = msg[:len(msg)-1]


        #verifica se é diretorio raiz
        if len(msg) == 0:
            print ("diretorio raiz")
            dirs = os.listdir("/")
            saida = "HTTP/1.1 200 OK\r\nContent-Type:text/txt \r\nContent-Length: "+str(len(dirs))+"\r\n\r\n"
            saida2 = saida.encode()+dirs
            self.conexao.send(saida2)
            self.conexao.close()


        #verifica se é arquivo
        if "." in msg:


            arq = open(msg[1:], "rb")
            arquivo = arq.read()
            if (msg.split(".")[1]== "html"):
                content = "text/HTML"
            if (msg.split(".")[1]== "txt"):
                content = "text/txt"
            elif (msg.split(".")[1]== "jpg"):
                content = "image/jpg"
            elif (msg.split(".")[1]== "png"):
                content = "image/png"
            elif (msg.split(".")[1]== "gif"):
                content = "image/gif"
            elif (msg.split(".")[1]== "ico"):
                content = "image/ico"
            elif (msg.split(".")[1]== "css"):
                content = "text/css"

            saida = "HTTP/1.1 200 OK\r\nContent-Type:"+content+"\r\nContent-Length: "+str(len(arquivo))+"\r\n\r\n"
            saida2 = saida.encode()+arquivo
            self.conexao.send(saida2)
            self.conexao.close()


            #gerar o codigo html

        #se nao é arquivo nem diretorio raiz, é uma cadeia dde diretorio
        else:
            print("diretorio nao raiz")



def main(argv):
    parse = argparse.ArgumentParser()
    parse.add_argument('-p', '--PORT', required=False, default=80, type=int, help="Numero da porta imbecil")
    args = parse.parse_args()

    if args.PORT:
        PORT = int(args.PORT)
        servidor = Servidor(PORT, 4096)
        servidor.rodar()


if __name__ == "__main__":
    main(sys.argv)
