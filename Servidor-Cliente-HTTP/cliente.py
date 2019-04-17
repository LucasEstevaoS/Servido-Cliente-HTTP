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
PORT = 5006


class Cliente(object):
    def __init__(self, tamBuffer):
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dest = (HOST, PORT)
        self.tamBuffer = tamBuffer

    def enviar(self, msg):
        dados_bytes = pickle.dumps(msg)
        self.tcp.send(dados_bytes)

    def receber(self):
        dados_byte = self.tcp.recv(self.tamBuffer)
        msg = pickle.loads(dados_byte)
        self.imprimirMsg(msg)
        return msg

    def imprimirMsg(self, msg):
        for m in msg:
            print(m)

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
