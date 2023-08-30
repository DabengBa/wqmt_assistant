import os
from debug import *
from wqmt import *
from pywebio.input import *
from pywebio.output import *
from pywebio import *
import subprocess
import uiautomator2 as u2

with open('config.yaml', 'r') as f:
  config = yaml.safe_load(f)
remote_path = config['remote_path']
local_path = config['local_path']
devicename = config['devicename']

d = u2.connect(devicename)
# adb_connect()
width, height = d.window_size()
print(width, height)
compare_click('./Target/wqmt/cancel.png',success="@@@@@@@已经取消月卡购买界面，请之后注意补充@@@@",fail="")
# adb_disconnect()5