from debug import *
from wqmt import *
from pywebio.input import *
from pywebio.output import *
from pywebio import *
# import uiautomator2 as u2 # 在家获取activities信息

""" with open('config.yaml', 'r') as f:
  config = yaml.safe_load(f)
remote_path = config['remote_path']
local_path = config['local_path']
devicename = config['devicename']
adb_path = config['adb_path']
 """

adb_connect()
adb_click(201,374)

# 切片
# adb_click(201,374)
# adb_swipe_percent(0.1,0.1,0.2,0.2)