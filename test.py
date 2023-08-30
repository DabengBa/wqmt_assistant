import os
from debug import *
from wqmt import *
from pywebio.input import *
from pywebio.output import *
from pywebio import *

adb_connect() 

with open('config.yaml', 'r') as f:
  config = yaml.safe_load(f)
remote_path = config['remote_path']
local_path = config['local_path']
devicename = config['devicename']

# adb_connect()
def get_time():
  time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  return time_stamp
# comparebackxy('./Target/wqmt/fuben1.png')
compare_click('./Target/wqmt/caigouban1.png', sleepn=4)
compare_click('./Target/wqmt/caigouban1.png', sleepn=4)
# adb_disconnect()