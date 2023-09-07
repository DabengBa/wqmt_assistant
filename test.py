from utils.functions import *
# import wqmt as wq
from pywebio.input import actions
import utils.log as log
import utils.config as cfg
import random as rd

def click_screen(x, y, sleep_time=None):

    if sleep_time is None:
        sleep_time = cfg.sleep_time

    if x < 1:
        x, y = trans_percent_to_xy(x, y)
    print(x,y)
    x, y = gen_ran_xy(x, y)
    click_coords = [str(coord) for coord in [x, y]]
    time_gap = gen_ran_time(sleep_time)

    adb_run([cfg.adb_path, "-s", cfg.device_name, "shell",
             "input", "tap"] + click_coords)
    log.write_log(f"点击坐标{click_coords}，将休息{time_gap}秒")
    
    sleep(time_gap)

# def gen_ran_xy(x, y, xx=0, yy=0):
#     # 根据xy数值，在一个15px的区间内生成新的正态分布数值，如果超过15px则重新生成
#     if xx != 0:
#         while True:
#             mx = round(rd.normalvariate(x, 7), 2)
#             my = round(rd.normalvariate(y, 7), 2)
#             mxx = round(rd.normalvariate(xx, 7), 2)
#             myy = round(rd.normalvariate(yy, 7), 2)

#             if all([
#                 abs(x - mx) <= 15,
#                 abs(y - my) <= 15,
#                 abs(xx - mxx) <= 15,
#                 abs(yy - myy) <= 15,
#                 mx > 0,
#                 my > 0,
#                 mxx > 0,
#                 myy > 0
#             ]):
#                 log.write_log(f"生成随机数 {mx} {my} {mxx} {myy}")
#                 return (mx, my, mxx, myy)
#     else:
#         while True:
#             mx = round(rd.normalvariate(x, 7), 2)
#             my = round(rd.normalvariate(y, 7), 2)

#             if all([
#                 abs(x - mx) <= 15,
#                 abs(y - my) <= 15,
#                 mx > 0,
#                 my > 0,
#             ]):
#                 log.write_log(f"生成随机数 {mx} {my}")
#                 return (mx, my)

def gen_ran_xy(x, y, xx=0, yy=0):
  # 根据xy数值，在一个15px的区间内生成新的正态分布数值，如果超过15px则重新生成
  
  # 确定需要生成的随机数的个数
  num_coords = 2 if xx == 0 else 4

  while True:
    # 生成均值为x和y的正态分布随机数
    coords = [round(rd.normalvariate(coord, 7), 2) for coord in [x, y]]

    if xx != 0:
      # 生成均值为xx和yy的正态分布随机数
      coords.extend([round(rd.normalvariate(coord, 7), 2) for coord in [xx, yy]])

    if all(abs(coord_1 - coord_2) <= 15 for coord_1, coord_2 in zip([x, y, xx, yy], coords)) and all(coord > 0 for coord in coords):
      break

  log.write_log(f"生成随机数 {' '.join(map(str, coords))}")
  return tuple(coords)

click_screen(20,20)