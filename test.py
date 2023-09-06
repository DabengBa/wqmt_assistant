from debug import *
import config

def topquit():
    put_text("开始：尝试从上方退出潜在弹窗与结算窗口")
    [ScreenCtrl().click(0.4, 0.06, sleep_time=1) for i in range(3)]
    put_text("完成：尝试从上方退出潜在弹窗与结算窗口")
def homequit():
    put_text("开始：尝试从home按钮退出")
    Reconize().compare_click(targetpic='homequit',sleep_time=5,success="已点击返回home",fail="")
    put_text("完成：尝试从home按钮退出")

def wqmtstart(): # 连接设备，失败则报错
    subprocess.run([config.adb_path, '-s', config.devicename, 'shell', 'am', 'start', '-n', 'com.zy.wqmt.cn/com.papegames.gamelib_unity.BaseUnityImplActivity'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

def panelcheck():
    put_text("开始：检查面板")
    if Reconize().comparebackxy(targetpic='friend1.png',fail="检测到面板未展开，尝试点击展开面板"):
        pass
    else:
        ScreenCtrl().click(0.683, 0.53, sleep_time=1) # 展开面板
    put_text("完成：检查面板")

def starttohome():# 启动到home
    put_text("开始：启动, 检查系统公告"+get_time())
    while True:
        center = Reconize().compare_click(targetpic='login')
        if center:
            put_text("点击开始游戏按钮")
            break
        else:
            put_text("没有找到开始游戏按钮，尝试启动app及检查系统公告")
            wqmtstart() # 启动无期迷途
            center = Reconize().compare_click(targetpic='start1.png',sleep_time=2, success="发现系统公告")
            if center:
                ScreenCtrl().click(0.95,0.5) # 点击右侧边缘退出公告
            time.sleep(4)
    put_text("等待16秒-->等待游戏完全进入主页面")
    time.sleep(16)
    topquit()

    while True:
        center = Reconize().comparebackxy(targetpic='fuben1.png')
        if center:
            break
        else:
            put_text("开始：检查月卡提示")
            Reconize().compare_click(targetpic='cancell.png',success="@@@@@@@已经取消月卡购买界面，请之后注意补充@@@@",fail="")
            put_text("结束：检查月卡提示")
            topquit()
            put_text("开始：检查工会战提示")
            Reconize().compare_click(targetpic='confirm.png',success="@@@@@@@已经取消公会战提醒，请之后记得参加@@@@",fail="") 
            put_text("结束：检查工会战提示")
            topquit()

    ScreenCtrl().click(0.683, 0.53, sleep_time=1) # 展开面板 - 需要替换 面板展开()
    Reconize().adb_screenshot()
    put_text("完成：启动, 检查系统公告"+get_time())

def guild():
    put_text("开始：公会收菜"+get_time())
    panelcheck()
    Reconize().adb_screenshot()
    ScreenCtrl().click(0.933, 0.365, sleep_time=3)
    put_text("进入工会")
    Reconize().adb_screenshot()
    [ScreenCtrl().click(0.513, 0.028, sleep_time=1) for i in range(2)]
    put_text("开始捐赠")
    ScreenCtrl().click(0.374, 0.69, sleep_time=2) 
    [ScreenCtrl().click(0.169, 0.827, sleep_time=1.5) for i in range(6)]
    homequit()
    put_text("完成：公会收菜"+get_time())

def dailycheckin():
    put_text("开始：Check-in"+get_time())
    Reconize().adb_screenshot()
    ScreenCtrl().click(0.825, 0.15, sleep_time=2)
    put_text("尝试完成对话")
    [ScreenCtrl().click(0.807, 0.64, sleep_time=0.8) for i in range(10)]
    put_text("尝试收取签到礼物")
    for i in range(2):
        ScreenCtrl().click(0.448, 0.752, sleep_time=0.5)
        ScreenCtrl().click(0.558, 0.773, sleep_time=0.5)
        ScreenCtrl().click(0.67, 0.752, sleep_time=0.5)
        ScreenCtrl().click(0.792, 0.761, sleep_time=0.5)
    Reconize().adb_screenshot()
    topquit()
    Reconize().adb_screenshot()
    put_text("完成：Check-in"+get_time())

def getmail():
    put_text("开始：收邮件"+get_time())
    Reconize().adb_screenshot()
    ScreenCtrl().click(0.958, 0.146, sleep_time=2)
    [ScreenCtrl().click(0.263, 0.942, sleep_time=1) for i in range(4)]
    homequit()
    put_text("完成：收邮件"+get_time())

def Bureau():
    put_text("开始：管理局领体力，派遣"+get_time())
    Reconize().compare_click(targetpic='glj1.png', sleep_time=3)
    put_text("尝试收取体力")
    [ScreenCtrl().click(0.143, 0.456,sleep_time=3) for i in range(2)]
    [Reconize().compare_click(targetpic='lingqu.png', sleep_time=3, times=3) for i in range(2)]
    topquit()
    put_text("尝试派遣")
    Reconize().adb_screenshot()
    ScreenCtrl().click(0.44, 0.742,sleep_time=2)
    Reconize().adb_screenshot()
    [ScreenCtrl().click(0.105, 0.707, sleep_time=3) for i in range(4)]
    homequit()
    put_text("完成：管理局领体力，派遣"+get_time())

def friends(): # 朋友
    put_text("开始：拜访朋友"+get_time())
    panelcheck()
    Reconize().compare_click(targetpic='friend1.png', sleep_time=2)
    Reconize().adb_screenshot()
    [ScreenCtrl().click(0.869, 0.855, sleep_time=1) for i in range(3)]
    homequit()
    put_text("完成：朋友拜访"+get_time())

def construction(): # 基建
    put_text("开始：基建"+get_time())
    panelcheck()
    ScreenCtrl().click(0.844, 0.629, sleep_time=3)
    Reconize().adb_screenshot()
    put_text("开始收菜")
    [ScreenCtrl().click(0.096, 0.373,sleep_time=2) for i in range(3)] # 收菜
    put_text("开始聊天")
    [ScreenCtrl().click(0.074, 0.249, sleep_time=2) for i in range(2)]
    ScreenCtrl().click(0.908, 0.612)
    [ScreenCtrl().click(0.908, 0.889) for i in range(40)]
    homequit()
    put_text("完成：基建"+get_time())

def purchase(): # 采购办领免费体力
    put_text("开始：采购办领体力"+get_time())
    Reconize().compare_click(targetpic='caigouban1.png', sleep_time=4)
    ScreenCtrl().click(0.091, 0.41, sleep_time=2)
    [ScreenCtrl().percent(0.965, 0.578, 0.27, 0.611, sleep_time=1) for i in range(3)]
    put_text("准备打开礼包")
    Reconize().adb_screenshot()
    ScreenCtrl().click(0.587, 0.88, sleep_time=2) # 收每日体力
    Reconize().adb_screenshot()
    ScreenCtrl().click(0.766, 0.733, sleep_time=2) # 确认
    Reconize().adb_screenshot()
    topquit()
    homequit()
    put_text("结束：采购办领体力"+get_time())

def raidriver(): # 锈河
    put_text("开始：锈河副本"+get_time())
    Reconize().compare_click(targetpic='fuben1.png', sleep_time=4, success="尝试打开副本界面")
    Reconize().adb_screenshot()

    put_text("尝试切换到锈河")
    ScreenCtrl().click(0.17, 0.92, sleep_time=3)

    Reconize().compare_click(targetpic='fuben2.png', sleep_time=2, success="尝试打开记忆风暴") 
    Reconize().adb_screenshot()
    ScreenCtrl().click(0.835, 0.682, sleep_time=2)

    Reconize().compare_click(targetpic='fubensaodang.png', sleep_time=2, success="尝试点击连续扫荡") 
    Reconize().compare_click(targetpic='fubensaodangkaishi.png', sleep_time=6, success="尝试点击开始") 
    center = Reconize().compare_click(targetpic='done.png', sleep_time=2, success="尝试点击完成")

    if center is None:
        Reconize().compare_click(targetpic='cancell.png', sleep_time=2, success="次数用光，取消扫荡") 

    topquit()
    homequit()
    put_text("完成：锈河副本"+get_time())

def raid11(): # 刷11章
    put_text("开始：raid任务"+get_time())
    Reconize().compare_click(targetpic='fuben1.png', sleep_time=4, success="尝试打开副本界面")
    Reconize().compare_click(targetpic='fuben3-11.png', sleep_time=2, success="尝试打开11章")
    [ScreenCtrl().percent(0.965, 0.578, 0.27, 0.611, sleep_time=1) for i in range(2)] # 滑动屏幕
    ScreenCtrl().click(0.078, 0.541, sleep_time=2) # 点击11-6
    Reconize().compare_click(targetpic='fubensaodang.png', sleep_time=2, success="尝试点击连续扫荡")
    [ScreenCtrl().click(0.712, 0.683) for i in range(6)] # 点击+号
    Reconize().compare_click(targetpic='fubensaodangkaishi.png', sleep_time=12, success="尝试点击开始")
    Reconize().compare_click(targetpic='done.png', sleep_time=2, success="尝试点击完成")
    topquit()
    homequit()
    put_text("结束：raid任务"+get_time())

def raiddark():## 深井
    put_text("开始：深井扫荡"+get_time())
    Reconize().compare_click(targetpic='fuben1.png', sleep_time=4, success="尝试打开副本界面"+get_time())
    ScreenCtrl().click(0.837, 0.891, sleep_time=2) # 内海
    ScreenCtrl().click(0.193, 0.523, sleep_time=2) # 浊暗之井
    while True:
        center = Reconize().compare_click(targetpic='fuben4.png', sleep_time=2, success="尝试找到乐园"+get_time())
        if center:
            ScreenCtrl().click(0.587, 0.86,sleep_time=3) # 点击扫荡
            break
        else:
            center = Reconize().compare_click(targetpic='fuben4-1.png', 
                                   threshold=0.85 ,sleep_time=3, success="非乐园副本，切换页面"+get_time())
    topquit()
    homequit()
    put_text("完成：深井扫荡"+get_time())

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