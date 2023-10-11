# Ori
from os import path
from time import sleep
import random as rd
from typing import List, Optional

# Pip
import cv2

# Private
from .PPOCR_api import GetOcrApi
import utils.config as cfg
import utils.log as log
import utils.adb as adb


class Getxy:
    def __init__(
        self,
        tgt_pic: str = "",
        tgt_txt: str = "",
        threshold: float = cfg.default_threshold,
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
        self.success_msg = success_msg
        self.fail_msg = fail_msg
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
            path.join(
                cfg.curr_dir, "Target", cfg.prog_Name, f"{self.tgt_pic}.png"
            )
        )
        self.retry_times = int(10) if self.retry_enabled else int(1)

        # Call the appropriate methods based on the provided parameters
        if self.tgt_pic:
            log.logit(
                f"收到指令 {self.tgt_pic}, 目标置信度{self.threshold}, 自动重试{self.retry_times}次, 每次延迟{self.retry_wait_seconds} 开始查找坐标，预计找到坐标后将点击{click_times}次",
                False,
            ).text()
            self.find_pic()
        if self.tgt_txt:
            log.logit(
                f"收到指令 {self.tgt_txt}, 目标置信度{self.threshold}, 自动重试{self.retry_times}次, 每次延迟{self.retry_wait_seconds} 开始查找坐标，预计找到坐标后将点击{click_times}次",
                False,
            ).text()
            self.find_txt()
        else:
            return None

    def gen_ran_xy(self) -> List[float]:
        """
        Generate random x and y based on a normal distribution  within +- 12px.
        precondition x !=0.0
        Returns:
            List[float]: A list of generated coordinates [x, y, xx, yy].
        """
        log.logit(f"收到{self.x}, {self.y},{self.xx},{self.yy}", False).text()
        if self.x < 1:
            log.logit(f"需要转换%坐标", False).text()
            self.x = round(cfg.width * self.x, 2)
            self.y = round(cfg.height * self.y, 2)
            if self.xx > 0.0:
                self.xx = round(cfg.width * self.xx, 2)
                self.yy = round(cfg.height * self.yy, 2)
        while True:
            # generate coordinates xy
            original_coords = [self.x, self.y, self.xx, self.yy]
            self.coords = [
                round(rd.normalvariate(coord, 6.0), 2)
                for coord in original_coords
            ]
            # * debug print(f"{self.x} {self.y} {self.xx} {self.yy}")
            # check if the coordinates are valid
            if all(coord > 0.0 for coord in self.coords) and all(
                abs(orig - curr) <= 12.0
                for orig, curr in zip(original_coords, self.coords)
            ):
                self.x, self.y, self.xx, self.yy = self.coords
                break
        log.logit(f"生成了符合要求的随机坐标 {self.coords}", False).text()
        return self.coords

    def cap_scrn(self) -> None:
        """
        Captures a screenshot and saves it to the specified directory.

        Args:
            self: The current instance of the class.

        Returns:
            None
        """
        adb.cap_scrn()
        log.logit(
            f"Screenshot completed, saved to {cfg.scrn_dir}", False
        ).text()

    def find_txt(self):
        for i in range(self.retry_times):
            log.logit(f"开始第{i+1}次文字匹配, 目标{self.tgt_txt}", False).text()
            sleep(self.retry_wait_seconds)
            self.cap_scrn()

            ocr = GetOcrApi(cfg.ocr_dir)  # PaddleOCR API
            res = ocr.run(cfg.scrn_dir)
            for data_dict in res["data"]:
                log.logit(f"文字匹配结果 {data_dict}", False).text()
                if data_dict["text"] == self.tgt_txt:
                    box_data = data_dict["box"]  # 获取box数据
                    self.x = (box_data[0][0] + box_data[2][0]) / 2  # 计算X坐标
                    self.y = (box_data[0][1] + box_data[2][1]) / 2  # 计算Y坐标
                    log.logit(
                        f"{self.success_msg}, 根据文字匹配结果返回 {self.x} {self.y}",
                        False,
                    ).text()
                    self.coords = [self.x, self.y]
                    return self.coords
                else:
                    log.logit(
                        f"{self.fail_msg}, 文字匹配失败 {self.tgt_txt}",
                        False,
                    ).text()
                    self.coords = None
                    return self.coords

    def find_pic(self) -> Optional[List[float]]:
        for i in range(self.retry_times):
            log.logit(f"开始第{i+1}次图像匹配, 目标 {self.tgt_pic}", False).text()
            sleep(self.retry_wait_seconds)
            self.cap_scrn()

            img = cv2.imread(cfg.scrn_dir, 0)  # 屏幕图片
            template = cv2.imread(self.tgt_pic_dir, 0)  # 寻找目标
            # *debug print(cfg.scrn_dir)
            # *debug print(self.tgt_pic_dir)
            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)

            log.logit(
                f"{self.tgt_pic} 图像匹配结果 {max_val} {max_loc}", False
            ).text()

            if max_val > self.threshold:
                self.x, self.y = (
                    max_loc[0] + template.shape[1] // 2,
                    max_loc[1] + template.shape[0] // 2,
                )
                log.logit(
                    f"{self.success_msg}, 根据图像匹配结果返回 {self.x} {self.y}", False
                ).text()
                self.coords = [self.x, self.y, 0.0, 0.0]
                return self.coords
            else:
                log.logit(
                    f"{self.fail_msg}, 图像匹配失败 {self.tgt_pic}", False
                ).text()
                self.coords = None
                return self.coords

    def click(self):
        if self.x == 0.0:
            return
        log.logit(
            f"开始点击屏幕坐标 {self.x} {self.y}, {self.sleep_time}", False
        ).text()
        [
            scrn_ctrl().click(self.x, self.y, self.sleep_time)
            for _ in range(self.click_times)
        ]


class scrn_ctrl:
    def __init__(
        self,
    ):
        pass

    def gen_ran_time(self, sleep_time: float = cfg.sleep_time):
        """
        Generate a random time based on the given sleep_time.
        Args:
            sleep_time (float): The original sleep time.
        Returns:
            None
        """
        self.sleep_time = float(sleep_time)

        log.logit(f"收到时间 {self.sleep_time} 准备生成随机时间", False).text()
        for _ in range(45):
            mtime = round(
                rd.normalvariate(self.sleep_time, self.sleep_time * 0.2), 2
            )
            if self.sleep_time < mtime < self.sleep_time * 1.3:
                if rd.random() > 0.85:
                    mtime += 1
                    log.logit(f"遇到了15%的随机事件，随机时间调整为 {mtime}", False).text()
                log.logit(f"根据 {self.sleep_time} 生成随机时间 {mtime}", False).text()
                self.sleep_time = mtime
                break

    def get_coords(self, x: float, y: float, xx: float = 0.0, yy: float = 0.0):
        """
        Generate random coordinates and assign them to instance variables.

        Args:
            x: The x-coordinate.
            y: The y-coordinate.
            xx: The xx-coordinate (default 0).
            yy: The yy-coordinate (default 0).
        """
        self.coords = Getxy(x=x, y=y, xx=xx, yy=yy).gen_ran_xy()
        self.x, self.y, self.xx, self.yy = self.coords

    def click(self, x: float, y: float, sleep_time: float = cfg.sleep_time):
        """
        Clicks on the screen at the specified coordinates.

        Args:
            x (float): The x-coordinate of the click.
            y (float): The y-coordinate of the click.
            sleep_time (float, optional): The amount of time to sleep after clicking. Defaults to cfg.sleep_time.
        """
        self.get_coords(x=x, y=y)
        self.gen_ran_time(sleep_time=sleep_time)
        log.logit(
            f"收到坐标 {self.x},{self.y}, 休眠{self.sleep_time}点击屏幕", False
        ).text()
        adb.touch(self.x, self.y)
        sleep(self.sleep_time)

    def swipe(
        self,
        x: float,
        y: float,
        xx: float,
        yy: float,
        sleep_time: float = cfg.sleep_time,
    ):
        """
        Swipe the screen from (x, y) to (xx, yy) with a sleep time between swipes.

        Args:
            x (float): The x-coordinate of the starting point.
            y (float): The y-coordinate of the starting point.
            xx (float): The x-coordinate of the ending point.
            yy (float): The y-coordinate of the ending point.
            sleep_time (float, optional): The sleep time between swipes. Defaults to cfg.sleep_time.
        """
        self.get_coords(x=x, y=y, xx=xx, yy=yy)
        self.gen_ran_time(sleep_time=sleep_time)
        log.logit(
            f"收到坐标 {self.x},{self.y},{self.xx},{self.yy}, 间隔{self.sleep_time}准备滑动屏幕",
            False,
        ).text()
        adb.touch(self.x, self.y, self.xx, self.yy)
        sleep(self.sleep_time)
