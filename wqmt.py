from pywebio.input import checkbox as pw_checkbox
from ruamel.yaml import YAML
from utils.functions import *
import utils.config as cfg
import utils.log as log


def rouge():
    log.logit("开始：刷肉鸽")
    comp_tap(tgt_pic="rouge000_ico")
    count = 1
    while True:
        log.logit(f"开始第{count}次")
        comp_tap(
            tgt_pic="rouge001_entry", fail="没有找到肉鸽入口，请确保已经进到有“进入探索”的界面")
        comp_tap(tgt_pic="rouge002_nextstep")
        comp_tap(tgt_pic="rouge003_start", sleep_time=5)
        click_screen(0.35, 0.5)
        comp_tap(tgt_pic="rouge004_confirmselection", sleep_time=5)
        click_screen(0.04, 0.06)
        comp_tap(tgt_pic="rouge005_termination", times=2)
        comp_tap(tgt_pic="rouge006_quit")
        count += 1


def topquit():
    log.logit("开始：尝试从上方退出潜在弹窗与结算窗口")
    [click_screen(0.4, 0.06, sleep_time=1) for i in range(3)]
    log.logit("完成：尝试从上方退出潜在弹窗与结算窗口")


def homequit():
    log.logit("开始：尝试从home按钮退出")
    center = comp_tap(tgt_pic="homequit", sleep_time=5, success="已点击返回home", fail="", retry_wait=0.5)
    if center:
        log.logit("完成：尝试从home按钮退出")
    else:
        log.logit("尝试从home按钮退出失败, 点击右下角退出潜在弹窗")
        click_screen(0.916, 0.935)
        comp_tap(tgt_pic="homequit", sleep_time=5, success="已点击返回home", fail="", retry=False)


def wqmtstart():  # 连接设备，失败则报错
    adb_run(
        [
            cfg.adb_dir,
            "-s",
            cfg.device_name,
            "shell",
            "am",
            "start",
            "-n",
            "com.zy.wqmt.cn/com.papegames.gamelib_unity.BaseUnityImplActivity",
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
    sleep(12)


def panelcheck():
    log.logit("开始：检查面板")
    if comp_pic_xy(tgt_pic="friend1", fail="检测到面板未展开，尝试点击展开面板", retry=False):
        pass
    else:
        click_screen(0.683, 0.53, sleep_time=2)  # 展开面板
        log.logit("点击展开面板")
    log.logit("完成：检查面板")


def starttohome():  # 启动到home
    log.logit("开始：启动, 检查系统公告")
    if comp_pic_xy(tgt_pic="caigouban1", threshold=0.95, retry=False):  # 看看是不是已经进入主界面了
        pass
    else:
        while True:
            center = comp_tap(tgt_pic="login")
            if center:
                log.logit("点击开始游戏按钮")
                break
            else:
                log.logit("没有找到开始游戏按钮，尝试启动app及检查系统公告, 等待10秒")
                wqmtstart()  # 启动无期迷途
                center = comp_pic_xy(tgt_pic="start1", success="发现系统公告", retry=False)
                if center:
                    click_screen(0.97, 0.5)  # 点击右侧边缘退出公告
        log.logit("等待16秒-->等待游戏完全进入主页面")
        sleep(16)
        log.logit("点击右下角退出潜在弹窗")
        [click_screen(0.916, 0.935) for i in range(2)]

        while True:
            center = comp_pic_xy(tgt_pic="fuben1", retry=False)
            if center:
                break
            else:
                log.logit("开始：检查月卡提示")
                comp_tap(
                    tgt_pic="cancell", success="@@@@@@@已经取消月卡购买界面，请之后注意补充@@@@", fail="", retry=False
                )
                log.logit("结束：检查月卡提示")
                log.logit("点击右下角退出潜在弹窗")
                [click_screen(0.916, 0.935) for i in range(2)]
                log.logit("开始：检查工会战提示")
                comp_tap(
                    tgt_pic="confirm", success="@@@@@@@已经取消公会战提醒，请之后记得参加@@@@", fail="", retry=False
                )
                log.logit("结束：检查工会战提示")
                log.logit("点击右下角退出潜在弹窗")
                [click_screen(0.916, 0.935) for i in range(2)]
    [click_screen(0.916, 0.935) for i in range(2)]
    panelcheck()  # 检查面板状态，如果没有展开则展开
    adb_cap_scrn()
    log.logit("完成：启动, 检查系统公告")


def guild():
    log.logit("开始：公会收菜")
    panelcheck()
    click_screen(0.933, 0.365, sleep_time=3)
    log.logit("进入工会")
    adb_cap_scrn()
    [click_screen(0.513, 0.028, sleep_time=1) for i in range(2)]
    log.logit("开始捐赠")
    click_screen(0.374, 0.69, sleep_time=2)
    [click_screen(0.169, 0.827, sleep_time=1.5) for i in range(6)]
    log.logit("捐赠完毕")
    homequit()
    log.logit("完成：公会收菜")


def dailycheckin():
    log.logit("开始：Check-in")
    adb_cap_scrn()
    click_screen(0.825, 0.15, sleep_time=2)
    log.logit("尝试完成对话")
    [click_screen(0.807, 0.64) for i in range(10)]
    log.logit("尝试收取签到礼物")
    for i in range(2):
        click_screen(0.44, 0.75)
        click_screen(0.55, 0.77)
        click_screen(0.67, 0.75)
        click_screen(0.79, 0.76)
    log.logit("完成对话和礼物收取")
    adb_cap_scrn()
    topquit()
    adb_cap_scrn()
    log.logit("完成：Check-in")


def getmail():
    log.logit("开始：收邮件")
    adb_cap_scrn()
    click_screen(0.958, 0.146, sleep_time=2)
    [click_screen(0.263, 0.942, sleep_time=1) for i in range(4)]
    homequit()
    adb_cap_scrn()
    log.logit("完成：收邮件")


def Bureau():
    log.logit("开始：管理局领体力，派遣")
    comp_tap(tgt_pic="glj1", sleep_time=3)

    log.logit("尝试收取体力")
    click_screen(0.143, 0.456, sleep_time=3)
    [comp_tap(tgt_pic="lingqu", sleep_time=3, times=2) for i in range(2)]

    adb_cap_scrn()
    log.logit("完成收取体力")

    topquit()

    log.logit("尝试派遣")
    click_screen(0.44, 0.742, sleep_time=2)
    [click_screen(0.105, 0.707, sleep_time=3) for i in range(4)]
    log.logit("完成派遣")
    homequit()
    log.logit("完成：管理局领体力，派遣")


def friends():  # 朋友
    log.logit("开始：拜访朋友")
    panelcheck()
    comp_tap(tgt_pic="friend1", sleep_time=5)
    [click_screen(0.869, 0.855, sleep_time=1) for i in range(3)]
    homequit()
    log.logit("完成：朋友拜访")


def construction():  # 基建
    log.logit("开始：基建")
    panelcheck()
    click_screen(0.844, 0.629, sleep_time=3)
    log.logit("开始收菜")
    [click_screen(0.096, 0.373, sleep_time=2) for i in range(3)]  # 收菜
    log.logit("开始聊天")
    [click_screen(0.074, 0.249, sleep_time=2) for i in range(2)]
    click_screen(0.908, 0.612)
    [click_screen(0.908, 0.889) for i in range(40)]
    homequit()
    log.logit("完成：基建")


def purchase():  # 采购办领免费体力
    log.logit("开始：采购办领体力")
    comp_tap(tgt_pic="caigouban1", sleep_time=5)
    click_screen(0.091, 0.41, sleep_time=2)
    [swipe_screen(0.965, 0.578, 0.27, 0.611, sleep_time=1) for i in range(3)]
    log.logit("准备打开礼包")
    adb_cap_scrn()
    click_screen(0.587, 0.88, sleep_time=2)  # 收每日体力
    click_screen(0.766, 0.733, sleep_time=2)  # 确认
    adb_cap_scrn()
    topquit()
    homequit()
    log.logit("结束：采购办领体力")


def raidriver():  # 锈河
    log.logit("开始：锈河副本")
    comp_tap(tgt_pic="fuben1", sleep_time=4, success="尝试打开副本界面")

    log.logit("尝试切换到锈河")
    click_screen(0.17, 0.92, sleep_time=3)

    comp_tap(tgt_pic="fuben2", sleep_time=2, success="尝试打开记忆风暴")
    click_screen(0.835, 0.682, sleep_time=2)

    comp_tap(tgt_pic="fubensaodang", success="尝试点击连续扫荡")
    comp_tap(tgt_pic="fubensaodangkaishi",success="尝试点击开始")
    center = comp_tap(tgt_pic="done", success="尝试点击完成")

    if center is None:
        comp_tap(tgt_pic="cancell", success="次数用光，取消扫荡")

    topquit()
    homequit()
    log.logit("完成：锈河副本")


def raid11():  # 刷11章
    log.logit("开始：raid任务")
    comp_tap(tgt_pic="fuben1", sleep_time=4, success="尝试打开副本界面")
    click_screen(0.98, 0.41, sleep_time=2)  # 点击切换到右侧
    comp_tap(tgt_pic="fuben3-11", sleep_time=2, success="尝试打开11章")
    [swipe_screen(0.965, 0.578, 0.27, 0.611, sleep_time=1) for i in range(2)]  # 滑动屏幕
    click_screen(0.078, 0.541, sleep_time=2)  # 点击11-6
    comp_tap(tgt_pic="fubensaodang", sleep_time=2, success="尝试点击连续扫荡")
    [click_screen(0.712, 0.683) for i in range(6)]  # 点击+号
    comp_tap(tgt_pic="fubensaodangkaishi", success="尝试点击开始")
    comp_tap(tgt_pic="done", sleep_time=2, success="尝试点击完成")
    homequit()
    log.logit("结束：raid任务")


def raiddark():  ## 深井
    log.logit("开始：深井扫荡")
    comp_tap(tgt_pic="fuben1", sleep_time=4, success="尝试打开副本界面")
    click_screen(0.837, 0.891, sleep_time=2)  # 内海
    click_screen(0.193, 0.523, sleep_time=2)  # 浊暗之井
    while True:
        center = comp_tap(tgt_pic="fuben4", sleep_time=2, success="尝试找到乐园")
        if center:
            click_screen(0.587, 0.86, sleep_time=3)  # 点击扫荡
            break
        else:
            center = comp_tap(
                tgt_pic="fuben4-1", threshold=0.85, sleep_time=3, success="非乐园副本，切换页面"
            )
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
