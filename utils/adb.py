# Py
import re
import sys
import random as rd


# Pip
from subprocess import run as adb_run, DEVNULL, PIPE

# Private
import utils.config as cfg
import utils.log as log


def touch(x, y, xx=0.0, yy=0.0):
    if xx != 0.0:
        duration = rd.randint(150, 250)
        adb_run(
            [
                cfg.adb_dir,
                "-s",
                cfg.device_name,
                "shell",
                "input",
                "swipe",
                str(x),
                str(y),
                str(xx),
                str(yy),
                str(duration),
            ]
        )
    else:
        adb_run(
            [
                cfg.adb_dir,
                "-s",
                cfg.device_name,
                "shell",
                "input",
                "tap",
                str(x),
                str(y),
            ]
        )


def cap_scrn():
    adb_run(
        [
            cfg.adb_dir,
            "-s",
            cfg.device_name,
            "shell",
            "screencap",
            cfg.remote_dir,
        ],
        stdout=DEVNULL,
        stderr=DEVNULL,
    )
    adb_run(
        [
            cfg.adb_dir,
            "-s",
            cfg.device_name,
            "pull",
            cfg.remote_dir,
            cfg.scrn_dir,
        ],
        stdout=DEVNULL,
        stderr=DEVNULL,
    )


def disconnect():  # 断开设备
    adb_run(
        [cfg.adb_dir, "disconnect", cfg.device_name],
        stdout=DEVNULL,
        stderr=DEVNULL,
    )


def connect():  # 连接设备，失败则报错
    result = adb_run(
        [cfg.adb_dir, "connect", cfg.device_name], stdout=PIPE, stderr=PIPE
    )
    if "already connected" in result.stdout.decode():
        log.logit("自动连接模拟器成功").text()
    else:
        reconnect()


def reconnect():
    log.logit(content="未连接模拟器，将会尝试自动连接").text()
    result = adb_run([cfg.adb_dir, "devices"], stdout=PIPE, stderr=PIPE)
    pat = re.compile(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:.\d{1,5}")
    devices = pat.findall(result.stdout.decode())
    if not devices:
        log.logit(content="未检测到模拟器或手机，请检查设备是否连接").warning()
        sys.exit()
    result = adb_run(
        [cfg.adb_dir, "connect", devices[0]], stdout=PIPE, stderr=PIPE
    )
    if "already connected" in result.stdout.decode():
        log.logit("连接模拟器成功").text()
        cfg.device_name = devices[0]
    else:
        log.logit(content="连接模拟器失败，请检查设备是否连接").warning()
    result = adb_run(
        [cfg.adb_dir, "-s", cfg.device_name, "shell", "wm", "size"],
        stdout=PIPE,
        stderr=PIPE,
    )
    pat = re.compile(r"\d{1,5}")
    height, width = pat.findall(result.stdout.decode())
    cfg.width, cfg.height = int(width), int(height)
    log.logit(f"屏幕尺寸为{width}x{height}").text()


def start(app):
    adb_run(
        [
            cfg.adb_dir,
            "-s",
            cfg.device_name,
            "shell",
            "am",
            "start",
            "-n",
            app,
        ],
        stdout=PIPE,
        stderr=PIPE,
    )


def close(app):
    adb_run(
        [
            cfg.adb_dir,
            "-s",
            cfg.device_name,
            "shell",
            "am",
            "force-stop",
            app,
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
