import subprocess
import numpy as np

import time
import cv2
import yaml
from pywebio import *
from pywebio.input import *
from pywebio.output import *
import datetime

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


def test_menu():
    options = ['1', '2']
    selected_options = actions("嗯……", options)
    if "1" in selected_options:
        morning()
    if "2" in selected_options:
        night()
    test_menu()  # 递归调用主菜单函数，以实现循环显示菜单

# ADB
# Connection


def adb_disconnect():  # 断开设备
    subprocess.run([adb_path, 'disconnect', devicename],
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def adb_connect():  # 连接设备，失败则报错
    result = subprocess.run([adb_path, 'connect', devicename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    if str(result.stdout).find('cannot') != -1:
        put_text("连接模拟器失败，请见检查congfig中devicename的配置")

# UI Control


class RandomCoords():
    def __init__(self):
        pass

    def xy(self, x, y, xx=0, yy=0):
        while True:
            mx = np.round(np.random.choice(np.random.normal(
                loc=x, scale=7, size=15)), decimals=2)
            my = np.round(np.random.choice(np.random.normal(
                loc=y, scale=7, size=15)), decimals=2)
            mxx = np.round(np.random.choice(np.random.normal(
                loc=xx, scale=7, size=15)), decimals=2)
            myy = np.round(np.random.choice(np.random.normal(
                loc=yy, scale=7, size=15)), decimals=2)
            if x-15 < mx < x+15 and y-15 < my < y+15 and xx-15 < mxx < xx+15 and yy-15 < myy < yy+15:
                return mx, my, mxx, myy

    def time(self, SleepTime):
        while True:
            mtime = np.round(np.random.choice(np.random.normal(
                loc=SleepTime, scale=SleepTime*0.3, size=15)), decimals=2)

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
        swipe_coords = list(map(str, [x, y, xx, yy]))
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
        click_coords = list(map(str, [x, y]))
        time_gap = RandomCoords().time(SleepTime)
        subprocess.run([adb_path, "-s", devicename, "shell",
                       "input", "tap"] + click_coords)
        put_text(f"点击坐标{click_coords}，将休息{time_gap}秒，{get_time()}")
        time.sleep(time_gap)

    def percent(self, x, y, xx=0, yy=0):
        x = round(self.adb_get_resolution()[0] * x, 2)
        y = round(self.adb_get_resolution()[1] * y, 2)
        xx = round(self.adb_get_resolution()[0] * xx, 2)
        yy = round(self.adb_get_resolution()[1] * yy, 2)
        return x, y, xx, yy


def adb_screenshot():  # 屏幕截图覆盖screenshop.png, 使用DEVNULL避免输出命令行
    subprocess.run([adb_path, '-s', devicename, 'shell', 'screencap',
                   remote_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run([adb_path, '-s', devicename, 'pull', remote_path,
                   local_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    put_image(open(local_path, 'rb').read(), width='500px')

# CV


def comparebackxy(targetpic, threshold=0.9):  # 找图，返回坐标
    adb_screenshot()
    img = cv2.imread(local_path, 0)  # 屏幕图片
    template = cv2.imread(targetpic, 0)  # 寻找目标
    h, w = template.shape[:2]
    # 相关系数匹配方法：cv2.TM_CCOEFF
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    x, y = max_loc[0] + w // 2, max_loc[1] + h // 2
    put_text(f"寻找{targetpic}, 最大匹配度{max_val:.2f}，坐标{x},{y}")
    return (x, y) if max_val > threshold else None


def compare_click(targetpic, threshold=0.9, sleepn=0.2, times=1, success="success", fail="fail"):
    center = comparebackxy(targetpic, threshold)
    if center:
        put_text(success, get_time())
        x, y = center
        for _ in range(times):
            adb_click(x, y)
            time.sleep(sleepn)
        return x, y
    else:
        put_text(fail, get_time())
        time.sleep(sleepn)
        return None
