from ruamel.yaml import YAML
from os import path
import time
from sys import argv

# 动态参数
## 常用参数
curr_dir = path.join(path.dirname(argv[0]), "")
default_threshold = 0.85
## 环境参数
ocr_dir = path.join(curr_dir, "tools", "PaddleOCR-json", "PaddleOCR-json.exe")
adb_dir = path.join(curr_dir, "tools", "adb.exe")
scrn_dir = path.join(curr_dir, "screenshot.png")  # 截图后用于识别
## 当前日期
formatted_today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
#! 以上参数在引用时需要使用类似config.ocr_dir的格式


# 从Config取值，当前程序专用
def load_config():
    with open(path.join(curr_dir, "config.yaml"), "r", encoding="utf-8") as f:
        yaml = YAML()
        config = yaml.load(f)
    return config


def save_config():
    with open(path.join(curr_dir, "config.yaml"), "w", encoding="utf-8") as f:
        yaml = YAML()
        yaml.dump(config, f)


config = load_config()

log_switch = config["log_switch"]
sleep_time = config["sleep_time"]
remote_dir = config["remote_dir"]
device_name = config["device_name"]
sever_type = config["sever_type"]
fights = config["saved_fights"]
last_action = config["saved_last_action"]
width, height = (1280, 720)  # TODO 是否已经写死分辨率?
saved_selections = config["saved_selections"]
prog_Name = "wqmt"
