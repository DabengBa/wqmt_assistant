from ruamel.yaml import YAML
from os import path
import time

# 动态参数
current_path = path.abspath(path.dirname(__file__))  
main_path = path.abspath(path.join(current_path, '..'))
ocr_path = path.join(main_path, 'tools', 'PaddleOCR-json', 'PaddleOCR-json.exe')
adb_path = path.join(main_path, 'tools', 'adb.exe')
local_path = path.join(main_path, 'screenshot.png')
## 当前日期
formatted_today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
#! 以上参数在引用时需要使用类似config.ocr_path的格式

# 读取Config
try:
  with open(path.join(main_path, 'config.yaml'), 'r', encoding='utf-8') as f:
    yaml = YAML()
    config = yaml.load(f)
except FileNotFoundError:
  print("Error: config.yaml file not found.")

# 从Config取值
sleep_time = config.get('sleep_time', '')
remote_path = config.get('remote_path', '')
device_name = config.get('device_name', '')
width, height = map(int, config.get('dimensions', '').split(',')) if config.get('dimensions') else (1280, 720)
saved_selections = config.get('saved_selections', '')