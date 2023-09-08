# Ori
from os import path
from datetime import datetime
from time import sleep
import random as rd
# Pip
from subprocess import run as adb_run, DEVNULL, PIPE
from pywebio.output import put_text, put_image
import cv2
# Private
from .PPOCR_api import GetOcrApi
import utils.config as cfg
import utils.log as log

def get_time():
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return time_stamp



# ADB
## ADB-连接
def adb_disconnect():  # 断开设备
    adb_run([cfg.adb_path, 'disconnect',  cfg.device_name],
            stdout=DEVNULL,
            stderr=DEVNULL)

def adb_connect():  # 连接设备，失败则报错
    result = adb_run([cfg.adb_path, 'connect',  cfg.device_name],
                     stdout=PIPE,
                     stderr=PIPE)
    if 'cannot' in result.stdout.decode():
        put_text("连接模拟器失败，请见检查congfig.yaml中device_name的配置")
    else:
        put_text("连接模拟器成功"+" "+get_time())
        log.write_log(f"连接模拟器成功")

## ADB-屏幕控制
### ADB-屏幕控制-随机数
def gen_ran_xy(x, y, xx=0, yy=0):
  # 根据xy数值，在一个15px的区间内生成新的正态分布数值，如果超过15px则重新生成

  while True:
    # 生成均值为x和y的正态分布随机数
    coords = [round(rd.normalvariate(coord, 7), 2) for coord in [x, y]]

    if xx != 0:
      # 生成均值为xx和yy的正态分布随机数
      coords.extend([round(rd.normalvariate(coord, 7), 2) for coord in [xx, yy]])

    if all(abs(coord_1 - coord_2) <= 15 for coord_1, coord_2 in zip([x, y, xx, yy], coords)) and all(coord > 0 for coord in coords):
      break

  log.write_log(f"生成随机数 {' '.join(map(str, coords))}")
  return tuple(coords)

def gen_ran_time(time=None):
    if time is None:
        time = cfg.sleep_time
    for _ in range(15):
        mtime = round(rd.normalvariate(time, time * 0.3), 2)
        if time < mtime < time * 1.3:
            if rd.random() > 0.85:
                mtime += 1
                log.write_log(f"根据 {time} 生成随机时间 {mtime}")
            return mtime
    return 2

## ADB-屏幕控制-执行
def adb_get_screenshot():  # 屏幕截图覆盖screenshop.png, 使用DEVNULL避免输出命令行
    adb_run([cfg.adb_path, '-s', cfg.device_name, 'shell', 'screencap',
             cfg.remote_path], stdout=DEVNULL, stderr=DEVNULL)
    adb_run([cfg.adb_path, '-s', cfg.device_name, 'pull', cfg.remote_path,
             cfg.sni_path], stdout=DEVNULL, stderr=DEVNULL)
    put_image(open(cfg.sni_path, 'rb').read(), width='500px')
    log.write_log(f"屏幕截图")

def swipe_screen(x, y, xx, yy, sleep_time=None):

    if sleep_time is None:
        sleep_time = cfg.sleep_time

    if x < 1:
        x, y, xx, yy = trans_percent_to_xy(x, y, xx, yy)

    x, y, xx, yy = gen_ran_xy(x, y, xx, yy)
    swipe_coords = [str(coord) for coord in [x, y, xx, yy]]
    time_gap = gen_ran_time(sleep_time)

    adb_run(["adb", "-s", cfg.device_name,
                    "shell", "input", "touchscreen", "swipe"] + swipe_coords)
    
    log.write_log(f"滑动坐标{swipe_coords}，将休息{time_gap}秒")
    sleep(time_gap)

def click_screen(x, y, sleep_time=None):

    if sleep_time is None:
        sleep_time = cfg.sleep_time

    if x < 1:
        x, y = trans_percent_to_xy(x, y)

    x, y = gen_ran_xy(x, y)
    click_coords = [str(coord) for coord in [x, y]]
    time_gap = gen_ran_time(sleep_time)

    adb_run([cfg.adb_path, "-s", cfg.device_name, "shell",
             "input", "tap"] + click_coords)
    log.write_log(f"点击坐标{click_coords}，将休息{time_gap}秒")
    
    sleep(time_gap)

def trans_percent_to_xy(x, y, xx=0, yy=0):
    x = round(cfg.width * x, 2)
    y = round(cfg.height * y, 2)
    xx = round(cfg.width * xx, 2)
    yy = round(cfg.height * yy, 2)
    if xx == 0:
        coord = (x, y)
        log.write_log(f"根据百分比转换 {x} {y}")
    else:
        coord = (x, y, xx, yy)
        log.write_log(f"根据百分比转换 {x} {y} {xx} {yy}")
    return coord

def compare_click(target_pic='', target_txt='', threshold=0.8, sleep_time=None, times=1,
                  success="success", fail="fail"):

    center = comparebackxy(target_pic, target_txt, threshold)

    if sleep_time is None:
        sleep_time = cfg.sleep_time

    if center:
        x, y = center
        click_coords = [str(coord) for coord in [x, y]]
        put_text(
            f"{success}, 找到 {target_pic}{target_txt}，坐标{click_coords}, {get_time()}")
        for _ in range(times):  # 在目标位置重复点击，用于收菜之后再确认一下
            click_screen(x, y)
            sleep(sleep_time)
        return (x, y)

    put_text(f"{fail}, 没找到 {target_pic}{target_txt}, {get_time()}")
    sleep(sleep_time)
    return None

# 图像/文字识别
def trans_pic_path(name):
    pic_path = path.join(cfg.current_path, "Target", cfg.prog_Name, f"{name}.png")
    return pic_path

def comparebackxy(target_pic='', target_txt='', threshold=0.8, success='success', fail='fail'):  # 找图，返回坐标

    adb_get_screenshot()
    sni_path = cfg.sni_path
    ocr_path = cfg.ocr_path

    if target_pic:
        log.write_log(f"开始图像匹配 {target_pic}")
        target_pic_path = trans_pic_path(target_pic)
        img = cv2.imread(sni_path, 0)  # 屏幕图片
        template = cv2.imread(target_pic_path, 0)  # 寻找目标
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) # 相关系数匹配方法：cv2.TM_CCOEFF
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        log.write_log(f"{target_pic} 图像匹配结果 {max_val} {max_loc}")
        x, y = max_loc[0] + template.shape[1] // 2, max_loc[1] + \
            template.shape[0] // 2
        if max_val > threshold:
            log.write_log(f"{success}, 根据图像匹配结果返回 {x} {y}")
            return (x, y)
        else:
            log.write_log(f"{fail}, 图像匹配失败 {target_pic}")
            return None

    if target_txt:
        log.write_log(f"开始文字匹配 {target_txt}")
        ocr = GetOcrApi(ocr_path)  # PaddleOCR API
        res = ocr.run(sni_path)
        for data_dict in res['data']:
            log.write_log(f"文字匹配结果 {data_dict}")
            if data_dict['text'] == target_txt:
                box_data = data_dict['box']  # 获取box数据
                x = (box_data[0][0] + box_data[2][0]) / 2  # 计算X坐标
                y = (box_data[0][1] + box_data[2][1]) / 2  # 计算Y坐标
                log.write_log(f"根据文字匹配结果返回 {x} {y}")
                return (x, y)
        log.write_log(f"文字匹配失败 {target_txt}")
        return None
