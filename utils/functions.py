# Ori
from os import path
from datetime import datetime
from time import sleep
import random as rd
# Pip
from subprocess import run as adb_run, DEVNULL, PIPE
from pywebio.output import put_image as pw_put_image
import cv2
# Private
from .PPOCR_api import GetOcrApi
import utils.config as cfg
import utils.log as log


def get_time():
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return time_stamp

# ADB
# ADB-连接


def adb_disconnect():  # 断开设备
    adb_run([cfg.adb_dir, 'disconnect',  cfg.device_name],
            stdout=DEVNULL,
            stderr=DEVNULL)


def adb_connect():  # 连接设备，失败则报错
    result = adb_run([cfg.adb_dir, 'connect',  cfg.device_name],
                     stdout=PIPE,
                     stderr=PIPE)
    if 'cannot' in result.stdout.decode():
        log.logit(f"连接模拟器失败，请见检查congfig.yaml中device_name的配置")
    else:
        log.logit(f"连接模拟器成功")

# ADB-屏幕控制
# ADB-屏幕控制-随机数


def gen_ran_xy(x, y, xx=0, yy=0):
    # 根据xy数值，在一个15px的区间内生成新的正态分布数值，如果超过15px则重新生成
    log.logit(f"接收坐标 {x} {y} {xx} {yy}，准备生成随机坐标", False)
    while True:
        # 生成均值为x和y的正态分布随机数
        coords = [round(rd.normalvariate(coord, 7), 2) for coord in [x, y]]

        if xx != 0:
            # 生成均值为xx和yy的正态分布随机数
            coords.extend([round(rd.normalvariate(coord, 7), 2)
                          for coord in [xx, yy]])

        if all(abs(coord_1 - coord_2) <= 15 for coord_1, coord_2 in zip([x, y, xx, yy], coords)) and all(coord > 0 for coord in coords):
            break

    log.logit(f"生成了符合要求的随机坐标 {' '.join(map(str, coords))}", False)
    return tuple(coords)


def gen_ran_time(time=None):
    log.logit(f"收到时间 {time} 准备生成随机时间", False)
    if time is None:
        time = cfg.sleep_time
        log.logit(f"因为时间为None，赋值为{cfg.sleep_time}", False)
    for _ in range(15):
        mtime = round(rd.normalvariate(time, time * 0.3), 2)
        if time < mtime < time * 1.3:
            log.logit(f"根据 {time} 生成随机时间 {mtime}", False)
            if rd.random() > 0.85:
                mtime += 1
                log.logit(f"遇到了15%的随机事件，随机时间调整为 {mtime}", False)
            return mtime
    log.logit(f"根据 {time} 在指定次数内没有生成符合要求的新时间，将返回2", False)
    return 2

# ADB-屏幕控制-执行


def adb_cap_scrn():
    log.logit(f"开始屏幕截图，尝试保存到{cfg.remote_dir}", False)
    adb_run([cfg.adb_dir, '-s', cfg.device_name, 'shell', 'screencap',
             cfg.remote_dir], stdout=DEVNULL, stderr=DEVNULL)
    log.logit(f"开始将截图文件拉到本地{cfg.scrn_dir}", False)
    adb_run([cfg.adb_dir, '-s', cfg.device_name, 'pull', cfg.remote_dir,
             cfg.scrn_dir], stdout=DEVNULL, stderr=DEVNULL)
    pw_put_image(open(cfg.scrn_dir, 'rb').read(), width='500px')
    log.logit(f"完成截图, 保存到{cfg.scrn_dir}", False)


def swipe_screen(x, y, xx, yy, sleep_time=None):

    log.logit(f"收到坐标 {x} {y} {xx} {yy}，{sleep_time}准备滑动屏幕", False)

    if sleep_time is None:
        sleep_time = cfg.sleep_time
        log.logit(f"因为时间为None，赋值为{cfg.sleep_time}", False)
    if x < 1:
        log.logit(f"收到百分比坐标，将传入trans转换成px", False)
        x, y, xx, yy = trans_percent_to_xy(x, y, xx, yy)

    x, y, xx, yy = gen_ran_xy(x, y, xx, yy)
    swipe_coords = [str(coord) for coord in [x, y, xx, yy]]
    time_gap = gen_ran_time(sleep_time)

    log.logit(f"开始通过adb滑动屏幕", False)
    adb_run(["adb", "-s", cfg.device_name,
                    "shell", "input", "touchscreen", "swipe"] + swipe_coords)

    log.logit(f"滑动坐标{swipe_coords}完成，将休息{time_gap}秒", False)
    sleep(time_gap)


def click_screen(x, y, sleep_time=None):
    log.logit(f"收到坐标 {x} {y}，{sleep_time}准备点击屏幕", False)

    if sleep_time is None:
        sleep_time = cfg.sleep_time

    if x < 1:
        x, y = trans_percent_to_xy(x, y)

    x, y = gen_ran_xy(x, y)
    click_coords = [str(coord) for coord in [x, y]]
    time_gap = gen_ran_time(sleep_time)

    log.logit(f"开始通过adb滑动屏幕", False)
    adb_run([cfg.adb_dir, "-s", cfg.device_name, "shell",
             "input", "tap"] + click_coords)
    log.logit(f"点击坐标{click_coords}，将休息{time_gap}秒", False)

    sleep(time_gap)


def trans_percent_to_xy(x, y, xx=0, yy=0):
    log.logit(f"根据百分比转换 {x} {y} {xx} {yy}", False)
    
    x = round(cfg.width * x, 2)
    y = round(cfg.height * y, 2)
    xx = round(cfg.width * xx, 2)
    yy = round(cfg.height * yy, 2)

    if xx == 0:
        coord = (x, y)
    else:
        coord = (x, y, xx, yy)
    log.logit(f"得到转换后的坐标为 {x} {y} {xx} {yy}", False)
    return coord


def comp_tap(tgt_pic='', tgt_txt='', threshold=0.8, sleep_time=None, times=1,
             success="success", fail="fail"):
    log.logit(
        f"comp_tap收到指令 {tgt_pic}{tgt_txt} {threshold} {sleep_time} {times}，开始查找", False)

    center = comp_xy(tgt_pic, tgt_txt, threshold)

    if sleep_time is None:
        sleep_time = cfg.sleep_time

    if center:
        x, y = center
        click_coords = [str(coord) for coord in [x, y]]
        log.logit(f"{success}, 找到 {tgt_pic}{tgt_txt}，坐标{click_coords}", False)
        for _ in range(times):  # 在目标位置重复点击，用于收菜之后再确认一下
            click_screen(x, y)
            sleep(sleep_time)
        return (x, y)

    log.logit(f"{fail}, 没找到 {tgt_pic}{tgt_txt}", False)
    sleep(sleep_time)
    return None

# 图像/文字识别


def trans_pic_dir(name):
    pic_dir = path.join(cfg.curr_dir, "Target",
                        cfg.prog_Name, f"{name}.png")
    log.logit(f"trans生成图片路径为 {pic_dir}", False)
    return pic_dir


def comp_xy(tgt_pic='', tgt_txt='', threshold=0.8, success='success', fail='fail'):
    log.logit(f"comp_xy收到指令 {tgt_pic}{tgt_txt} {threshold}，开始查找坐标", False)

    adb_cap_scrn()
    scrn_dir = cfg.scrn_dir
    ocr_dir = cfg.ocr_dir

    if tgt_pic:
        log.logit(f"开始图像匹配 {tgt_pic}")
        tgt_pic_dir = trans_pic_dir(tgt_pic)
        img = cv2.imread(scrn_dir, 0)  # 屏幕图片
        template = cv2.imread(tgt_pic_dir, 0)  # 寻找目标
        # 相关系数匹配方法：cv2.TM_CCOEFF
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        log.logit(f"{tgt_pic} 图像匹配结果 {max_val} {max_loc}", False)
        x, y = max_loc[0] + template.shape[1] // 2, max_loc[1] + \
            template.shape[0] // 2
        if max_val > threshold:
            log.logit(f"{success}, 根据图像匹配结果返回 {x} {y}")
            return (x, y)
        else:
            log.logit(f"{fail}, 图像匹配失败")
            return None

    if tgt_txt:
        log.logit(f"开始文字匹配 {tgt_txt}")
        ocr = GetOcrApi(ocr_dir)  # PaddleOCR API
        res = ocr.run(scrn_dir)
        for data_dict in res['data']:
            log.logit(f"文字匹配结果 {data_dict}", False)
            if data_dict['text'] == tgt_txt:
                box_data = data_dict['box']  # 获取box数据
                x = (box_data[0][0] + box_data[2][0]) / 2  # 计算X坐标
                y = (box_data[0][1] + box_data[2][1]) / 2  # 计算Y坐标
                log.logit(f"根据文字匹配结果返回 {x} {y}")
                return (x, y)
        log.logit(f"文字匹配失败 {tgt_txt}", F)
        return None