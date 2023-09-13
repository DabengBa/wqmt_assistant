from pywebio.input import checkbox as pw_checkbox
from ruamel.yaml import YAML
from utils.functions import *
import utils.config as cfg
import utils.log as log


def rouge():
    log.logit("开始：刷肉鸽")
    Getxy(tgt_pic="rouge00_ico").click()
    count = 1
    while True:
        log.logit(f"开始第{count}次")
        Getxy(
            tgt_pic="rouge01_entry", fail_msg="没有找到肉鸽入口，请确保已经进到有“进入探索”的界面").click()
        Getxy(tgt_pic="rouge02_nextstep").click()
        Getxy(tgt_pic="rouge03_start", timg_gap=5).click()
        scrn_ctrl().click(0.35, 0.5)
        Getxy(tgt_pic="rouge04_confirmselection", timg_gap=5).click()
        scrn_ctrl().click(0.04, 0.06)
        Getxy(tgt_pic="rouge05_termination").click()
        Getxy(tgt_pic="rouge06_quit").click()
        count += 1


def topquit():
    log.logit("开始：尝试从上方退出潜在弹窗与结算窗口")
    [scrn_ctrl().click(0.4, 0.05, timg_gap=1) for i in range(3)]
    log.logit("完成：尝试从上方退出潜在弹窗与结算窗口")


def homequit():
    while True:
        log.logit("开始：尝试从home按钮退出")
        tgt_xy = Getxy(tgt_pic="homequit", retry_enabled=False)
        if tgt_xy:
            tgt_xy.click()
            log.logit("完成：尝试从home按钮退出")
        else:
            log.logit("尝试从home按钮退出失败, 点击右下角退出潜在弹窗")
            scrn_ctrl().click(0.916, 0.935,sleep_time=2)


def wqmtstart():  # 连接设备，失败则报错
    adb.start("com.zy.wqmt.cn/com.papegames.gamelib_unity.BaseUnityImplActivity")
    sleep(12)

def panelcheck():
    log.logit("开始：检查面板")
    tgt_xy = Getxy(tgt_pic="friend1", retry_enabled=False)
    if tgt_xy:
        pass
    else:
        scrn_ctrl().click(0.683, 0.53, sleep_time=2)  # 展开面板
        log.logit("点击展开面板")
    log.logit("完成：检查面板")


def starttohome():  # 启动到home
    log.logit("开始：启动, 检查系统公告")
    if Getxy(tgt_pic="caigouban1", retry_enabled=False).coords is not None: # 看看是不是已经进入主界面了
        pass
    else:
        while True:
            if Getxy(tgt_pic="login", retry_enabled=False, threshold=0.8).coords is not None:
                Getxy(tgt_pic="login").click()
                log.logit("点击开始游戏按钮")
                break
            else:
                log.logit("没有找到开始游戏按钮，尝试启动app及检查系统公告, 等待10秒")
                wqmtstart()  # 启动无期迷途
                if Getxy(tgt_pic="start1", retry_enabled=False, success_msg="发现系统公告").coords is not None:
                    scrn_ctrl().click(0.97, 0.5)  # 点击右侧边缘退出公告
        log.logit("等待16秒-->等待游戏完全进入主页面")
        sleep(16)
        log.logit("点击右下角退出潜在弹窗")
        [scrn_ctrl().click(0.916, 0.935) for i in range(2)]

        while True:
            if Getxy(tgt_pic="fuben1", retry_enabled=False).coords is not None:
                break
            else:
                log.logit("开始：检查月卡提示")
                Getxy(
                    tgt_pic="cancell", success_msg="@@@@@@@已经取消月卡购买界面，请之后注意补充@@@@", fail_msg="").click()
                log.logit("结束：检查月卡提示")
                log.logit("点击右下角退出潜在弹窗")
                [scrn_ctrl().click(0.916, 0.935) for i in range(2)]
                log.logit("开始：检查工会战提示")
                Getxy(
                    tgt_pic="confirm", success_msg="@@@@@@@已经取消公会战提醒，请之后记得参加@@@@", fail_msg="").click()
                log.logit("结束：检查工会战提示")
                log.logit("点击右下角退出潜在弹窗")
                [scrn_ctrl().click(0.916, 0.935) for i in range(2)]
    [scrn_ctrl().click(0.916, 0.935) for i in range(2)]
    panelcheck()  # 检查面板状态，如果没有展开则展开
    log.logit("完成：启动, 检查系统公告")


def guild():
    log.logit("开始：公会收菜")
    panelcheck()
    scrn_ctrl().click(0.933, 0.365, timg_gap=3)
    log.logit("进入工会")
    [scrn_ctrl().click(0.513, 0.028, timg_gap=1) for i in range(2)]
    log.logit("开始捐赠")
    scrn_ctrl().click(0.374, 0.69, timg_gap=2)
    [scrn_ctrl().click(0.169, 0.827, timg_gap=1.5) for i in range(6)]
    log.logit("捐赠完毕")
    homequit()
    log.logit("完成：公会收菜")


def dailycheckin():
    log.logit("开始：Check-in")
    scrn_ctrl().click(0.825, 0.15, timg_gap=2)
    log.logit("尝试完成对话")
    [scrn_ctrl().click(0.807, 0.64) for i in range(10)]
    log.logit("尝试收取签到礼物")
    for i in range(2):
        scrn_ctrl().click(0.44, 0.75)
        scrn_ctrl().click(0.55, 0.77)
        scrn_ctrl().click(0.67, 0.75)
        scrn_ctrl().click(0.79, 0.76)
    log.logit("完成对话和礼物收取")
    topquit()
    log.logit("完成：Check-in")


def getmail():
    log.logit("开始：收邮件")
    scrn_ctrl().click(0.958, 0.146, timg_gap=2)
    [scrn_ctrl().click(0.263, 0.942, timg_gap=1) for i in range(4)]
    homequit()
    log.logit("完成：收邮件")


def Bureau():
    log.logit("开始：管理局领体力，派遣")
    Getxy(tgt_pic="glj1", timg_gap=3).click()

    log.logit("尝试收取体力")
    scrn_ctrl().click(0.143, 0.456, timg_gap=3)
    [Getxy(tgt_pic="lingqu", timg_gap=3, times=2).click() for i in range(2)]
    log.logit("完成收取体力")

    topquit()

    log.logit("尝试派遣")
    scrn_ctrl().click(0.44, 0.742, timg_gap=2)
    [scrn_ctrl().click(0.105, 0.707, timg_gap=3) for i in range(4)]
    log.logit("完成派遣")
    homequit()
    log.logit("完成：管理局领体力，派遣")


def friends():  # 朋友
    log.logit("开始：拜访朋友")
    panelcheck()
    Getxy(tgt_pic="friend1", timg_gap=5).click()
    [scrn_ctrl().click(0.869, 0.855, timg_gap=1) for i in range(3)]
    homequit()
    log.logit("完成：朋友拜访")


def construction():  # 基建
    log.logit("开始：基建")
    panelcheck()
    scrn_ctrl().click(0.844, 0.629, timg_gap=3)
    log.logit("开始收菜")
    [scrn_ctrl().click(0.096, 0.373, timg_gap=2) for i in range(3)]  # 收菜
    log.logit("开始聊天")
    [scrn_ctrl().click(0.074, 0.249, timg_gap=2) for i in range(2)]
    scrn_ctrl().click(0.908, 0.612)
    [scrn_ctrl().click(0.908, 0.889) for i in range(40)]
    homequit()
    log.logit("完成：基建")


def purchase():  # 采购办领免费体力
    log.logit("开始：采购办领体力")
    Getxy(tgt_pic="caigouban1", timg_gap=5).click()
    scrn_ctrl().click(0.091, 0.41, timg_gap=2)
    [scrn_ctrl().swipe(0.965, 0.578, 0.27, 0.611, timg_gap=1) for i in range(3)]
    log.logit("准备打开礼包")
    scrn_ctrl().click(0.587, 0.88, timg_gap=2)  # 收每日体力
    scrn_ctrl().click(0.766, 0.733, timg_gap=2)  # 确认
    topquit()
    homequit()
    log.logit("结束：采购办领体力")


def raidriver():  # 锈河
    log.logit("开始：锈河副本")
    Getxy(tgt_pic="fuben1", timg_gap=4, success_msg="尝试打开副本界面").click()

    log.logit("尝试切换到锈河")
    scrn_ctrl().click(0.17, 0.92, timg_gap=3)

    Getxy(tgt_pic="fuben2", timg_gap=2, success_msg="尝试打开记忆风暴").click()
    scrn_ctrl().click(0.835, 0.682, timg_gap=2)

    Getxy(tgt_pic="fubensaodang", success_msg="尝试点击连续扫荡").click()
    Getxy(tgt_pic="fubensaodangkaishi",success_msg="尝试点击开始").click()
    if Getxy(tgt_pic="done", retry_enabled=False, success_msg="尝试点击完成").coords is None:
        Getxy(tgt_pic="cancell", success_msg="次数用光，取消扫荡").click()

    topquit()
    homequit()
    log.logit("完成：锈河副本")


def raid11():  # 刷11章
    log.logit("开始：raid任务")
    Getxy(tgt_pic="fuben1", timg_gap=4, success_msg="尝试打开副本界面").click()
    scrn_ctrl().click(0.98, 0.41, timg_gap=2)  # 点击切换到右侧
    Getxy(tgt_pic="fuben3-11", timg_gap=2, success_msg="尝试打开11章").click()
    [scrn_ctrl().swipe(0.965, 0.578, 0.27, 0.611, timg_gap=1) for i in range(2)]  # 滑动屏幕
    scrn_ctrl().click(0.078, 0.541, timg_gap=2)  # 点击11-6
    Getxy(tgt_pic="fubensaodang", timg_gap=2, success_msg="尝试点击连续扫荡").click()
    [scrn_ctrl().click(0.712, 0.683) for i in range(6)]  # 点击+号
    Getxy(tgt_pic="fubensaodangkaishi", success_msg="尝试点击开始").click()
    Getxy(tgt_pic="done", timg_gap=2, success_msg="尝试点击完成").click()
    homequit()
    log.logit("结束：raid任务")


def raiddark():  ## 深井
    log.logit("开始：深井扫荡")
    Getxy(tgt_pic="fuben1", timg_gap=4, success_msg="尝试打开副本界面").click()
    scrn_ctrl().click(0.837, 0.891, timg_gap=2)  # 内海
    scrn_ctrl().click(0.193, 0.523, timg_gap=2)  # 浊暗之井
    while True:
        if Getxy(tgt_pic="fuben4", retry_enabled=False).coords is not None:
            Getxy(tgt_pic="fuben4", retry_enabled=False, timg_gap=3).click()
            scrn_ctrl().click(0.587, 0.86, timg_gap=3)  # 点击扫荡
            break
        else:
            Getxy(tgt_pic="fuben4-1", retry_enabled=False, timg_gap=3, success_msg="非乐园副本，切换页面").click()
    topquit()
    homequit()
    log.logit("完成：深井扫荡")


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


def select_jobs():
    options = [
        "启动",
        "签到",
        "公会",
        "邮件",
        "采购中心-每日免费体力",
        "基建收菜",
        "管理局",
        "好友",
        "副本-锈河记忆",
        "副本-11-6",
        "副本-深井",
    ]
    selected_options = pw_checkbox(
        "Selection", options=options, value=cfg.saved_selections
    )
    saved_selections = selected_options
    cfg.config["saved_selections"] = saved_selections
    with open(path.join(cfg.curr_dir, "config.yaml"), "w", encoding="utf-8") as f:
        yaml = YAML()
        yaml.dump(cfg.config, f)
    return selected_options
