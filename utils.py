import subprocess
import time
import cv2
import yaml
import os
import numpy as np
<<<<<<< Updated upstream
import uiautomator2 as u2

=======
>>>>>>> Stashed changes

with open('config.yaml', 'r') as f:
  config = yaml.safe_load(f)
remote_path = config['remote_path']
local_path = config['local_path']
devicename = config['devicename']

def main_menu():
  print("1. 运行 smzdm.py")
  print("2. 选项2")
  print("3. 选项3")
  print("4. 退出")
  choice = input("请选择一个选项：")
  if choice == "1":
    start_smzdm()
  elif choice == "2":
    # 在这里编写选项2的代码
    print("执行选项2")
  elif choice == "3":
    # 在这里编写选项3的代码
    print("执行选项3")
  elif choice == "4":
    print("退出程序")
    return
  else:
    print("无效的选项")
  # 递归调用主菜单函数，以实现循环显示菜单
  main_menu()

def start_smzdm():
  # 运行 smzdm.py 文件
  subprocess.run(["python", "smzdm.py"])

# ADB
def adb_disconnect():
  # 执行adb命令来断开设备连接
  subprocess.run(['adb', 'disconnect', ''])
def adb_connect(ipport):
  # 执行adb connect命令
  subprocess.run(['adb', 'connect', ipport])
<<<<<<< Updated upstream

def adb_screenshot(remote_path, local_path, devicename):# 屏幕截图覆盖screenshop.png
  subprocess.run(['adb', '-s', devicename, 'shell', 'screencap', remote_path])
  subprocess.run(['adb', '-s', devicename, 'pull', remote_path, local_path])

### 屏幕控制
def adb_swap(x, y, xx, yy, sleepn=0.2):
  subprocess.run(["adb", '-s', devicename,"shell", "input", "touchscreen", "swipe", str(x), str(y), str(xx), str(yy)])
=======
def adb_screenshot(remote_path, local_path):# 屏幕截图覆盖screenshop.png
  subprocess.run(['adb', 'shell', 'screencap', remote_path])
  subprocess.run(['adb', 'pull', remote_path, local_path])
### 屏幕控制
def adb_swap(x, y, xx, yy, sleepn=0):
  subprocess.run(["adb", "shell", "input", "touchscreen", "swipe", str(x), str(y), str(xx), str(yy)])
>>>>>>> Stashed changes
  time.sleep(sleepn)
def adb_swap_percent(x_percent, y_percent, xx_percent, yy_percent, sleepn=0.2):
  width, height = adb_get_resolution(devicename)
  x_pixel = width * x_percent
  y_pixel = height * y_percent
  xx_pixel = width * xx_percent
  yy_pixel = height * yy_percent
  subprocess.run(["adb", '-s', devicename,"shell", "input", "touchscreen", "swipe", str(x_pixel), str(y_pixel), str(xx_pixel), str(yy_pixel)])
  time.sleep(sleepn)

def adb_tohome():
  subprocess.run(["adb", "shell", "svc", "power", "stayon", "true"])  # 防止息屏&点亮屏幕
  center = comparebackxy('./Target/Phone/lock.png',0.85)
  if center is None:
    center = comparebackxy('./Target/Phone/home.png',0.9)
    if center is None:
      print('也不是home，尝试回到home')
      subprocess.run(["adb", "shell", "input", "keyevent", "3"])
      time.sleep(1) 
      center = comparebackxy('./Target/Phone/home.png',0.9)
      if center is None:
        print('回到home失败，停止程序')
        import sys
        sys.exit()
    else:
      print('已经是home')
  else:
    print('需要解锁')
    x,y = center
    xx = x
    y = y - 300
    yy = y - 1000
    print(x,y,xx,yy)
    adb_swap(x, y, xx, yy, 2)
    subprocess.run(["adb", "shell", "input", "keyevent", "3"])# 回到Home
  subprocess.run(["adb", "shell", "settings", "put", "system", "screen_brightness", "0"])  # 调整亮度
def adb_end():
  subprocess.run(["adb", "shell", "svc", "power", "stayon", "false"])  # 恢复防止息屏
  subprocess.run(["adb", "shell", "settings", "put", "system", "screen_brightness", "50"])  # 恢复调整亮度
  print('Complete')
<<<<<<< Updated upstream
def adb_click(x, y,sleepn=0.2):
  subprocess.run(['adb', '-s', devicename, 'shell', 'input', 'tap', str(x), str(y)])
  time.sleep(sleepn)
def adb_get_resolution(devicename):
  output = subprocess.check_output(['adb', '-s', devicename, 'shell', 'wm', 'size']).decode()
  res = output.split()[-1].split('x')
  width = int(res[0])
  height = int(res[1])
  return width, height
def adb_click_percent(x_percent, y_percent,sleepn=0.2):
  width, height = adb_get_resolution(devicename)
  x_pixel = width * x_percent
  y_pixel = height * y_percent
  adb_click(str(x_pixel), str(y_pixel),sleepn)
=======
def adb_click(x,y,sleepn=0):
  subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])
  time.sleep(sleepn)
>>>>>>> Stashed changes

#CV
def comparebackxy(targetpic,threshold=0.9):
  global center  # 声明center为全局变量
  while True:
    #截图
    adb_screenshot(remote_path, local_path, devicename)
    img = cv2.imread(local_path, 0)
    template = cv2.imread(targetpic, 0)
    h, w = template.shape[:2]  # rows->h, cols->w
    # 相关系数匹配方法：cv2.TM_CCOEFF
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    left_top = max_loc  # 左上角
    """ right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
        cv2.rectangle(img, left_top, right_bottom, 255, 2)  # 画出矩形位置
        cv2.imwrite('./log/result.png', img) # 保存本次的最大值 """
    print(max_val)
    if max_val > threshold:
      x = max_loc[0] + w // 2
      y = max_loc[1] + h // 2
      print('找到目标区域,坐标为:', x, y)
      center = x, y
      return center
    else:
      print('未找到，最大相似度为'+str(max_val))
    """       center = None  # 在else的情况下，返回center为空值
          return center """








