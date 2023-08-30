from debug import *

def topquit():
    put_text("开始：尝试从上方退出潜在弹窗与结算窗口")
    [d.click(0.5, 0.05) for i in range(3)]
    put_text("完成：尝试从上方退出潜在弹窗与结算窗口")
def homequit():
    put_text("开始：尝试从home按钮退出")
    compare_click('./Target/wqmt/homequit.png',success="已点击返回home",fail="")
    adb_screenshot()
    put_text("完成：尝试从home按钮退出")

def starttohome():# 启动到home
    put_text("开始：启动, 检查系统公告"+get_time())
    app_info = d.app_current()
    package = app_info.get('package')
    if package != "com.zy.wqmt.cn":
        d.app_start("com.zy.wqmt.cn")
        put_text("游戏还未启动，请等待启动")
        time.sleep(15)
    center = compare_click('./Target/wqmt/start1.png', success="发现系统公告", fail="未发现系统公告")
    if center:
        topquit()
    put_text("点击开始")
    [d.click(0.498, 0.903) for i in range(2)]
    put_text("等待16秒-->等待游戏完全进入主页面")
    time.sleep(16)
    topquit()

    while True:
        center = comparebackxy('./Target/wqmt/fuben1.png')
        if center:
            break
        else:
            put_text("开始：检查月卡提示")
            compare_click('./Target/wqmt/cancell.png',success="@@@@@@@已经取消月卡购买界面，请之后注意补充@@@@",fail="")
            put_text("结束：检查月卡提示")
            topquit()
            put_text("开始：检查工会战提示")
            compare_click('./Target/wqmt/confirm.png',success="@@@@@@@已经取消公会战提醒，请之后记得参加@@@@",fail="") 
            put_text("结束：检查工会战提示")
            topquit()

    d.click(0.683, 0.53) # 展开面板 - 需要替换 面板展开()
    adb_screenshot()
    put_text("完成：启动, 检查系统公告"+get_time())

def guild():
    put_text("开始：公会收菜"+get_time())
    adb_screenshot()
    d.click(0.933, 0.365)
    put_text("进入工会")
    adb_screenshot()
    [d.click(0.513, 0.028) for i in range(2)]
    put_text("开始捐赠")
    d.click(0.374, 0.69) 
    [d.click(0.169, 0.827) for i in range(6)]
    homequit()
    put_text("完成：公会收菜"+get_time())

def dailycheckin():
    put_text("开始：Check-in"+get_time())
    adb_screenshot()
    d.click(0.825, 0.15)
    put_text("尝试完成对话")
    [d.click(0.807, 0.64) for i in range(10)]
    put_text("尝试收取签到礼物")
    for i in range(2):
        d.click(0.448, 0.752)
        d.click(0.558, 0.773)
        d.click(0.67, 0.752)
        d.click(0.792, 0.761)
    topquit()
    adb_screenshot()
    put_text("完成：Check-in"+get_time())

def getmail():
    put_text("开始：收邮件"+get_time())
    adb_screenshot()
    d.click(0.958, 0.146)
    [d.click(0.263, 0.942) for i in range(4)]
    homequit()
    put_text("完成：收邮件"+get_time())

def Bureau():
    put_text("开始：管理局领体力，派遣"+get_time())
    compare_click('./Target/wqmt/glj1.png')
    put_text("尝试收取体力")
    [d.click(0.143, 0.456) for i in range(2)]
    [compare_click('./Target/wqmt/lingqu.png', times=3) for i in range(2)]
    topquit()
    put_text("尝试派遣")
    adb_screenshot()
    d.click(0.44, 0.742)
    adb_screenshot()
    [d.click(0.105, 0.707, ran=1) for i in range(3)]
    homequit()
    put_text("完成：管理局领体力，派遣"+get_time())

def friends(): # 朋友
    put_text("开始：拜访朋友"+get_time())
    compare_click('./Target/wqmt/friend1.png')
    adb_screenshot()
    [d.click(0.869, 0.855, ran=1) for i in range(3)]
    homequit()
    put_text("完成：朋友拜访"+get_time())

def construction(): # 基建
    put_text("开始：基建"+get_time())
    d.click(0.844, 0.629)
    adb_screenshot()
    put_text("开始收菜")
    [d.click(0.096, 0.373) for i in range(3)] # 收菜
    put_text("开始聊天")
    [d.click(0.074, 0.249) for i in range(2)]
    d.click(0.908, 0.612)
    [d.click(0.908, 0.889, ran=1) for i in range(30)]
    homequit()
    put_text("完成：基建"+get_time())

def purchase(): # 采购办领免费体力
    put_text("开始：采购办领体力"+get_time())
    compare_click('./Target/wqmt/caigouban1.png')
    d.click(0.091, 0.41)
    [d.swipe(0.965, 0.578, 0.27, 0.611) for i in range(3)]
    put_text("准备打开礼包")
    adb_screenshot()
    d.click(0.587, 0.88) # 收每日体力
    adb_screenshot()
    d.click(0.766, 0.733) # 确认
    adb_screenshot()
    topquit()
    homequit()
    put_text("结束：采购办领体力"+get_time())

def raidriver(): # 锈河
    put_text("开始：锈河副本"+get_time())
    compare_click('./Target/wqmt/fuben1.png', success="尝试打开副本界面")
    adb_screenshot()

    put_text("尝试切换到锈河")
    d.click(0.17, 0.92)

    compare_click('./Target/wqmt/fuben2.png', success="尝试打开记忆风暴") 
    adb_screenshot()
    d.click(0.835, 0.682)

    compare_click('./Target/wqmt/fubensaodang.png', success="尝试点击连续扫荡") 
    compare_click('./Target/wqmt/fubensaodangkaishi.png', success="尝试点击开始") 
    center = compare_click('./Target/wqmt/done.png', success="尝试点击完成")

    if center is None:
        compare_click('./Target/wqmt/cancell.png', success="次数用光，取消扫荡") 

    topquit()
    homequit()
    put_text("完成：锈河副本"+get_time())

def raid11(): # 刷11章
    put_text("开始：raid任务"+get_time())
    compare_click('./Target/wqmt/fuben1.png', success="尝试打开副本界面")
    compare_click('./Target/wqmt/fuben3-11.png', success="尝试打开11章")
    [d.swipe(0.965, 0.578, 0.27, 0.611) for i in range(2)] # 滑动屏幕
    d.click(0.078, 0.541) # 点击11-6
    compare_click('./Target/wqmt/fubensaodang.png', success="尝试点击连续扫荡")
    [d.click(0.712, 0.683, ran=1,) for i in range(5)] # 点击+号
    compare_click('./Target/wqmt/fubensaodangkaishi.png', success="尝试点击开始")
    compare_click('./Target/wqmt/done.png', success="尝试点击完成")
    topquit()
    homequit()
    put_text("结束：raid任务"+get_time())

def raiddark():## 深井
    put_text("开始：深井扫荡"+get_time())
    compare_click('./Target/wqmt/fuben1.png', success="尝试打开副本界面"+get_time())
    d.click(0.837, 0.891) # 内海
    d.click(0.193, 0.523) # 浊暗之井
    while True:
        center = compare_click('./Target/wqmt/fuben4.png', success="尝试找到乐园"+get_time())
        if center:
            d.click(0.587, 0.86) # 点击扫荡
            break
        else:
            center = compare_click('./Target/wqmt/fuben4-1.png', 
                                   threshold=0.85 , success="非乐园副本，切换页面"+get_time())
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