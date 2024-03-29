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
    try:
        md_server = input_str.split('$')[0]
        input_str = input_str.split('$')[1]
        if md_server == 's1':
            api_connector(input_str, 5557)
        elif md_server == 's2':
            api_connector(input_str, 5558)
        elif md_server == 's3':
            api_connector(input_str, 5559)
        elif md_server == 's':
            print(header()+'For Metadata Server 1:')
            api_connector('ls ', 5557)
            print(header()+'For Metadata Server 2:')
            api_connector('ls ', 5558)
            print(header()+'For Metadata Server 3:')
            api_connector('ls ', 5559)
        else:
            print(header() + 'Error: Incorrect metadata server number')
    except:
        print(header() + 'Error: Incorrect metadata server command')
    