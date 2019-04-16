#client_sock.py
import socket

HOST = 'localhost' #coloca o host do servidor
PORT = 57001

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect((HOST,PORT))
arq = open('/home/lucas/aaa.txt', 'r')

for i in arq.readlines():
    s.send(str(i))

arq.close()
s.close()
