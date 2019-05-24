import pickle
import socket
import argparse
import sys
import os
from termcolor import colored


# Endereco IP do Servidor
HOST = 'localhost'
# Porta que o Servidor esta
PORT = 5008


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
        return msg

    def imprimirMsg(self, msg):
        for m in msg:
            print(m)

    def conectar(self):
        self.tcp.connect(self.dest)

    def ls(self):
        self.imprimirMsg(self.receber())

    def getHttp(self):
        pass

    def getFile(self, arquivo):
        caminho = os.getcwd()
        caminho = caminho + "/downloads/" + arquivo
        print(caminho)
        arq = open(caminho, 'wb')

        while 1:
            dados = self.receber()
            if dados == '\x18':
                arq.close()
                break
            arq.write(dados)

def main(argv):
    cliente = Cliente(1024)
    cliente.conectar()

    print ('Para sair use CTRL+X\n')
    msg = input()

    while msg != '\x18':

        cliente.enviar(msg)

        if(msg[4:8] =="http"):
            cliente.getHttp()


        elif(msg[4:9] =="file "):
            arquivo = msg[9:].split("/")[-1]
            cliente.getFile(arquivo)


        elif(msg[0:3] == "ls "):
            cliente.ls()

        else:
            print("tá errado")


        msg = input()

    tcp.close()


if __name__ == "__main__":
    main(sys.argv)
