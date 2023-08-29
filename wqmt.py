from utils import *
import random

def topquit():
    adb_screenshot()
    [adb_click_percent(0.43, 0.03, sleepn=0.5,ran=1) for i in range(6)]
def homequit():
    compare_click('./Target/wqmt/homequit.png',sleepn=2,success="点击返回home",fail="")

def starttohome():# 启动到home
    adb_connect() # 连接MUMU模拟器
    [adb_click_percent(0.497656, 0.9, ran=1, sleepn=1) for i in range(3)]
    put_text("等待15秒->等待游戏完全进入主页面")
    time.sleep(15) 
    put_text("开始跳过弹窗")
    # 进入主界面
    [topquit() for i in range(2)]
    compare_click('./Target/wqmt/cancell.png',success="@@@@@@@已经取消月卡购买界面，请之后注意补充@@@@",fail="") # 检查月卡提示
    put_text("检查月卡提示")
    [topquit() for i in range(2)]
    compare_click('./Target/wqmt/confirm.png',success="@@@@@@@已经取消公会战提醒，请之后记得参加@@@@",fail="") 
    put_text("检查工会战提示")
    [topquit() for i in range(2)]
    adb_click_percent(0.683, 0.53, sleepn=1) # 展开面板 - 需要替换 面板展开()

def guild():
    put_text("开始公会收菜")
    adb_click_percent(0.933, 0.365, sleepn=2)
    adb_screenshot()
    [adb_click_percent(0.513, 0.028, ran=1, sleepn=1) for i in range(3)]    ## 避免工会弹窗
    ## 开始捐赠
    adb_click_percent(0.374, 0.69, sleepn=1) 
    [adb_click_percent(0.169, 0.827, sleepn=1) for i in range(9)]
    homequit()
    put_text("公会收菜完毕")

def dailycheckin():
    put_text("开始Check-in")
    adb_click_percent(0.825, 0.15, sleepn=2)
    [adb_click_percent(0.807, 0.64, sleepn=0.8) for i in range(10)]
    for i in range(2):
        adb_click_percent(0.448, 0.752, sleepn=0.5)
        adb_click_percent(0.558, 0.773, sleepn=0.5)
        adb_click_percent(0.67, 0.752, sleepn=0.5)
        adb_click_percent(0.792, 0.761, sleepn=0.5)
    topquit()
    put_text("Check-in完成")

def getmail():
    put_text("开始收邮件")
    adb_click_percent(0.958, 0.146, sleepn=2)
    [adb_click_percent(0.263, 0.942, sleepn=1) for i in range(4)]
    homequit()
    put_text("收完邮件")

def Bureau():
    put_text("管理局领体力，派遣")
    compare_click('./Target/wqmt/glj1.png', sleepn=3)
    ## 收体力
    [adb_click_percent(0.143, 0.456,sleepn=3) for i in range(2)]
    [compare_click('./Target/wqmt/lingqu.png', sleepn=3, times=3) for i in range(2)]
    topquit() # 退到管理局
    ## 派遣
    adb_click_percent(0.44, 0.742,sleepn=2)
    [adb_click_percent(0.105, 0.707, ran=1, sleepn=3) for i in range(3)]
    homequit()    ## 退出
    put_text("完成管理局领体力，派遣")

def friends(): # 朋友
    put_text("开始拜访朋友")
    compare_click('./Target/wqmt/friend1.png', sleepn=2)
    [adb_click_percent(0.869, 0.855, ran=1, sleepn=1) for i in range(3)]
    homequit() # 退出
    put_text("完成朋友拜访")

def construction(): # 基建
    put_text("开始基建")
    adb_click_percent(0.844, 0.629, sleepn=3)
    [adb_click_percent(0.096, 0.373,sleepn=1) for i in range(3)] # 收菜
    # 开始聊天
    put_text("开始聊天")
    [adb_click_percent(0.074, 0.249, sleepn=2) for i in range(2)]
    adb_click_percent(0.908, 0.612)
    [adb_click_percent(0.908, 0.889, ran=1) for i in range(40)]
    put_text("完成基建")
    homequit()

def purchase(): # 采购办领免费体力
    put_text("开始采购办领体力")
    compare_click('./Target/wqmt/caigouban1.png', sleepn=2)
    adb_click_percent(0.091, 0.407, sleepn=2)
    [adb_swap_percent(0.965, 0.578, 0.27, 0.611, sleepn=1) for i in range(3)]
    put_text("准备打开礼包")
    adb_screenshot()
    adb_click_percent(0.587, 0.88, sleepn=2) # 收每日体力
    adb_click_percent(0.766, 0.733, sleepn=2) # 确认
    adb_screenshot()
    topquit()
    put_text("领完体力")
    homequit()

def raidriver(): # 绣河
    put_text("开始绣河")
    compare_click('./Target/wqmt/fuben1.png', sleepn=3) # 打开副本
    adb_click_percent(0.172, 0.926, sleepn=2) # 打开绣河
    compare_click('./Target/wqmt/fuben2.png', sleepn=2, success="打开记忆风暴") 
    adb_click_percent(0.835, 0.682, sleepn=2)
    compare_click('./Target/wqmt/fubensaodang.png', sleepn=2, success="点击连续扫荡") 
    compare_click('./Target/wqmt/fubensaodangkaishi.png', sleepn=6, success="点击开始") 
    compare_click('./Target/wqmt/done.png', sleepn=2, success="点击完成") 
    compare_click('./Target/wqmt/cancell.png', sleepn=2, success="次数用光，取消扫荡") 
    [homequit() for i in range(2)]

def raid11(): # 刷11章
    compare_click('./Target/wqmt/fuben1.png', sleepn=2, success="开始raid任务") ## 打开副本界面
    compare_click('./Target/wqmt/fuben3-11.png', sleepn=2, success="打开11章")
    [adb_swap_percent(0.965, 0.578, 0.27, 0.611, sleepn=1) for i in range(2)]
    adb_click_percent(0.078, 0.541, sleepn=2) # 打开11-6
    compare_click('./Target/wqmt/fubensaodang.png', sleepn=2, success="点击连续扫荡")
    [adb_click_percent(0.712, 0.683, ran=1,) for i in range(5)] # 点击+号
    compare_click('./Target/wqmt/fubensaodangkaishi.png', sleepn=10, success="点击开始")
    topquit()
    [homequit() for i in range(2)]

def raiddark():## 深井
    compare_click('./Target/wqmt/fuben1.png', sleepn=2, success="点开始深井任务")
    adb_click_percent(0.837, 0.891, 1) # 内海
    adb_click_percent(0.193, 0.523, 2) # 浊暗之井
    while True:
        center = compare_click('./Target/wqmt/fuben4.png', sleepn=2, success="找到乐园")
        if center:
            adb_click_percent(0.587, 0.86,sleepn=2) # 点击扫荡
            topquit()
            homequit()
            break
        else:
            center = compare_click('./Target/wqmt/fuben4-1.png', 
                                   threshold=0.85 ,sleepn=2, success="切换页面")
    homequit()

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
    put_text("完成任务")

def night():
    starttohome()
    Bureau()
    friends()
    construction()
    raid11()
    put_text("完成任务")