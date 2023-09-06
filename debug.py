from datetime import datetime
from time import sleep
from subprocess import run as adb_run, DEVNULL, PIPE
from numpy import round, random
import cv2
from PPOCR_api import GetOcrApi
from pywebio.output import put_text, put_image
from os import path
import config

def get_time():
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return time_stamp

# ADB
# Connection
def adb_disconnect():  # 断开设备
    adb_run([config.adb_path, 'disconnect', config.device_name],
                   stdout=DEVNULL,
                   stderr=DEVNULL)

def adb_connect():  # 连接设备，失败则报错
    result = adb_run([config.adb_path, 'connect', config.device_name],
                            stdout=PIPE,
                            stderr=PIPE)
    if str(result.stdout).find('cannot') != -1:
        put_text("连接模拟器失败，请见检查congfig.yaml中device_name的配置")

# UI Control
def gen_ran_xy(x, y, xx=0, yy=0):
    # 根据xy数值，在一个15px的区间内生成新的正态分布数值，如果超过15px则重新生成
    while True:
        mx = round(random.choice(random.normal(loc=x, scale=7, size=15)), decimals=2)
        my = round(random.choice(random.normal(loc=y, scale=7, size=15)), decimals=2)
        mxx = round(random.choice(random.normal(loc=xx, scale=7, size=15)), decimals=2)
        myy = round(random.choice(random.normal(loc=yy, scale=7, size=15)), decimals=2)
        
        if all([
        x - 15 < mx < x + 15,
        y - 15 < my < y + 15,
        xx - 15 < mxx < xx + 15,
        yy - 15 < myy < yy + 15,
        mx > 0,
        my > 0,
        mxx > 0,
        myy > 0
        ]):
            return (mx, my, mxx, myy)

def gen_ran_time(time=None):
    if time is None:
        time = config.sleep_time
    while True:
        mtime = round(random.choice(random.normal(
            loc=time, scale=time*0.3, size=15)), decimals=2)

        if time < mtime < time*1.3:
            random_float = random.random()
            if random_float > 0.8: # 有20%几率额外增加1s延迟
                mtime = mtime+1
            return mtime

def swipe_screen( x, y, xx, yy, sleep_time=None):

    if sleep_time is None:
        sleep_time = config.sleep_time

    if x < 1:
        x, y, xx, yy = trans_percent_to_xy(x, y, xx, yy)

    x, y, xx, yy = gen_ran_xy(x, y, xx, yy)
    swipe_coords = [str(coord) for coord in [x, y, xx, yy]]
    time_gap = gen_ran_time(sleep_time)

    adb_run(["adb", "-s", config.device_name,
                    "shell", "input", "touchscreen", "swipe"] + swipe_coords)
    # put_text(f"滑动坐标{swipe_coords}，将休息{time_gap}秒，{get_time()}")
    sleep(time_gap)

def click_screen( x, y, sleep_time=None):
    """
    Clicks on the screen at the specified coordinates.

    Args:
        x (int): The x-coordinate of the screen position to click.
        y (int): The y-coordinate of the screen position to click.
        sleep_time (float, optional): The amount of time to sleep after clicking. 
            If not provided, the default sleep time from the config module will be used.

    Returns:
        None
    """

    if sleep_time is None:
        sleep_time = config.sleep_time

    if x < 1:
        x, y = trans_percent_to_xy(x, y)

    x, y = gen_ran_xy(x, y)
    click_coords = [str(coord) for coord in [x, y]]
    time_gap = gen_ran_time(sleep_time)

    adb_run([config.adb_path, "-s", config.device_name, "shell",
                    "input", "tap"] + click_coords)
    # put_text(f"点击坐标{click_coords}，将休息{time_gap}秒，{get_time()}")
    sleep(time_gap)

def trans_percent_to_xy( x, y, xx=0, yy=0):
    x = round(config.width * x, 2)
    y = round(config.height * y, 2)
    xx = round(config.width * xx, 2)
    yy = round(config.height * yy, 2)
    return (x, y, xx, yy)

# Recognize
def get_screenshot():  # 屏幕截图覆盖screenshop.png, 使用DEVNULL避免输出命令行
    adb_run([config.adb_path, '-s', config.device_name, 'shell', 'screencap',
                config.remote_path], stdout=DEVNULL, stderr=DEVNULL)
    adb_run([config.adb_path, '-s', config.device_name, 'pull', config.remote_path,
                config.local_path], stdout=DEVNULL, stderr=DEVNULL)
    put_image(open(config.local_path, 'rb').read(), width='500px')

def trans_pic_path(name):
    pic_path = path.join(config.current_path, "Target", "wqmt", f"{name}.png")
    return pic_path

def comparebackxy(target_pic='', target_txt='', threshold=0.8):  # 找图，返回坐标

    get_screenshot()

    if target_pic:
        target_pic_path = trans_pic_path(target_pic)
        img = cv2.imread(config.local_path, 0)  # 屏幕图片
        template = cv2.imread(target_pic_path, 0)  # 寻找目标
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) # 相关系数匹配方法：cv2.TM_CCOEFF
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        x, y = max_loc[0] + template.shape[1] // 2, max_loc[1] + template.shape[0] // 2
        if max_val > threshold:
            return (x, y)  
        else:
            return None
        
    if target_txt:
        ocr = GetOcrApi(config.ocr_path) # PaddleOCR API
        res = ocr.run(config.local_path)
        for data_dict in res['data']:
            if data_dict['text'] == target_txt:
                box_data = data_dict['box']  # 获取box数据
                x = (box_data[0][0] + box_data[2][0]) / 2  # 计算X坐标
                y = (box_data[0][1] + box_data[2][1]) / 2 # 计算Y坐标
                return (x, y)
        return None

def compare_click( target_pic='', target_txt='', threshold=0.8, sleep_time=None, times=1, 
                  success="success", fail="fail"):
    
    center = comparebackxy(target_pic, target_txt, threshold)

    if sleep_time is None:
        sleep_time = config.sleep_time

    if center:
        x, y = center
        click_coords = [str(coord) for coord in [x, y]]
        put_text(f"{success}, 找到 {target_pic}{target_txt}，坐标{click_coords}, {get_time()}")
        for _ in range(times): # 在图片位置重复点击，用于收菜之后再确认一下
            click_screen(x, y)
            sleep(sleep_time)
        return (x, y)
    
    put_text(f"{fail}, 没找到 {target_pic}{target_txt}, {get_time()}")
    sleep(sleep_time)
    return None
    