#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import pickle
import argparse
import sys
import os

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

    def rodar(self):
        try:
            self.tcp.bind(self.origem)
        except PermissionError:
            print("Erro de permissao de porta ver o numero do erro")
            exit(0)

        self.tcp.listen(1)
        while True:
            con, cliente = self.tcp.accept()
            self.conexao = con
            print ('Conetado por', cliente)
            while True:
                dados_byte = self.conexao.recv(self.tamBuffer)
                msg = str(dados_byte).split(" ")
                print(msg[1])
                self.navegadorDir(msg[1])

                if not msg: break

            print ('Finalizando conexao do cliente', cliente)
            con.close()

    #Metodos para navegar nos diretorios
    def navegadorDir(self, msg):
        #if type(msg) == 'NoneType':
        #    print ("error")

        #if msg[-1] == "/":
        #    msg = msg[:len(msg)-1]
        #    print("hahahah")

        #verifica se é diretorio raiz
        #if len(msg) == 0:
        #    print ("diretorio raiz")

        #verifica se é arquivo
        if "." in msg:

            #msg.split(".")[1]
            arq = open(msg[1:], "rb")
            arquivo = arq.read()
            saida = "HTTP/1.1 200 OK\r\nContent-Type: image/jpg \r\nContent-Length: "+str(len(arquivo))+"\r\n\r\n"
            saida2 = saida.encode()+arquivo
            self.conexao.send(saida2)


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
