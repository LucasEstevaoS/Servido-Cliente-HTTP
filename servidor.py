#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import pickle
import argparse
import sys
import os

# Endereco IP do Servidor
HOST = 'http://www.sandrinha.com.br'
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
            print("Permissao negada! (porta ja esta em uso)")
            exit(0)
        self.tcp.listen(1)

        while True:
            con, cliente = self.tcp.accept()
            self.conexao = con
            print ('Conetado por', cliente)
            while True:
                msg = self.receber()
                if not msg: break
                self.verificaRequisicao(msg)

            print ('Finalizando conexao do cliente', cliente)
            con.close()
            exit(0)

    def enviarArquivo(self, arq):
        for i in arq.readlines():
            self.enviar(i)

    def verificaRequisicao(self, msg):

        #descobrir que é get
        if msg[:4] == "get ":
            print(msg[4:])

            #descobrir que é http
            if(msg[4:8] =="http"):
                print ("http")

            #descobrir que é file
            if(msg[4:9] =="file "):
                caminho = msg[9:] #caminho do arquivo + nome do arquivo
                arquivo = caminho.split("/")[-1] #nome do arquivo
                try:
                    arq = open(caminho, 'rb')
                except EOFError:
                    print("Arquivo inexistente!")
                    return
                self.enviarArquivo(arq)
                arq.close()
                self.enviar('\x18')

        #listar pastas
        elif msg[:3] == "ls ":
            print("ls")
            dirs = os.listdir(msg[3:])
            print (dirs)
            self.enviar(dirs)
        else :
            print(" Comando Invalido\n ")

    #transforma string em byte e envia
    def enviar(self, msg):
        dados_byte = pickle.dumps(msg)
        self.conexao.send(dados_byte)

    #recebe a mensagem em byte e converte pra caracter
    def receber(self):
        dados_byte = self.conexao.recv(self.tamBuffer)
        msg = pickle.loads(dados_byte)
        return msg


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
