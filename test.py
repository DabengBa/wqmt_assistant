import os
from utils import *
from pywebio.input import *
from pywebio.output import *
from pywebio import *

adb_connect() 

with open('config.yaml', 'r') as f:
  config = yaml.safe_load(f)
remote_path = config['remote_path']
local_path = config['local_path']
devicename = config['devicename']

def test_comparebackxy(targetpic,threshold=0.9): #找图，返回坐标, 显示
  adb_screenshot()
  img = cv2.imread(local_path, 0) # 屏幕图片
  template = cv2.imread(targetpic, 0) # 寻找目标
  h, w = template.shape[:2]  # rows->h, cols->w
  # 相关系数匹配方法：cv2.TM_CCOEFF
  res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
  _, max_val, _, max_loc = cv2.minMaxLoc(res)
  x = max_loc[0] + w // 2
  y = max_loc[1] + h // 2
  if max_val > threshold:
    put_text(f"找到了，最大匹配度{max_val:.3f}，坐标{x},{y}")
    put_text("找到了")
    return x, y
  else:
    put_text(f"没找到，最大匹配度{max_val:.3f}，坐标{x},{y}")
    return None
# adb_connect()

# comparebackxy('./Target/wqmt/fuben1.png')
test_comparebackxy('./Target/wqmt/fubensaodang.png',threshold=0.9)
compare_click('./Target/wqmt/fubensaodang.png',success="成功",fail="失败")
# adb_disconnect()