# Py
import random as rd

# Pip
from subprocess import run as adb_run, DEVNULL, PIPE

# Private
import utils.config as cfg
import utils.log as log


def touch(x, y, xx=0, yy=0):
    if xx != 0:
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
    if "cannot" in result.stdout.decode():
        log.logit(content="连接模拟器失败，请见检查congfig.yaml中device_name的配置").warning()
    else:
        log.logit(f"连接模拟器成功").text()


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
