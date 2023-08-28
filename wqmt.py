from utils import *
from pywebio.input import *
from pywebio.output import *
import random

## 之后需要设置一个检查工会战的步骤放到starthome，需要做一个管理局收体力和对话的步骤

subprocess.run(["adb", "connect", devicename])  # 连接MUMU模拟器

def topquit():
    for i in range(6):
        adb_click_percent(0.429, 0.031)
        time.sleep(0.5)
def homequit():
    adb_click_percent(0.133, 0.06)
    time.sleep(2)

def starttohome():# 启动到home
    for i in range(3):
        ran = random.uniform(0.001, 0.005)
        adb_click_percent(0.497656+ran, 0.9-ran, 1)
    time.sleep(12) 
    # 进入主界面
    for i in range(5):
        ran = random.uniform(0.001, 0.005)
        adb_click_percent(0.274219-ran, 0.03)
        time.sleep(1)
    time.sleep(1)
    center = comparebackxy('./Target/wqmt/cancell.png')
    if center is not None:
        put_text("@@@@@@@已经取消月卡购买界面，请之后注意补充@@@@")
        x,y = center
        adb_click(x, y, 2)
        for i in range(5):
            ran = random.uniform(0.001, 0.005)
            adb_click_percent(0.274219-ran, 0.03)
    center = comparebackxy('./Target/wqmt/confirm.png')
    if center is not None:
        x,y = center
        adb_click(x, y, 2)
        for i in range(5):
            ran = random.uniform(0.001, 0.005)
            adb_click_percent(0.274219-ran, 0.03)
    adb_click_percent(0.683, 0.53) # 展开面板
    time.sleep(1)

def guild():# 公会收菜
    adb_click_percent(0.933, 0.365)
    time.sleep(2)
    ## 避免工会弹窗
    for i in range(3):
        ran = random.uniform(0.001, 0.005)
        adb_click_percent(0.513+ran, 0.028+ran)
        time.sleep(0.5)
    ## 开始捐赠
    adb_click_percent(0.374, 0.69) 
    time.sleep(1)
    for i in range(9):
        adb_click_percent(0.169, 0.827)
        time.sleep(1)
    ## 退出
    homequit()

def dailycheckin(): # 晨菜daily对话
    adb_click_percent(0.825, 0.15)
    time.sleep(2)
    for i in range(15):
        adb_click_percent(0.807, 0.64)
        time.sleep(0.5)
    for i in range(2):
        adb_click_percent(0.448, 0.752)
        adb_click_percent(0.558, 0.773)
        adb_click_percent(0.67, 0.752)
        adb_click_percent(0.792, 0.761)
        time.sleep(1)
    ## 退出
    topquit()

def getmail(): # 邮件
    adb_click_percent(0.958, 0.146)
    time.sleep(2)
    for i in range(9):
        adb_click_percent(0.263, 0.942)
        time.sleep(1)
    ## 退出
    homequit()

def Bureau(): # 管理局领体力，派遣
    center = comparebackxy('./Target/wqmt/glj1.png',0.95)
    if center is not None:
        x,y = center
        adb_click(x, y,2)
    ## 收体力
    adb_click_percent(0.143, 0.456,2)
    for i in range(2):
        center = comparebackxy('./Target/wqmt/lingqu.png',0.95)
        if center is not None:
            x,y = center
            adb_click(x, y, 2)
            adb_click(x, y, 2) # 收取体力
    ### 退出
    topquit()
    ## 派遣
    adb_click_percent(0.44, 0.742,2)
    for i in range(3):
        ran = random.uniform(0.001, 0.005)
        adb_click_percent(0.105+ran, 0.707-ran)
        time.sleep(3)
    ## 退出
    homequit()

def friends(): # 朋友
    center = comparebackxy('./Target/wqmt/friend1.png',0.95)
    if center is not None:
        x,y = center
        adb_click(x, y, 2)
    for i in range(3):
        ran = random.uniform(0.001, 0.005)
        adb_click_percent(0.869+ran, 0.855-ran)
        time.sleep(2)
    ## 退出
    homequit()

def construction(): # 基建
    adb_click_percent(0.844, 0.629, 3)
    for i in range(3):
        adb_click_percent(0.096, 0.373,1)
    adb_click_percent(0.074, 0.249, 2) # 开始聊天
    adb_click_percent(0.908, 0.612)
    for i in range(50):
        ran = random.uniform(0.001, 0.005)
        adb_click_percent(0.908-ran, 0.889+ran)
    homequit()

def purchase(): # 采购办领免费体力
    center = comparebackxy('./Target/wqmt/caigouban1.png',0.95)
    if center is not None:
        x,y = center
        adb_click(x, y, 2)
    adb_click_percent(0.091, 0.407, 2)
    for i in range(4):
        adb_swap_percent(0.965, 0.578, 0.27, 0.611, sleepn=1)
    adb_click_percent(0.587, 0.88, 2) # 收每日体力
    adb_click_percent(0.766, 0.733,2) # 确认
    ## 退出
    homequit()
    homequit()

def raidriver(): # 秀河
    center = comparebackxy('./Target/wqmt/fuben1.png',0.95)
    if center is not None:
        x,y = center
        adb_click(x, y, 2)
    ## 秀河
    adb_click_percent(0.172, 0.926, 2)
    center = comparebackxy('./Target/wqmt/fuben2.png',0.95) # 记忆风暴
    if center is not None:
        x,y = center
        adb_click(x, y, 2)
    adb_click_percent(0.835, 0.682, 2)
    center = comparebackxy('./Target/wqmt/fubensaodang.png',0.95) # 开始扫荡
    if center is not None:
        x,y = center
        adb_click(x, y, 2)
        center = comparebackxy('./Target/wqmt/fubensaodangkaishi.png',0.95)
        if center is not None:
            x,y = center
            adb_click(x, y, 10)
            homequit()
            homequit()
    homequit()
    homequit()

def raid11(): # 刷11章
    center = comparebackxy('./Target/wqmt/fuben1.png',0.95) ## 回到副本界面
    if center is not None:
        x,y = center
        adb_click(x, y, 2)
    center = comparebackxy('./Target/wqmt/fuben3-11.png',0.95) ## 打开11章
    if center is not None:
        x,y = center
        adb_click(x, y, 2)
    for i in range(2):
        adb_swap_percent(0.965, 0.578, 0.27, 0.611, sleepn=1)
    adb_click_percent(0.078, 0.541, 2) # 打开11-6
    center = comparebackxy('./Target/wqmt/fubensaodang.png',0.95)
    if center is not None:
        x,y = center
        adb_click(x, y, 2)
        center = comparebackxy('./Target/wqmt/fubensaodangkaishi.png',0.95)
        if center is not None:
            x,y = center
            adb_click(x, y, 10)
            homequit()
            homequit()

def raiddark():## 深井
    center = comparebackxy('./Target/wqmt/fuben1.png',0.95) ## 回到副本界面
    if center is not None:
        x,y = center
        adb_click(x, y, 2)
    adb_click_percent(0.837, 0.891, 1) # 内海
    adb_click_percent(0.193, 0.523, 2) # 浊暗之井
    while True:
        center = comparebackxy('./Target/wqmt/fuben4.png', 0.95) ## 找乐园
        if center is not None:
            x, y = center
            adb_click(x, y, 2)
            adb_click_percent(0.587, 0.86) # 点击扫荡
            homequit()
            homequit()
            break
            center = comparebackxy('./Target/wqmt/fuben4-1.png', 0.85) ## 尝试切换
            if center is not None:
                x, y = center
                adb_click(x, y, 2)

def morning():
    starttohome()
    dailycheckin()
    guild()
    getmail()
    purchase()
    construction()
    raidriver()
    raid11()
    raiddark()

def night():
    starttohome()
    Bureau()
    friends()
    construction()
    raid11()