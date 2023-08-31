import random
import subprocess
import time
import cv2
import yaml
from pywebio import *
from pywebio.input import *
from pywebio.output import *
import datetime

with open('config.yaml', 'r') as f:
  config = yaml.safe_load(f)
remote_path = config['remote_path']
local_path = config['local_path']
devicename = config['devicename']
adb_path = config['adb_path']

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
        ran = gen_ran()
    """
    ran = random.randint(-5, 5)
    return ran

def get_time():
  """
  des:
      获取当前时间，例如 "2023-08-30 08:03:02"
  使用方法：
      put_text("开始"，get_time()）
  """
  time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  return time_stamp

# ADB
## Connection
def adb_disconnect(): # 断开设备
  subprocess.run([adb_path, 'disconnect', devicename], 
                 stdout=subprocess.DEVNULL, 
                 stderr=subprocess.DEVNULL)

def adb_connect(): # 连接设备，失败则报错
    result = subprocess.run([adb_path,'connect',devicename], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE)
    if str(result.stdout).find('cannot') != -1:
        put_text("连接模拟器失败，请见检查congfig中devicename的配置")

## UI Control
def adb_get_resolution():
    process = subprocess.Popen([adb_path, '-s', devicename, 'shell', 'wm', 'size'], stdout=subprocess.PIPE)
    output = process.stdout.read().decode()
    height, width = map(int, output.split()[-1].split('x'))
    return width, height

def adb_swipe(x, y, xx, yy, ran=0, sleepn=0.2):
    if ran == 1:
        ran = gen_ran()
        swipe_coordinates = [str(x+ran), str(y+ran), str(xx+ran), str(yy+ran)]
    else:
        swipe_coordinates = [str(x), str(y), str(xx), str(yy)]
    subprocess.run(["adb", "-s", devicename, 
                    "shell", "input", "touchscreen", "swipe"] + swipe_coordinates)
    put_text(f"滑动坐标{swipe_coordinates}，{get_time()}")
    time.sleep(sleepn)

def adb_swipe_percent(x_percent, y_percent, xx_percent, yy_percent, ran=0, sleepn=0.2):
    x_pixel = round(adb_get_resolution()[0] * x_percent,2)
    y_pixel = round(adb_get_resolution()[1] * y_percent,2)
    xx_pixel = round(adb_get_resolution()[0] * xx_percent,2)
    yy_pixel = round(adb_get_resolution()[1] * yy_percent,2)
    adb_swipe(x_pixel, y_pixel, xx_pixel, yy_pixel, ran, sleepn)

def adb_click(x, y,ran=0, sleepn=0.2):
    if ran == 1:
        ran = gen_ran()
        click_coordinates = [str(x+ran), str(y+ran)]
    else:
        click_coordinates = [str(x), str(y)]
    subprocess.run([adb_path, "-s", devicename, "shell", "input", "tap"] + click_coordinates)
    put_text(f"点击坐标{click_coordinates}，{get_time()}")
    time.sleep(sleepn)
  
def adb_click_percent(x_percent, y_percent,ran=0, sleepn=0.2):
    x_pixel = round(adb_get_resolution()[0] * x_percent,2)
    y_pixel = round(adb_get_resolution()[1] * y_percent,2)
    adb_click(x_pixel, y_pixel, ran, sleepn)

def adb_screenshot():# 屏幕截图覆盖screenshop.png, 使用DEVNULL避免输出命令行
  subprocess.run([adb_path, '-s', devicename, 'shell', 'screencap', remote_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  subprocess.run([adb_path, '-s', devicename, 'pull', remote_path, local_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
  put_text(f"寻找{targetpic}, 最大匹配度{max_val:.2f}，坐标{x},{y}")
  return (x, y) if max_val > threshold else None

def compare_click(targetpic, threshold=0.9, sleepn=0.2, times=1, success="success",fail="fail"):
    center = comparebackxy(targetpic,threshold)
    if center:
        put_text(success,get_time())
        x,y = center
        for _ in range(times):
            adb_click(x, y)
            time.sleep(sleepn)
        return x, y
    else:
        put_text(fail, get_time())
        time.sleep(sleepn)
        return None