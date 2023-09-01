# from debug import *
# from wqmt import *
from pywebio.input import *
from pywebio.output import *
from pywebio import *
import numpy as np
import yaml
import subprocess
import datetime
import time

# import uiautomator2 as u2 # 在家获取activities信息

try:
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("Error: config.yaml file not found.")

remote_path = config.get('remote_path', '')
local_path = config.get('local_path', '')
devicename = config.get('devicename', '')
adb_path = config.get('adb_path', '')
SleepTime = config.get('SleepTime', '')

class RandomCoords():
  def __init__(self):
    pass

  def xy(self, x, y, xx=0, yy=0):
    while True:
      mx = np.round(np.random.choice(np.random.normal(loc=x, scale=7, size=15)),decimals=2)
      my = np.round(np.random.choice(np.random.normal(loc=y, scale=7, size=15)),decimals=2)
      mxx = np.round(np.random.choice(np.random.normal(loc=xx, scale=7, size=15)),decimals=2)
      myy = np.round(np.random.choice(np.random.normal(loc=yy, scale=7, size=15)),decimals=2)
      if x-15 < mx < x+15 and y-15 < my < y+15 and xx-15 < mxx < xx+15 and yy-15 < myy < yy+15:
        return mx, my, mxx, myy
  
  def time(self, SleepTime):
    while True:
      mtime = np.round(np.random.choice(np.random.normal(loc=SleepTime, scale=SleepTime*0.3, size=15)),decimals=2)

      if SleepTime < mtime < SleepTime*1.3:
        random_float = np.random.random()
        if random_float > 0.8:
           mtime = mtime+1
        return mtime

def get_time():
  """
  des:
      获取当前时间，例如 "2023-08-30 08:03:02"
  使用方法：
      put_text("开始"，get_time()）
  """
  time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  return time_stamp

class ScreenCtrl():
    def __init__(self):
        pass
        
    def adb_get_resolution(self):
        process = subprocess.Popen([adb_path, '-s', devicename, 'shell', 'wm', 'size'], 
                                   stdout=subprocess.PIPE)
        output = process.stdout.read().decode()
        height, width = map(int, output.split()[-1].split('x'))
        return width, height

    def swipe(self, x, y, xx, yy, SleepTime=SleepTime):
        if x < 1:
            x, y, xx, yy = self.percent(x, y, xx, yy)
        x, y, xx, yy = RandomCoords().xy(x, y, xx, yy)
        swipe_coords = list(map(str,[x, y, xx, yy]))
        time_gap = RandomCoords().time(SleepTime)
        subprocess.run(["adb", "-s", devicename, 
                        "shell", "input", "touchscreen", "swipe"] + swipe_coords)
        put_text(f"滑动坐标{swipe_coords}，将休息{time_gap}秒，{get_time()}")
        time.sleep(time_gap)

    def click(self, x, y, SleepTime=SleepTime):
        if x < 1:
            Codi = self.percent(x, y)
            x = Codi[0]
            y = Codi[1]
        Codi = RandomCoords().xy(x, y)
        x = Codi[0]
        y = Codi[1]
        click_coords = list(map(str,[x, y]))
        time_gap = RandomCoords().time(SleepTime)
        subprocess.run([adb_path, "-s", devicename, "shell", "input", "tap"] + click_coords)
        put_text(f"点击坐标{click_coords}，将休息{time_gap}秒，{get_time()}")
        time.sleep(time_gap)

    def percent(self, x, y, xx=0, yy=0):
        x = round(self.adb_get_resolution()[0] * x,2)
        y = round(self.adb_get_resolution()[1] * y,2)
        xx = round(self.adb_get_resolution()[0] * xx,2)
        yy = round(self.adb_get_resolution()[1] * yy,2)
        return x, y, xx, yy

subprocess.run([adb_path,'connect',devicename], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE)

ScreenCtrl().click(0.2,0.5,SleepTime=5)
