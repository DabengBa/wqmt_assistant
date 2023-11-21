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
with open(path.join(curr_dir, "config.yaml"), "r", encoding="utf-8") as f:
    yaml = YAML()
    config = yaml.load(f)

log_switch = config.get("log_switch", "")
sleep_time = config.get("sleep_time", "")
remote_dir = config.get("remote_dir", "")
device_name = config.get("device_name", "")
sever_type = config.get("sever_type", "")
width, height = (
    map(int, config.get("dimensions", "").split(","))
    if config.get("dimensions")
    else (1280, 720)
)
saved_selections = config.get("saved_selections", "")
prog_Name = "wqmt"
