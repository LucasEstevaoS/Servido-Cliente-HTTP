#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import socket
import argparse
import sys
import os
from termcolor import colored


# Endereco IP do Servidor
HOST = 'localhost'
# Porta que o Servidor esta
PORT = 5011


class Cliente(object):
    def __init__(self, tamBuffer):
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dest = (HOST, PORT)
        self.tamBuffer = tamBuffer

    def enviar(self, msg):
        dados = {'msg': msg,
                 'lixo': ''}
        dados_bytes = pickle.dumps(dados)

        # Adicionar lixo no final
        if len(dados_bytes) < self.tamBuffer:
            dados['lixo'] = '$'*(self.tamBuffer-len(dados_bytes))
            dados_bytes = pickle.dumps(dados)
        elif len(dados_bytes) > self.tamBuffer:
            # zuou a parada
            return
        self.tcp.send(dados_bytes)

    def receber(self):
        dados_byte = self.tcp.recv(self.tamBuffer)
        dados = pickle.loads(dados_byte)

        if dados['tipoArq'] is None: # Se a requisição for GET
            # receber arquivo
            # salvar arquivo
            print(colored("Download concluído!", 'green'))
            return

        self.imprimirMsg(dados['msg'], dados['tipoArq'])
        return dados['msg'], dados['tipoArq']

    #o tipo dele ta dando bosta
    def imprimirMsg(self, msg, tipoArq):
        for index, valor in enumerate(msg):
            if tipoArq[index] == 'arq':
                print(colored(valor, 'magenta'))
            if tipoArq[index] == 'dir':
                print(colored(valor, 'yellow'))

            print (tipoArq[index])

    def conectar(self):
        self.tcp.connect(self.dest)

def main(argv):
    cliente = Cliente(1024)
    cliente.conectar()

    print ('Para sair use CTRL+X\n')
    msg = input()

    while msg != '\x18':
        cliente.enviar(msg)
        msg = cliente.receber()

        msg = input()

    tcp.close()


if __name__ == "__main__":
    main(sys.argv)
