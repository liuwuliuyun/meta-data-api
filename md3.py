import datetime
import socket

sock = socket.socket()
# Bind the socket to the port
server_address = ('localhost', 5559)
sock.bind(server_address)
sock.listen(5)
#data structure
file_dict = {'root' : ['user']}
file_stat = {}
header = '[MD3'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+']: '

# TEST CODE COMMENT WHEN DEPLOY
# test_string = ['/user/s1/LiuYun', '/user/s1/Github', '/user/s1/LiuYun/myprofile.py', '/user/s1/system.ini']


def mkdir(s):
    dir_list = s.split('/')
    start_dir = 'root'
    for dir_item in dir_list[1:]:
        if start_dir in file_dict:
            if dir_item not in file_dict[start_dir]:
                file_dict[start_dir].append(dir_item)
        else:
            file_dict[start_dir] = [dir_item]
        start_dir = start_dir+'/'+dir_item
    return file_dict


def create_file(s):
    mkdir(s)
    file_stat[s] = {'Access Time': header, 'Block Size': '233KB'}

def readdir(s):
    s = 'root' + s
    result_list = _readdir(s)
    result_list = list(set(result_list))
    result_list.sort()
    return result_list

def _readdir(s):
    result_list = []
    if s in file_dict:
        result_list += [s+'/'+i for i in file_dict[s]]
        for item in result_list:
            result_list += _readdir(item)
    return result_list

def stat(s):
    if s in file_stat:
        return file_stat[s]
    else:
        return None

def rmfile(s):
    global file_dict, file_stat
    name = s.split('/')[-1]
    file_stat.pop(s)
    for k, v in file_dict.items():
        if name in v:
            v.remove(name)
            file_dict[k] = v


while True:
    con, clt_addr = sock.accept()
    rec_str = con.recv(1024).decode()
    try:
        command = rec_str.split(' ')[0]
        try:
            dir_str = rec_str.split(' ')[1]
        except:
            dir_str = ''
        if command == 'ls':
            out_str = readdir(dir_str)
            con.send(str(out_str).encode())
        elif command == 'stat':
            out_str = stat(dir_str)
            con.send(str(out_str).encode())
        elif command == 'touch':
            create_file(dir_str)
            con.send('File creation succeed ...'.encode())
        elif command == 'mkdir':
            mkdir(dir_str)
            con.send('Directory insertion succeed ...'.encode())
        elif command == 'rm':
            rmfile(dir_str)
            con.send(('File ' + dir_str + ' removed ...').encode())
        else:
            con.send('Can not parse this command, plz check ...'.encode())
    except:
        con.send('Error occured when processing command, check before proceed ...'.encode())

con.close()

#TEST CODE COMMENT WHEN DEPLOY
# mkdir(test_string[0])
# mkdir(test_string[1])
# create_file(test_string[2])
# create_file(test_string[3])
# print(readdir('/user'))
# print(file_dict)
# rmfile(test_string[3])
# print(file_dict)
# print(readdir('/user'))
