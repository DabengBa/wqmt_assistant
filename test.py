from utils.functions import *

def topquit():
    put_text("开始：尝试从上方退出潜在弹窗与结算窗口")
    [click_screen(0.4, 0.06, sleep_time=1) for i in range(3)]
    put_text("完成：尝试从上方退出潜在弹窗与结算窗口")
def homequit():
    put_text("开始：尝试从home按钮退出")
    compare_click(target_pic='homequit',sleep_time=5,success="已点击返回home",fail="")
    put_text("完成：尝试从home按钮退出")

def wqmtstart(): # 连接设备，失败则报错
    adb_run([utils.config.adb_path, '-s', config.devicename, 'shell', 'am', 'start', '-n', 'com.zy.wqmt.cn/com.papegames.gamelib_unity.BaseUnityImplActivity'], 
            stdout=PIPE, 
            stderr=PIPE)

def panelcheck():
    put_text("开始：检查面板")
    if comparebackxy(target_pic='friend1.png',fail="检测到面板未展开，尝试点击展开面板"):
        pass
    else:
        click_screen(0.683, 0.53, sleep_time=2) # 展开面板
        put_text("点击展开面板")
    put_text("完成：检查面板")

def starttohome():# 启动到home
    put_text("开始：启动, 检查系统公告"+get_time())
    while True:
        center = compare_click(target_pic='login')
        if center:
            put_text("点击开始游戏按钮")
            break
        else:
            put_text("没有找到开始游戏按钮，尝试启动app及检查系统公告")
            wqmtstart() # 启动无期迷途
            center = compare_click(target_pic='start1.png',sleep_time=2, success="发现系统公告")
            if center:
                click_screen(0.97,0.5) # 点击右侧边缘退出公告
            sleep(4) # 等待后检查“开始游戏”
    put_text("等待16秒-->等待游戏完全进入主页面")
    sleep(16)
    topquit()

    while True:
        center = comparebackxy(target_pic='fuben1.png')
        if center:
            break
        else:
            put_text("开始：检查月卡提示")
            compare_click(target_pic='cancell.png',success="@@@@@@@已经取消月卡购买界面，请之后注意补充@@@@",fail="")
            put_text("结束：检查月卡提示")
            topquit()
            put_text("开始：检查工会战提示")
            compare_click(target_pic='confirm.png',success="@@@@@@@已经取消公会战提醒，请之后记得参加@@@@",fail="") 
            put_text("结束：检查工会战提示")
            topquit()

    click_screen(0.683, 0.53, sleep_time=1) # 展开面板 - 需要替换 面板展开()
    get_screenshot()
    put_text("完成：启动, 检查系统公告"+get_time())

def guild():
    put_text("开始：公会收菜"+get_time())
    panelcheck()
    click_screen(0.933, 0.365, sleep_time=3)
    put_text("进入工会")
    get_screenshot()
    [click_screen(0.513, 0.028, sleep_time=1) for i in range(2)]
    put_text("开始捐赠")
    click_screen(0.374, 0.69, sleep_time=2) 
    [click_screen(0.169, 0.827, sleep_time=1.5) for i in range(6)]
    put_text("捐赠完毕")
    homequit()
    put_text("完成：公会收菜"+get_time())

def dailycheckin():
    put_text("开始：Check-in"+get_time())
    get_screenshot()
    click_screen(0.825, 0.15, sleep_time=2)
    put_text("尝试完成对话")
    [click_screen(0.807, 0.64) for i in range(10)]
    put_text("尝试收取签到礼物")
    for i in range(2):
        click_screen(0.44, 0.75)
        click_screen(0.55, 0.77)
        click_screen(0.67, 0.75)
        click_screen(0.79, 0.76)
    put_text("完成对话和礼物收取")
    get_screenshot()
    topquit()
    get_screenshot()
    put_text("完成：Check-in"+get_time())

def getmail():
    put_text("开始：收邮件"+get_time())
    get_screenshot()
    click_screen(0.958, 0.146, sleep_time=2)
    [click_screen(0.263, 0.942, sleep_time=1) for i in range(4)]
    homequit()
    get_screenshot()
    put_text("完成：收邮件"+get_time())

def Bureau():
    put_text("开始：管理局领体力，派遣"+get_time())
    compare_click(target_pic='glj1.png', sleep_time=3)

    put_text("尝试收取体力")
    [click_screen(0.143, 0.456,sleep_time=3) for i in range(2)]
    [compare_click(target_pic='lingqu.png', sleep_time=3, times=2) for i in range(2)]

    get_screenshot()
    put_text("完成收取体力")

    topquit()

    put_text("尝试派遣")
    get_screenshot()
    click_screen(0.44, 0.742,sleep_time=2)
    [click_screen(0.105, 0.707, sleep_time=3) for i in range(4)]
    put_text("完成派遣")
    homequit()
    put_text("完成：管理局领体力，派遣"+get_time())

def friends(): # 朋友
    put_text("开始：拜访朋友"+get_time())
    panelcheck()
    compare_click(target_pic='friend1.png', sleep_time=2)
    get_screenshot()
    [click_screen(0.869, 0.855, sleep_time=1) for i in range(3)]
    homequit()
    put_text("完成：朋友拜访"+get_time())

def construction(): # 基建
    put_text("开始：基建"+get_time())
    panelcheck()
    click_screen(0.844, 0.629, sleep_time=3)
    get_screenshot()
    put_text("开始收菜")
    [click_screen(0.096, 0.373,sleep_time=2) for i in range(3)] # 收菜
    put_text("开始聊天")
    [click_screen(0.074, 0.249, sleep_time=2) for i in range(2)]
    click_screen(0.908, 0.612)
    [click_screen(0.908, 0.889) for i in range(40)]
    homequit()
    put_text("完成：基建"+get_time())

def purchase(): # 采购办领免费体力
    put_text("开始：采购办领体力"+get_time())
    compare_click(target_pic='caigouban1.png', sleep_time=4)
    click_screen(0.091, 0.41, sleep_time=2)
    [swipe_screen(0.965, 0.578, 0.27, 0.611, sleep_time=1) for i in range(3)]
    put_text("准备打开礼包")
    get_screenshot()
    click_screen(0.587, 0.88, sleep_time=2) # 收每日体力
    get_screenshot()
    click_screen(0.766, 0.733, sleep_time=2) # 确认
    get_screenshot()
    topquit()
    homequit()
    put_text("结束：采购办领体力"+get_time())

def raidriver(): # 锈河
    put_text("开始：锈河副本"+get_time())
    compare_click(target_pic='fuben1.png', sleep_time=4, success="尝试打开副本界面")
    get_screenshot()

    put_text("尝试切换到锈河")
    click_screen(0.17, 0.92, sleep_time=3)

    compare_click(target_pic='fuben2.png', sleep_time=2, success="尝试打开记忆风暴") 
    get_screenshot()
    click_screen(0.835, 0.682, sleep_time=2)

    compare_click(target_pic='fubensaodang.png', sleep_time=2, success="尝试点击连续扫荡") 
    compare_click(target_pic='fubensaodangkaishi.png', sleep_time=6, success="尝试点击开始") 
    center = compare_click(target_pic='done.png', sleep_time=2, success="尝试点击完成")

    if center is None:
        compare_click(target_pic='cancell.png', sleep_time=2, success="次数用光，取消扫荡") 

    topquit()
    homequit()
    put_text("完成：锈河副本"+get_time())

def raid11(): # 刷11章
    put_text("开始：raid任务"+get_time())
    compare_click(target_pic='fuben1.png', sleep_time=4, success="尝试打开副本界面")
    compare_click(target_pic='fuben3-11.png', sleep_time=2, success="尝试打开11章")
    [swipe_screen(0.965, 0.578, 0.27, 0.611, sleep_time=1) for i in range(2)] # 滑动屏幕
    click_screen(0.078, 0.541, sleep_time=2) # 点击11-6
    compare_click(target_pic='fubensaodang.png', sleep_time=2, success="尝试点击连续扫荡")
    [click_screen(0.712, 0.683) for i in range(6)] # 点击+号
    compare_click(target_pic='fubensaodangkaishi.png', sleep_time=12, success="尝试点击开始")
    compare_click(target_pic='done.png', sleep_time=2, success="尝试点击完成")
    topquit()
    homequit()
    put_text("结束：raid任务"+get_time())

def raiddark():## 深井
    put_text("开始：深井扫荡"+get_time())
    compare_click(target_pic='fuben1.png', sleep_time=4, success="尝试打开副本界面"+get_time())
    click_screen(0.837, 0.891, sleep_time=2) # 内海
    click_screen(0.193, 0.523, sleep_time=2) # 浊暗之井
    while True:
        center = compare_click(target_pic='fuben4.png', sleep_time=2, success="尝试找到乐园"+get_time())
        if center:
            click_screen(0.587, 0.86,sleep_time=3) # 点击扫荡
            break
        else:
            center = compare_click(target_pic='fuben4-1.png', 
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