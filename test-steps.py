import os
from utils.PPOCR_api import GetOcrApi



current_dir = os.path.dirname(__file__)  # 获取当前脚本所在目录的路径

def pic_path(name):
    path = os.path.join(current_dir, "Target", "wqmt", f"{name}.png")
    return path

argument = {'config_path': "语言1.txt"}
ocr_path = str(os.path.join(current_dir, "tools", "PaddleOCR-json", "PaddleOCR-json.exe"))

ocr = GetOcrApi(ocr_path)
res = ocr.run(pic_path("fuben4"))
print("识别结果：\n", res)


target_text = '乐园幻境'
for data_dict in res['data']:
  if data_dict['text'] == target_text:
    box_data = data_dict['box']  # 获取box数据
    x_coordinate = (box_data[0][0] + box_data[2][0]) / 2  # 计算X坐标
    y_coordinate = (box_data[0][1] + box_data[2][1]) / 2 # 计算Y坐标
    break  # 找到目标文本后跳出循环

print("提取的坐标：", x_coordinate, y_coordinate)