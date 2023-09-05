import subprocess
import numpy as np
import os
from utils.PPOCR_api import *
import time
import cv2
from pywebio import *
from pywebio.input import *
from pywebio.output import *
import datetime


def test_menu():
    options = ['1', '2']
    selected_options = actions("嗯……", options)
    if "1" in selected_options:
        morning()
    if "2" in selected_options:
        night()
    test_menu()  # 递归调用主菜单函数，以实现循环显示菜单

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
# Connection
def adb_disconnect():  # 断开设备
    subprocess.run([config.adb_path, 'disconnect', config.device_name],
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)

def adb_connect():  # 连接设备，失败则报错
    result = subprocess.run([config.adb_path, 'connect', config.device_name],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    if str(result.stdout).find('cannot') != -1:
        put_text("连接模拟器失败，请见检查congfig.yaml中device_name的配置")

# UI Control
class RandomCoords():
    def __init__(self):
        pass

    def xy(self, x, y, xx=0, yy=0):
        """  
        根据xy数值，在一个15px的区间内生成新的正态分布数值，如果超过15px则重新生成
        """
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

    def time(self, sleep_time):
        """  
        根据sleep_time数值，在一个+30%的区间内生成新的正态分布数值，新数值要求在100%-130%之间
        """
        if sleep_time is None:
            sleep_time = config.sleep_time
        while True:
            mtime = np.round(np.random.choice(np.random.normal(
                loc=sleep_time, scale=sleep_time*0.3, size=15)), decimals=2)

            if sleep_time < mtime < sleep_time*1.3:
                random_float = np.random.random()
                if random_float > 0.8:
                    mtime = mtime+1
                return mtime

class ScreenCtrl():
    def __init__(self):
        pass

    def swipe(self, x, y, xx, yy, sleep_time=None):
        if sleep_time is None:
            sleep_time = config.sleep_time
        if x < 1:
            x, y, xx, yy = self.percent(x, y, xx, yy)
        x, y, xx, yy = RandomCoords().xy(x, y, xx, yy)
        swipe_coords = list(map(str, [x, y, xx, yy]))
        time_gap = RandomCoords().time(sleep_time)
        subprocess.run(["adb", "-s", config.device_name,
                        "shell", "input", "touchscreen", "swipe"] + swipe_coords)
        put_text(f"滑动坐标{swipe_coords}，将休息{time_gap}秒，{get_time()}")
        time.sleep(time_gap)

    def click(self, x, y, sleep_time=None):
        if sleep_time is None:
            sleep_time = config.sleep_time
        if x < 1:
            Codi = self.percent(x, y)
            x = Codi[0]
            y = Codi[1]
        Codi = RandomCoords().xy(x, y)
        x = Codi[0]
        y = Codi[1]
        click_coords = list(map(str, [x, y]))
        time_gap = RandomCoords().time(sleep_time)
        subprocess.run([config.adb_path, "-s", config.device_name, "shell",
                       "input", "tap"] + click_coords)
        put_text(f"点击坐标{click_coords}，将休息{time_gap}秒，{get_time()}")
        time.sleep(time_gap)

    def percent(self, x, y, xx=0, yy=0):
        x = round(config.width * x, 2)
        y = round(config.height * y, 2)
        xx = round(config.width * xx, 2)
        yy = round(config.height * yy, 2)
        return x, y, xx, yy

# CV
class Reconize():
    def __init__(self):
        pass

    def adb_screenshot(self):  # 屏幕截图覆盖screenshop.png, 使用DEVNULL避免输出命令行
        subprocess.run([config.adb_path, '-s', config.device_name, 'shell', 'screencap',
                    config.remote_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run([config.adb_path, '-s', config.device_name, 'pull', config.remote_path,
                    config.local_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        put_image(open(config.local_path, 'rb').read(), width='500px')

    def pic_path(name):
        path = os.path.join(config.current_path, "Target", "wqmt", f"{name}.png")
        return path
    


    def comparebackxy(self, targetpic='', targettxt='', threshold=0.9):  # 找图，返回坐标
        self.adb_screenshot()
        if targetpic:
            # targetpic_path = os.path.join(config.current_path, "Target", "wqmt", f"{targetpic}.png")
            targetpic_path = self.pic_path(targetpic)
            img = cv2.imread(config.local_path, 0)  # 屏幕图片
            template = cv2.imread(targetpic_path, 0)  # 寻找目标
            h, w = template.shape[:2]
            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) # 相关系数匹配方法：cv2.TM_CCOEFF
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            x, y = max_loc[0] + w // 2, max_loc[1] + h // 2
            put_text(f"寻找{targetpic}, 最大匹配度{max_val:.2f}，坐标{x},{y}")
            return (x, y) if max_val > threshold else None
        if targettxt:
            targettxt=str(targettxt)
            res = ocr.run(config.local_path_ocr)
            print(res['data'])
            for data_dict in res['data']:
                if data_dict['text'] == targettxt:
                    box_data = data_dict['box']  # 获取box数据
                    x = (box_data[0][0] + box_data[2][0]) / 2  # 计算X坐标
                    y = (box_data[0][1] + box_data[2][1]) / 2 # 计算Y坐标
                    return (x, y) 
            return None

    def compare_click(self, targetpic='', targettxt='', threshold=0.9, sleepn=0.2, times=1, success="success", fail="fail"):
        center = self.comparebackxy(targetpic, targettxt, threshold)
        if center:
            put_text(success, get_time())
            x, y = center
            for _ in range(times):
                self.adb_click(x, y)
                time.sleep(sleepn)
            return x, y
        else:
            put_text(fail, get_time())
            time.sleep(sleepn)
            return None