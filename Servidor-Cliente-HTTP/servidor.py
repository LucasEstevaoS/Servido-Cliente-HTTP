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

        #download
        if msg[:4] == "get ":
            print("get")
            self.dados.tipoArq = None


            #self.dados.msg = open(msg[4:])
            #print (cliente, msg)
            #dirs = os.listdir(msg)
            self.enviar(msg[4:], None)

        #listar
        elif msg[:3] == "ls ":
            print("ls")
            dirs = os.listdir(msg[3:])
            arquivos = self.verificarTipos(dirs)
            self.enviar(dirs, arquivos)

        else :
            print(" Comando Invalido\n ")

    #verifica se é um arquivo ou um diretorio
    def verificarTipos(self, dirs):
        arquivos = []
        for d in dirs:
            if os.path.isdir():
                arquivos.append('dir')
            if os.path.isfile():
                arquivos.append('arq')


        return arquivos

    def enviar(self, msg, arquivos=None): # None: requisicao GET
        dados = {'msg': msg,
                 'tipoArq':arquivos,
                 'lixo': '',
                 'baixando': True}
        dados_byte = pickle.dumps(dados)

        # Adicionar lixo no final
        if len(dados_byte) < self.tamBuffer:
            dados['lixo'] = '$'*(self.tamBuffer-len(dados_byte))
        elif len(dados_byte) > self.tamBuffer:
            # zuou a parada
            return

        dados_byte = pickle.dumps(dados)

        print(dados_byte)
        self.conexao.send(dados_byte)

    #recebe a mensagem em byte e converte pra caracter
    def receber(self):
        dados_byte = self.conexao.recv(self.tamBuffer)
        dados = pickle.loads(dados_byte)
        return dados['msg']



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
