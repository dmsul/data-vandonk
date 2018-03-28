from os import path
import os
import socket

# Check which machine we're on
HOST = socket.gethostname()
if HOST == 'sullivan-7d':
    data_root = "D:\\"
elif HOST == 'DESKTOP-HOME':
    data_root = "D:\\"
elif HOST == 'nepf-7d':
    data_root = "M:\\EPA_AirPollution\\"
else:
    data_root = r'\\Sullivan-7d\d'

DATA_PATH = os.path.join(data_root, 'Data', 'multisatpm')
SRC_PATH = path.join(DATA_PATH, 'src')


def data_path(*args):
    return os.path.join(DATA_PATH, *args)


def src_path(*args):
    return path.join(SRC_PATH, *args)
