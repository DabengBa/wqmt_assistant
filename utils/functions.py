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
import utils.adb as adb


def get_time():
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return time_stamp


class Getxy:
    def __init__(
        self,
        tgt_pic="",
        tgt_text="",
        threshold=0.85,
        success_msg="success",
        fail_msg="fail",
        retry_enabled=True,
        retry_wait_seconds=3.0,
        x=None,
        y=None,
        xx=None,
        yy=None,
        sleep_time=None,
    ):
        """
        Initialize the `Getxy` object.

        Args:
            tgt_pic (str): The target picture.
            tgt_text (str): The target text.
            threshold (float): The confidence threshold.
            success_msg (str): The success message.
            fail_msg (str): The failure message.
            retry_enabled (bool): Whether retry is enabled.
            retry_wait_seconds (float): The wait time between retries.
            x (float): The x-coordinate.
            y (float): The y-coordinate.
            xx (float): The second x-coordinate.
            yy (float): The second y-coordinate.
            sleep_time (Optional[float]): The sleep time.

        """
        self.tgt_pic = tgt_pic
        self.tgt_pic_dir = str(path.join(cfg.curr_dir, "Target", cfg.prog_Name, f"{self.tgt_pic}.png"))
        self.tgt_text = str(tgt_text)
        self.threshold = float(threshold)
        self.success_msg = str(success_msg)
        self.fail_msg = str(fail_msg)
        self.retry_enabled = bool(retry_enabled)
        self.retry_times = int(10) if self.retry_enabled else int(1)
        self.retry_wait_seconds = float(retry_wait_seconds)
        self.x = x
        self.y = y
        self.xx = xx
        self.yy = yy

        # Log the initialization details
        log.logit(
            f"收到指令 {self.tgt_pic}{self.tgt_text}, 目标置信度{self.threshold}, 自动重试{self.retry_times}次{self.retry_enabled}, 默认延迟{self.retry_wait_seconds} 开始查找坐标。 ",
            False,
        )

        # Set the sleep time attribute
        if sleep_time is None:
            self.sleep_time = cfg.sleep_time
            log.logit(f"因为时间为None，赋值为{cfg.sleep_time}", False)

        # Call the appropriate methods based on the provided parameters
        if self.tgt_pic:
            self.find_pic()
        if self.tgt_text:
            self.find_txt()
        if self.x != 0:
            self.gen_ran_xy()
        else:
            return None
    
    def gen_ran_xy(self):
        # generate xy based on random normal distribution with 12px diffs
        if self.x is not None:
            if self.x < 1:
                self.x = round(cfg.width * self.x, 2)
                self.y = round(cfg.height * self.y, 2)
            if self.xx is not None:
                if self.xx < 1:
                    self.xx = round(cfg.width * self.xx, 2)
                    self.yy = round(cfg.height * self.yy, 2)
            while True:
                # generate coordinates xy
                self.coords = [round(rd.normalvariate(coord, 6), 2) for coord in [self.x, self.y]]
                self.x, self.y = self.coords
                # generate coordinates xx,yy
                if self.xx is not None:  
                    self.coords.extend([round(rd.normalvariate(coord, 6), 2) for coord in [self.xx, self.yy]])
                    self.x, self.y, self.xx, self.yy = self.coords
                # check if the coordinates are valid
                if all(
                    abs(coord_1 - coord_2) <= 12
                    for coord_1, coord_2 in zip([self.x, self.y, self.xx, self.yy], self.coords)
                ) and all(coord > 0 for coord in self.coords):
                    break
            log.logit(f"生成了符合要求的随机坐标 {' '.join(map(str, self.coords))}", False)
        else:
            return None


    def cap_scrn(self):
        adb.cap_scrn()
        if cfg.log_switch == "open":
            pw_put_image(open(cfg.scrn_dir, "rb").read(), width="500px")
        log.logit(f"完成截图, 保存到{cfg.scrn_dir}", False)

    def find_txt(self):
        
        for i in range(self.retry_times):
            log.logit(f"开始第{i+1}次文字匹配, 目标{self.tgt_txt}")
            sleep(self.retry_wait_seconds)
            self.cap_scrn()

            ocr = GetOcrApi(cfg.ocr_dir)  # PaddleOCR API
            res = ocr.run(cfg.scrn_dir)
            for data_dict in res["data"]:
                log.logit(f"文字匹配结果 {data_dict}", False)
                if data_dict["text"] == self.tgt_txt:
                    box_data = data_dict["box"]  # 获取box数据
                    self.x = (box_data[0][0] + box_data[2][0]) / 2  # 计算X坐标
                    self.y = (box_data[0][1] + box_data[2][1]) / 2  # 计算Y坐标
                    log.logit(f"{self.success_msg}, 根据文字匹配结果返回 {self.x} {self.y}")
                    break
                else:
                    log.logit(
                        f"{self.fail_msg}, 文字匹配失败 {self.tgt_txt}",
                    )

    def find_pic(self):

        for i in range(self.retry_times):
            log.logit(f"开始第{i+1}次图像匹配, 目标 {self.tgt_pic}")
            sleep(self.retry_wait_seconds)
            self.cap_scrn()

            img = cv2.imread(cfg.scrn_dir, 0)  # 屏幕图片
            template = cv2.imread(self.tgt_pic_dir, 0)  # 寻找目标
            #*debug print(cfg.scrn_dir)
            #*debug print(self.tgt_pic_dir)
            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)

            log.logit(f"{self.tgt_pic} 图像匹配结果 {max_val} {max_loc}", False)

            if max_val > self.threshold:
                self.x, self.y = (
                    max_loc[0] + template.shape[1] // 2,
                    max_loc[1] + template.shape[0] // 2,
                )
                log.logit(f"{self.success_msg}, 根据图像匹配结果返回 {self.x} {self.y}")
                break
            else:
                log.logit(f"{self.fail_msg}, 图像匹配失败 {self.tgt_pic}")
                return None
    
    def click(self):
        log.logit(f"开始点击屏幕坐标 {self.x} {self.y}", False)
        scrn_ctrl().click(self.x, self.y, self.sleep_time)

class scrn_ctrl:
    def __init__(self):
        pass

    def gen_ran_time(self, sleep_time=None):
        log.logit(f"收到时间 {sleep_time} 准备生成随机时间", False)
        if sleep_time is None:
            self.sleep_time = cfg.sleep_time
            log.logit(f"因为时间为None，赋值为{cfg.sleep_time}", False)
        for _ in range(25):
            mtime = round(rd.normalvariate(sleep_time, sleep_time * 0.3), 2)
            if sleep_time < mtime < sleep_time * 1.3:
                log.logit(f"根据 {sleep_time} 生成随机时间 {mtime}", False)
                if rd.random() > 0.85:
                    mtime += 1
                    log.logit(f"遇到了15%的随机事件，随机时间调整为 {mtime}", False)
                self.sleep_time = mtime
        log.logit(f"根据 {sleep_time} 在指定次数内没有生成符合要求的新时间，将返回2", False)
        self.sleep_time = 2

    def get_coords(self, x, y,xx=0,yy=0):  
        self.coords1 = Getxy(x=x, y=y).coords
        self.x = self.coords1[0]
        self.y = self.coords1[1]
        if xx != 0:
            self.coords2 = Getxy(x=xx, y=yy).coords
            self.xx = self.coords2[0]
            self.yy = self.coords2[1]

    def click(self, x, y, sleep_time=None):
        self.get_coords(x=x, y=y)
        self.gen_ran_time(sleep_time=sleep_time)
        log.logit(f"收到坐标 {self.coords1}, 休眠{self.sleep_time}点击屏幕", False)
        adb.touch(self.x, self.y)
        sleep(self.sleep_time)

    def swipe(self,x, y, xx, yy, sleep_time=None):
        self.get_coords(x=x, y=y, xx=xx, yy=yy)
        self.gen_ran_time(sleep_time=sleep_time)
        log.logit(f"收到坐标 {self.coords1} {self.coords2}, 间隔{self.sleep_time}准备滑动屏幕", False)
        adb.touch(self.x, self.y, self.xx, self.yy)
        sleep(self.sleep_time)