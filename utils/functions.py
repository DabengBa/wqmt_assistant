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
        tgt_pic: str = "",
        tgt_txt: str = "",
        threshold: float = 0.85,
        success_msg: str = "success",
        fail_msg: str = "fail",
        retry_enabled: bool = True,
        retry_wait_seconds: float = 3.0,
        x: float = 0.0,
        y: float = 0.0,
        xx: float = 0.0,
        yy: float = 0.0,
        sleep_time: float = cfg.sleep_time,
        click_times: int = 1,
    ):
        """
        Initialize the `Getxy` object.

        Args:
            tgt_pic (str): The target picture.
            tgt_txt (str): The target text.
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
        # Set the attributes
        # get
        self.tgt_pic = str(tgt_pic)
        self.tgt_txt = str(tgt_txt)
        self.threshold = float(threshold)
        self.success_msg = str(success_msg)
        self.fail_msg = str(fail_msg)
        self.retry_enabled = bool(retry_enabled)
        self.retry_wait_seconds = float(retry_wait_seconds)
        self.x = float(x)
        self.y = float(y)
        self.xx = float(xx)
        self.yy = float(yy)
        self.sleep_time = float(sleep_time)
        self.click_times = int(click_times)

        # Generated
        self.tgt_pic_dir = str(
            path.join(cfg.curr_dir, "Target", cfg.prog_Name, f"{self.tgt_pic}.png")
        )
        self.retry_times = int(10) if self.retry_enabled else int(1)

        # Call the appropriate methods based on the provided parameters
        if self.tgt_pic:
            log.logit(
            f"收到指令 {self.tgt_pic}, 目标置信度{self.threshold}, 自动重试{self.retry_times}次, 每次延迟{self.retry_wait_seconds} 开始查找坐标，预计找到坐标后将点击{click_times}次",
            False,
        )
            self.find_pic()
        if self.tgt_txt:
            log.logit(
            f"收到指令 {self.tgt_txt}, 目标置信度{self.threshold}, 自动重试{self.retry_times}次, 每次延迟{self.retry_wait_seconds} 开始查找坐标，预计找到坐标后将点击{click_times}次",
            False,
        )
            self.find_txt()
        else:
            return None

    def gen_ran_xy(self):
        # precondition x !=0.0generate xy based on random normal distribution with 12px diffs. 
        log.logit(f"收到{self.x}, {self.y},{self.xx},{self.yy}", False)
        if self.x < 1:
            log.logit(f"需要转换%坐标", False)
            self.x = round(cfg.width * self.x, 2)
            self.y = round(cfg.height * self.y, 2)
            if self.xx > 0.0:
                self.xx = round(cfg.width * self.xx, 2)
                self.yy = round(cfg.height * self.yy, 2)
        while True:
            # generate coordinates xy
            original_coords = [self.x, self.y, self.xx, self.yy]
            self.coords = [round(rd.normalvariate(coord, 6.0), 2) for coord in original_coords]
            #* debug print(f"{self.x} {self.y} {self.xx} {self.yy}")
            # check if the coordinates are valid
            if all(coord > 0.0 for coord in self.coords) and \
                all(abs(orig - curr) <= 12.0 for orig, curr in zip(original_coords, self.coords)):
                self.x, self.y, self.xx, self.yy = self.coords
                break
        log.logit(f"生成了符合要求的随机坐标 {self.coords}", False)
        return self.coords

    def cap_scrn(self):
        adb.cap_scrn()
        log.logit(f"完成截图, 保存到{cfg.scrn_dir}", False)

    def find_txt(self):
        for i in range(self.retry_times):
            log.logit(f"开始第{i+1}次文字匹配, 目标{self.tgt_txt}", False)
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
                    log.logit(f"{self.success_msg}, 根据文字匹配结果返回 {self.x} {self.y}", False)
                    self.coords = [self.x, self.y]
                    return self.coords
                else:
                    log.logit(
                        f"{self.fail_msg}, 文字匹配失败 {self.tgt_txt}", False,
                    )
                    self.coords = None
                    return self.coords

    def find_pic(self):
        for i in range(self.retry_times):
            log.logit(f"开始第{i+1}次图像匹配, 目标 {self.tgt_pic}", False)
            sleep(self.retry_wait_seconds)
            self.cap_scrn()

            img = cv2.imread(cfg.scrn_dir, 0)  # 屏幕图片
            template = cv2.imread(self.tgt_pic_dir, 0)  # 寻找目标
            # *debug print(cfg.scrn_dir)
            # *debug print(self.tgt_pic_dir)
            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)

            log.logit(f"{self.tgt_pic} 图像匹配结果 {max_val} {max_loc}", False)

            if max_val > self.threshold:
                self.x, self.y = (
                    max_loc[0] + template.shape[1] // 2,
                    max_loc[1] + template.shape[0] // 2,
                )
                log.logit(f"{self.success_msg}, 根据图像匹配结果返回 {self.x} {self.y}", False)
                self.coords = [self.x, self.y, 0.0, 0.0]
                return self.coords
            else:
                log.logit(f"{self.fail_msg}, 图像匹配失败 {self.tgt_pic}", False)
                self.coords = None
        return self.coords

    def click(self):
        log.logit(f"开始点击屏幕坐标 {self.x} {self.y}, {self.sleep_time}", False)
        [
            scrn_ctrl().click(self.x, self.y, self.sleep_time)
            for _ in range(self.click_times)
        ]


class scrn_ctrl:
    def __init__(self):
        pass

    def gen_ran_time(self, sleep_time:float=cfg.sleep_time):
        log.logit(f"收到时间 {sleep_time} 准备生成随机时间", False)
        self.sleep_time = float(sleep_time)
        for _ in range(35):
            mtime = round(rd.normalvariate(self.sleep_time, self.sleep_time * 0.2), 2)
            if self.sleep_time < mtime < self.sleep_time * 1.3:
                log.logit(f"根据 {self.sleep_time} 生成随机时间 {mtime}", False)
                if rd.random() > 0.85:
                    mtime += 1
                    log.logit(f"遇到了15%的随机事件，随机时间调整为 {mtime}", False)
                self.sleep_time = mtime
                break
            else:
                log.logit(f"根据 {self.sleep_time} 在指定次数内没有生成符合要求的新时间，将使用原值", False)

    def get_coords(self, x, y, xx=0, yy=0):
        self.coords = Getxy(x=x, y=y, xx=xx, yy=yy).gen_ran_xy()
        self.x = self.coords[0]
        self.y = self.coords[1]
        self.xx = self.coords[2]
        self.yy = self.coords[3]

    def click(self, x, y, sleep_time=cfg.sleep_time):
        self.get_coords(x=x, y=y)
        self.gen_ran_time(sleep_time=sleep_time)
        log.logit(f"收到坐标 {self.x},{self.y}, 休眠{self.sleep_time}点击屏幕", False)
        adb.touch(self.x, self.y)
        sleep(self.sleep_time)

    def swipe(self, x, y, xx, yy, sleep_time=cfg.sleep_time):
        self.get_coords(x=x, y=y, xx=xx, yy=yy)
        self.gen_ran_time(sleep_time=sleep_time)
        log.logit(
            f"收到坐标 {self.x},{self.y},{self.xx},{self.yy}, 间隔{self.sleep_time}准备滑动屏幕", False
        )
        adb.touch(self.x, self.y, self.xx, self.yy)
        sleep(self.sleep_time)
