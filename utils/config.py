from ruamel.yaml import YAML
from os import path
import time
from sys import argv

# 动态参数
## 常用参数
current_path = path.join(path.dirname(argv[0]),'')
## 环境参数
ocr_path = path.join(current_path, 'tools', 'PaddleOCR-json', 'PaddleOCR-json.exe')
adb_path = path.join(current_path, 'tools', 'adb.exe')
sni_path = path.join(current_path, 'screenshot.png') # 截图后用于识别
## 当前日期
formatted_today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
#! 以上参数在引用时需要使用类似config.ocr_path的格式
# 从Config取值，当前程序专用
try:
  with open(path.join(current_path, 'config.yaml'), 'r', encoding='utf-8') as f:
    yaml = YAML()
    config = yaml.load(f)
except FileNotFoundError:
  print("Error: config.yaml file not found.")

sleep_time = config.get('sleep_time', '')
remote_path = config.get('remote_path', '')
device_name = config.get('device_name', '')
width, height = map(int, config.get('dimensions', '').split(',')) if config.get('dimensions') else (1280, 720)
saved_selections = config.get('saved_selections', '')
prog_Name = 'wqmt'