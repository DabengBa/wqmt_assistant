import os
from utils import *
from pywebio.input import *
from pywebio.output import *
from pywebio import *

with open('config.yaml', 'r') as f:
  config = yaml.safe_load(f)
remote_path = config['remote_path']
local_path = config['local_path']
devicename = config['devicename']

# adb_connect()

# comparebackxy('./Target/wqmt/fuben1.png')
comparebackxy_test('./Target/wqmt/fubensaodang.png',threshold=0.9)
# adb_disconnect()