import zmq
from datetime import datetime

#zmq init
context = zmq.Context()
# recieve work
consumer_receiver = context.socket(zmq.PULL)
consumer_receiver.connect("tcp://127.0.0.1:5557")
# send work
consumer_sender = context.socket(zmq.PUSH)
consumer_sender.connect("tcp://127.0.0.1:5558")
#data structure
file_dict = {'root' : ['user']}
file_stat = {}

test_string = '/user/b/c/aa.py'
t2 = '/user/b/bb/aa'

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
    file_stat[s] = {'Access Time': datetime.today(), 'Block Size': '233KB'}

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
    pass

while True:
    rec_str = consumer_receiver.recv_string()
    command = rec_str.split(' ')[0]
    dir_str = rec_str.split(' ')[1]
    if command == 'readdir':
        out_str = readdir(dir_str)
        consumer_sender.send_string(str(out_str))
    elif command == 'stat':
        out_str = stat(dir_str)
        consumer_sender.send_string(str(out_str))
    elif command == 'create_file':
        create_file(dir_str)
        consumer_sender.send_string('Create File Succeed!')
    elif command == 'mkdir':
        mkdir(dir_str)
        consumer_sender.send_string('Make Dir Succeed!')
    else:
        consumer_sender.send_string('Command Not Recognized!')
# mkdir(t2)
# create_file(test_string)
# a = readdir('/user')
# print(a)
# print(file_stat)
# print(stat('/user/b/c/aa.py'))
