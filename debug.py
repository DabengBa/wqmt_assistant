import random
import subprocess
import time
import cv2
import yaml
import os
from pywebio import *
from pywebio.input import *
from pywebio.output import *

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
  test_menu() # 递归调用主菜单函数，以实现循环显示菜单

def gen_ran():
    """
    des:
        随机生成一个浮点数 
    使用方法：
        ran = genran()
    """
    ran = random.uniform(-0.005, 0.005)
    return float(ran)

# ADB
## Connection
def adb_disconnect(): # 断开设备
  subprocess.run(['adb', 'disconnect', devicename], 
                 stdout=subprocess.DEVNULL, 
                 stderr=subprocess.DEVNULL)

def adb_connect(): # 连接设备，失败则报错
  try:
    subprocess.run(['adb', 'connect', devicename], 
          stdout=subprocess.DEVNULL, 
          stderr=subprocess.DEVNULL)
  except subprocess.CalledProcessError:
    print(f"连接设备{devicename}失败!, 请检查config中的device配置")

## UI Control
def adb_get_resolution():
    process = subprocess.Popen(['adb', '-s', devicename, 'shell', 'wm', 'size'], stdout=subprocess.PIPE)
    output = process.stdout.read().decode()
    width, height = map(int, output.split()[-1].split('x'))
    return width, height

def adb_swap(x, y, xx, yy, ran=0, sleepn=0.2):
    if ran == 1:
        ran = gen_ran()
        swipe_coordinates = [str(float(x)+float(ran)), str(float(y)+float(ran)), str(float(xx)+float(ran)), str(float(yy)+float(ran))]
        print(f"swap{str(float(x)+float(ran)), str(float(y)+float(ran)), str(float(xx)+float(ran)), str(float(yy)+float(ran))}")
    else:
        swipe_coordinates = [str(x), str(y), str(xx), str(yy)]
        print(f"swap{str(x), str(y), str(xx), str(yy):.3f}")
    subprocess.run(["adb", "-s", devicename, "shell", "input", "touchscreen", "swipe"] + swipe_coordinates)
    time.sleep(sleepn)

def adb_swap_percent(x_percent, y_percent, xx_percent, yy_percent, ran=0, sleepn=0.2):
    x_pixel = adb_get_resolution()[0] * x_percent
    y_pixel = adb_get_resolution()[1] * y_percent
    xx_pixel = adb_get_resolution()[0] * xx_percent
    yy_pixel = adb_get_resolution()[1] * yy_percent
    adb_swap(x_pixel, y_pixel, xx_pixel, yy_pixel, ran, sleepn)

def adb_click(x, y,ran=0, sleepn=0.2):
    if ran == 1:
        ran = gen_ran()
        click_coordinates = [str(float(x)+float(ran)), str(float(y)+float(ran))]
        print(f"click{str(float(x)+float(ran)), str(float(y)+float(ran))}")
    else:
        click_coordinates = [str(x), str(y)]
    subprocess.run(["adb", "-s", devicename, "shell", "input", "tap"] + click_coordinates)
    time.sleep(sleepn)
  
def adb_click_percent(x_percent, y_percent,ran=0, sleepn=0.2):
    x_pixel = adb_get_resolution()[0] * x_percent
    y_pixel = adb_get_resolution()[1] * y_percent
    adb_click(str(x_pixel), str(y_pixel),ran, sleepn) # 传入sleepn，本函数不需要再设置time.sleep

def adb_screenshot():# 屏幕截图覆盖screenshop.png, 使用DEVNULL避免输出命令行
  subprocess.run(['adb', '-s', devicename, 'shell', 'screencap', remote_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  subprocess.run(['adb', '-s', devicename, 'pull', remote_path, local_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  put_image(open(local_path, 'rb').read(),width='500px')

#CV
def comparebackxy(targetpic,threshold=0.9): #找图，返回坐标
  adb_screenshot()
  img = cv2.imread(local_path, 0) # 屏幕图片
  template = cv2.imread(targetpic, 0) # 寻找目标
  h, w = template.shape[:2]
  res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)# 相关系数匹配方法：cv2.TM_CCOEFF
  _, max_val, _, max_loc = cv2.minMaxLoc(res)
  x, y = max_loc[0] + w // 2, max_loc[1] + h // 2
  print(f"寻找{targetpic}, 最大匹配度{max_val:.3f}，坐标{x},{y}")
  return (x, y) if max_val > threshold else None

def compare_click(targetpic, threshold=0.9, sleepn=0.2, times=1, success="success",fail="fail"):
    center = comparebackxy(targetpic,threshold)
    if center:
        put_text(success)
        x,y = center
        for _ in range(times):
            adb_click(x, y, sleepn)
            time.sleep(sleepn)
        return x, y
    else:
        put_text(fail)
        time.sleep(sleepn)
        return None
    
adb_connect()
compare_click('./Target/wqmt/fuben1.png',threshold=0.9)