import random
import subprocess
import time
import cv2
import yaml
from pywebio.input import *
from pywebio.output import *
from pywebio import *

with open('config.yaml', 'r') as f:
  config = yaml.safe_load(f)
remote_path = config['remote_path']
local_path = config['local_path']
devicename = config['devicename']

def test_menu():
  options = ['1', '2']
  selected_options = actions("嗯……", options)
  if "1" in selected_options:
    morning()
  if "2" in selected_options:
    night()
  # 递归调用主菜单函数，以实现循环显示菜单
  test_menu()

def gen_ran():
  ran = random.uniform(-0.005, 0.005)
  return str(ran)

# ADB
## Connection
def adb_disconnect():
  # 执行adb命令来断开设备连接
  subprocess.run(['adb', 'disconnect', devicename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def adb_connect():
  # 执行adb connect命令
  subprocess.run(['adb', 'connect', devicename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

## UI Control

def adb_get_resolution():
  output = subprocess.check_output(['adb', '-s', devicename, 'shell', 'wm', 'size']).decode()
  res = output.split()[-1].split('x')
  width = int(res[0])
  height = int(res[1])
  return width, height

def adb_swap(x, y, xx, yy, ran=0, sleepn=0.2):
  if ran == 1:
    ran = gen_ran()
    subprocess.run(["adb", '-s', devicename,"shell", "input", "touchscreen", "swipe", str(float(x)+float(ran)), str(float(y)+float(ran)), str(float(xx)+float(ran)), str(float(yy)+float(ran))])
  else:
    subprocess.run(["adb", '-s', devicename,"shell", "input", "touchscreen", "swipe", str(x), str(y), str(xx), str(yy)])

  time.sleep(sleepn)

def adb_swap_percent(x_percent, y_percent, xx_percent, yy_percent, ran =0, sleepn=0.2):
  width, height = adb_get_resolution()
  x_pixel = width * x_percent
  y_pixel = height * y_percent
  xx_pixel = width * xx_percent
  yy_pixel = height * yy_percent
  adb_swap(x_pixel, y_pixel, xx_pixel, yy_pixel, ran, sleepn)

def adb_click(x, y,ran=0, sleepn=0.2):
  if ran == 1:
    ran = gen_ran()
    subprocess.run(['adb', '-s', devicename, 'shell', 'input', 'tap', str(float(x)+float(ran)), str(float(y)+float(ran))])
  else:
    subprocess.run(['adb', '-s', devicename, 'shell', 'input', 'tap', str(x), str(y)])
  time.sleep(sleepn)

def adb_click_percent(x_percent, y_percent,ran=0, sleepn=0.2):
  width, height = adb_get_resolution()
  x_pixel = width * x_percent
  y_pixel = height * y_percent
  adb_click(str(x_pixel), str(y_pixel),ran, sleepn)

def adb_screenshot():# 屏幕截图覆盖screenshop.png
  # 执行adb命令获取屏幕截图，将输出重定向到空设备
  subprocess.run(['adb', '-s', devicename, 'shell', 'screencap', remote_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  # 将截图从设备复制到本地，将输出重定向到空设备
  subprocess.run(['adb', '-s', devicename, 'pull', remote_path, local_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  # 输出图片
  put_image(open(local_path, 'rb').read(),width='500px')

#CV
def comparebackxy(targetpic,threshold=0.9): #找图，返回坐标
  adb_screenshot()
  img = cv2.imread(local_path, 0) # 屏幕图片
  template = cv2.imread(targetpic, 0) # 寻找目标
  h, w = template.shape[:2]  # rows->h, cols->w
  # 相关系数匹配方法：cv2.TM_CCOEFF
  res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
  _, max_val, _, max_loc = cv2.minMaxLoc(res)
  if max_val > threshold:
    x = max_loc[0] + w // 2
    y = max_loc[1] + h // 2
    return x, y
  else:
    return None

#pywebio



    
""" 真机使用，无需调用
def adb_tohome():
  subprocess.run(["adb", "shell", "svc", "power", "stayon", "true"])  # 防止息屏&点亮屏幕
  center = comparebackxy('./Target/Phone/lock.png',0.85)
  if center is None:
    center = comparebackxy('./Target/Phone/home.png',0.9)
    if center is None:
      subprocess.run(["adb", "shell", "input", "keyevent", "3"])
      time.sleep(1) 
      center = comparebackxy('./Target/Phone/home.png',0.9)
      if center is None:
        import sys
        sys.exit()
  else:
    x,y = center
    xx = x
    y = y - 300
    yy = y - 1000
    adb_swap(x, y, xx, yy, 2)
    subprocess.run(["adb", "shell", "input", "keyevent", "3"])# 回到Home
  subprocess.run(["adb", "shell", "settings", "put", "system", "screen_brightness", "0"])  # 调整亮度

def adb_end():
  subprocess.run(["adb", "shell", "svc", "power", "stayon", "false"])  # 恢复防止息屏
  subprocess.run(["adb", "shell", "settings", "put", "system", "screen_brightness", "50"])  # 恢复调整亮度 """
