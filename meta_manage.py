import socket
import datetime

def header():
    return '['+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+']: '

def api_connector(input_str ,port_num):
    sock = socket.socket()
    # Bind the socket to the port
    sock.connect(('127.0.0.1', port_num))
    sock.send(input_str.encode())
    print(header() + sock.recv(1024).decode())
    sock.close()

while True:
    input_str = input(header())
    md_server = input_str.split('$')[0]
    input_str = input_str.split('$')[1]
    if md_server == 's1':
        api_connector(input_str, 5557)
    elif md_server == 's2':
        api_connector(input_str, 5558)
    else:
        print(header() + 'Wrong MD Server Nub=mber')
    