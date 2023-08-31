import os
from debug import *
from wqmt import *
from pywebio.input import *
from pywebio.output import *
from pywebio import *
import uiautomator2 as u2 # 在家获取activities信息

with open('config.yaml', 'r') as f:
  config = yaml.safe_load(f)
remote_path = config['remote_path']
local_path = config['local_path']
devicename = config['devicename']

adb_connect() 

d = u2.connect(devicename)
d.app_info("com.zy.wqmt.cn")
# subprocess.run(["adb", "-s", devicename, "shell", "input", "tap", str(360), str(1150)])
# adb_disconnect()