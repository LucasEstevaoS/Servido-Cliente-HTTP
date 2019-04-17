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
                msg = self.receber()
                self.navegadorDir(msg)
                if not msg: break

            print ('Finalizando conexao do cliente', cliente)
            con.close()

    #Metodos para navegar nos diretorios
    def navegadorDir(self, msg):

        if msg[-1] == "/":
            msg = msg[:len(msg)-1]
            print("hahahah")

        #verifica se é diretorio raiz
        if len(msg) == 0:
            print ("diretorio raiz")

        #verifica se é arquivo
        elif "." in msg:
            print("arquivo")

        #se nao é arquivo nem diretorio raiz, é uma cadeia dde diretorio
        else:
            print("diretorio nao raiz")

        #else :
        #    print(" Comando Invalido 404\n ")

    def enviar(self, msg): # None: requisicao GET
        dados_byte = pickle.dumps(msg)
        self.conexao.send(dados_byte)

    #recebe a mensagem em byte e converte pra caracter
    def receber(self):
        dados_byte = self.conexao.recv(self.tamBuffer)
        #msg = pickle.loads(dados_byte)
        #print("mensagem print:",msg)
        #print("mensagem print:",dados_byte)
        #return msg

        msg = str(dados_byte).split(" ")
        return msg[1]

def main(argv):
    parse = argparse.ArgumentParser()
    parse.add_argument('-p', '--PORT', required=False, default=80, type=int, help="Numero da porta imbecil")
    args = parse.parse_args()

    if args.PORT:
        PORT = int(args.PORT)
        servidor = Servidor(PORT, 1024)
        servidor.rodar()


if __name__ == "__main__":
    main(sys.argv)
