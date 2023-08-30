import os
from debug import *
from wqmt import *
from pywebio.input import *
from pywebio.output import *
from pywebio import *


with open('config.yaml', 'r') as f:
  config = yaml.safe_load(f)
remote_path = config['remote_path']
local_path = config['local_path']
devicename = config['devicename']

adb_connect() 

# adb_connect()
def get_time():
  time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  return time_stamp
# adb_screenshot()
adb_click_percent(0.683, 0.53, sleepn=1)
# adb_disconnect()