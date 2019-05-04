from os import path
import os
import socket

PROJECT_NAME = 'data-multisatpm'

# Check which machine we're on
HOST = socket.gethostname()
if HOST in ('sullivan-7d', 'sullivan-10d', 'DESKTOP-HOME', 'ThinkPad-PC'):
    data_root = "D:\\"
else:
    data_root = r'\\Sullivan-10d'

DATA_PATH = os.path.join(data_root, 'Data', PROJECT_NAME)
SRC_PATH = path.join(DATA_PATH, 'src')


def data_path(*args):
    return os.path.join(DATA_PATH, *args)


def src_path(*args):
    return path.join(SRC_PATH, *args)
