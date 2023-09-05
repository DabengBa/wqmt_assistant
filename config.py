from ruamel.yaml import YAML
import os

# 读取Config
try:
  with open('config.yaml', 'r', encoding='utf-8') as f:
    yaml = YAML()
    config = yaml.load(f)
except FileNotFoundError:
  print("Error: config.yaml file not found.")

# 写入Config
# with open('config.yaml', 'w', encoding='utf-8') as f:
#   yaml.dump(
#     config,
#     f,
#   )

# 从Config赋值
sleep_time = config.get('sleep_time', '')
remote_path = config.get('remote_path', '')
device_name = config.get('device_name', '')
width, height = map(int, config.get('dimensions', '').split(',')) if config.get('dimensions') else (11280, 720)
# 动态参数
current_path = os.path.dirname(__file__)
ocr_path = os.path.join(current_path, 'tools', 'PaddleOCR-json', 'PaddleOCR-json.exe')
adb_path = os.path.join(current_path, 'tools', 'adb.exe')
local_path = os.path.join(current_path, 'screenshot.png')
#！ 以上参数在引用时需要使用类似config.ocr_path的格式
