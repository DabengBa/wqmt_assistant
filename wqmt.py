import pywebio as pw
from ruamel.yaml import YAML
from utils.functions import *
import utils.config as cfg
import utils.log as log


def rouge():
    log.logit("开始：刷肉鸽").text()
    Getxy(tgt_pic="rouge00_ico").click()
    count = 1
    while True:
        log.logit(f"开始第{count}次").text()
        Getxy(
            tgt_pic="rouge01_entry", fail_msg="没有找到肉鸽入口，请确保已经进到有“进入探索”的界面"
        ).click()
        Getxy(tgt_pic="rouge02_nextstep").click()
        Getxy(tgt_pic="rouge03_start", sleep_time=5).click()
        scrn_ctrl().click(0.35, 0.5)
        Getxy(tgt_pic="rouge04_confirmselection", sleep_time=5).click()
        scrn_ctrl().click(0.04, 0.06)
        Getxy(tgt_pic="rouge05_termination").click()
        Getxy(tgt_pic="rouge06_quit").click()
        count += 1


def topquit():
    log.logit("尝试从上方退出潜在弹窗与结算窗口").text()
    [scrn_ctrl().click(0.4, 0.05, sleep_time=1) for _ in range(3)]


def homequit():
    """
    Attempts to exit the current screen by clicking on the "home" button.
    If the button is found, it is clicked and the function completes.
    If the button is not found, the function clicks on the bottom right corner of the screen to dismiss any potential pop-up windows and lowers the image matching threshold.
    This process is repeated until the "home" button is found or the image matching threshold reaches a minimum value.
    Inputs: None
    Outputs: None
    """
    threshold = cfg.default_threshold
    max_iterations = 10
    for _ in range(max_iterations):
        log.logit("开始：尝试从home按钮退出").text()
        find_xy = Getxy(
            tgt_pic="homequit", threshold=threshold, retry_enabled=False
        )
        if find_xy.coords:
            find_xy.click()
            log.logit("完成：尝试从home按钮退出").text()
            break
        else:
            log.logit("尝试从home按钮退出失败, 点击右下角退出潜在弹窗, 并调低图片匹配要求").text()
            scrn_ctrl().click(0.916, 0.935, sleep_time=2)
            threshold -= 0.1

    find_xy = Getxy(tgt_pic="fuben1", retry_enabled=False)  # 检查一下是否真的回到了主界面
    if not find_xy.coords:
        Getxy(tgt_pic="homequit", retry_enabled=False).click()


def wqmtstart():  # 启动游戏
    app = "com.zy.wqmt.cn/com.papegames.gamelib_unity.BaseUnityImplActivity"
    config = cfg.load_config()  # 刷新cfg数值
    if config["sever_type"] == "B服":
        adb.start(app.replace("cn", "bilibili"))
    else:
        adb.start(app)
    sleep(12)


def wqmtclose():  # 关闭游戏
    app = "com.zy.wqmt.cn"
    config = cfg.load_config()  # 刷新cfg数值
    if config["sever_type"] == "B服":
        adb.close(app.replace("cn", "bilibili"))
    else:
        adb.close(app)


def panelcheck():
    log.logit("开始：检查面板展开情况").text()
    find_xy = Getxy(tgt_pic="friend1", retry_enabled=False)
    if not find_xy.coords:
        scrn_ctrl().click(0.683, 0.53, sleep_time=2)  # 展开面板
        log.logit("点击展开面板").text()
    log.logit("完成：检查面板展开情况").text()


def starttohome():  # 启动到home
    log.logit("开始：启动, 检查系统公告").text()
    find_xy = Getxy(tgt_pic="caigouban01", retry_enabled=False)
    if not find_xy.coords:
        click_start()
    [scrn_ctrl().click(0.916, 0.935) for _ in range(2)]
    panelcheck()  # 检查面板状态，如果没有展开则展开
    log.logit().img()
    log.logit("完成：启动, 检查系统公告").text()


# TODO Rename this here and in `starttohome`
def click_start():
    while True:
        find_xy = Getxy(tgt_pic="login", retry_enabled=False, threshold=0.85)
        if find_xy.coords:
            find_xy.click()
            log.logit("点击开始游戏按钮").text()
            find_xy.click()  # 尽量避免因界面卡顿失败而没有点击成功
            break
        else:
            log.logit("没有找到开始游戏按钮，尝试启动app及检查系统公告, 等待10秒").text()
            wqmtstart()  # 启动无期迷途
            find_xy = Getxy(
                tgt_pic="start1", retry_enabled=False, success_msg="发现系统公告"
            )
            if find_xy.coords:
                scrn_ctrl().click(0.97, 0.5)  # 点击右侧边缘退出公告
    log.logit("等待16秒-->等待游戏完全进入主页面").text()
    sleep(16)
    log.logit("点击右下角退出潜在弹窗").text()
    [scrn_ctrl().click(0.966, 0.965) for _ in range(2)]

    count = 1
    while True:
        count = count + 1
        find_xy = Getxy(tgt_pic="fuben1", retry_enabled=False)
        if find_xy.coords:
            break
        log.logit("开始：检查月卡提示").text()
        Getxy(
            tgt_pic="cancell",
            success_msg="@@@@已经取消月卡购买界面，请之后注意补充@@@@",
            retry_enabled=False,
            fail_msg="",
        ).click()
        log.logit("结束：检查月卡提示").text()
        [scrn_ctrl().click(0.916, 0.935) for _ in range(2)]
        log.logit("开始：检查公会战提示").text()
        Getxy(
            tgt_pic="confirm",
            success_msg="@@@@已经取消公会战提醒，请之后记得参加@@@@",
            retry_enabled=False,
            fail_msg="",
        ).click()
        log.logit("结束：检查工会战提示").text()
        [scrn_ctrl().click(0.966, 0.965) for _ in range(2)]
        if count == 5:
            homequit()


def guild():
    log.logit("开始：公会收菜").text()
    log.logit().img()
    panelcheck()
    scrn_ctrl().click(0.933, 0.365, sleep_time=3)
    log.logit("进入工会").text()
    log.logit().img()
    [scrn_ctrl().click(0.513, 0.028, sleep_time=1) for _ in range(2)]
    log.logit("开始捐赠").text()
    scrn_ctrl().click(0.374, 0.69, sleep_time=2)
    [scrn_ctrl().click(0.169, 0.827, sleep_time=1.5) for _ in range(6)]
    log.logit("捐赠完毕").text()
    log.logit().img()
    homequit()
    log.logit("完成：公会收菜").text()


def dailycheckin():
    log.logit("开始：Check-in").text()
    log.logit().img()
    scrn_ctrl().click(0.825, 0.15, sleep_time=2)
    log.logit("尝试完成对话").text()
    [scrn_ctrl().click(0.807, 0.64) for _ in range(10)]
    log.logit("尝试收取签到礼物").text()
    for _ in range(2):
        scrn_ctrl().click(0.44, 0.75)
        scrn_ctrl().click(0.55, 0.77)
        scrn_ctrl().click(0.67, 0.75)
        scrn_ctrl().click(0.79, 0.76)
    log.logit("完成对话和礼物收取").text()
    log.logit().img()
    topquit()
    log.logit("完成：Check-in").text()


def getmail():
    log.logit("开始：收邮件").text()
    log.logit().img()
    scrn_ctrl().click(0.958, 0.146, sleep_time=2)
    [scrn_ctrl().click(0.263, 0.942, sleep_time=1) for _ in range(4)]
    log.logit().img()
    homequit()
    log.logit("完成：收邮件").text()


def Bureau():
    log.logit("开始：管理局领体力，派遣").text()
    log.logit().img()
    Getxy(tgt_pic="glj1", sleep_time=3).click()

    log.logit("尝试收取体力").text()
    scrn_ctrl().click(0.143, 0.456, sleep_time=3)
    [
        Getxy(tgt_pic="lingqu", sleep_time=3, click_times=2).click()
        for _ in range(2)
    ]
    log.logit().img()
    log.logit("完成收取体力").text()

    topquit()

    log.logit("尝试派遣").text()
    scrn_ctrl().click(0.44, 0.742, sleep_time=2)
    [scrn_ctrl().click(0.105, 0.707, sleep_time=3) for _ in range(4)]
    log.logit("完成派遣").text()
    log.logit().img()
    homequit()
    log.logit("完成：管理局领体力，派遣").text()


def friends():  # 朋友
    log.logit("开始：拜访朋友").text()
    log.logit().img()
    panelcheck()
    Getxy(tgt_pic="friend1", sleep_time=5).click()
    [scrn_ctrl().click(0.869, 0.855, sleep_time=1) for _ in range(3)]
    log.logit().img()
    homequit()
    log.logit("完成：朋友拜访").text()


def construction():  # 基建
    log.logit("开始：基建").text()
    log.logit().img()
    panelcheck()
    scrn_ctrl().click(0.844, 0.629, sleep_time=3)
    log.logit("开始收菜").text()
    [scrn_ctrl().click(0.096, 0.373, sleep_time=2) for _ in range(3)]
    log.logit("开始聊天").text()
    [scrn_ctrl().click(0.074, 0.249, sleep_time=2) for _ in range(2)]
    scrn_ctrl().click(0.908, 0.612)
    [scrn_ctrl().click(0.908, 0.889) for _ in range(40)]
    log.logit().img()
    homequit()
    log.logit("完成：基建").text()


def purchase():  # 采购办领免费体力
    log.logit("开始：采购办领体力").text()
    log.logit().img()
    Getxy(tgt_pic="caigouban01", sleep_time=5).click()
    scrn_ctrl().click(0.091, 0.41, sleep_time=2)
    while True:
        [
            scrn_ctrl().swipe(0.965, 0.578, 0.27, 0.611, sleep_time=1)
            for _ in range(3)
        ]
        find_xy = Getxy(
            tgt_pic="caigouban02", sleep_time=2, retry_enabled=False
        )
        if find_xy.coords:
            log.logit("准备打开礼包").text()
            find_xy.click()
            break
    scrn_ctrl().click(0.766, 0.733, sleep_time=2)  # 确认
    # 截图，呈现
    log.logit("领取完毕").text()
    log.logit().img()
    # 退出
    topquit()
    homequit()
    log.logit("结束：采购办领体力").text()


def raidriver(raid):  # 锈河
    log.logit("开始：锈河副本").text()
    log.logit().img()
    Getxy(tgt_pic="fuben1", sleep_time=4, success_msg="尝试打开副本界面").click()
    log.logit("尝试切换到锈河").text()
    Getxy(tgt_pic="fuben_xiuhe", sleep_time=4, success_msg="尝试打开副本界面").click()

    Getxy(tgt_pic=f"fuben_{raid}", sleep_time=2, success_msg="尝试打开目标副本").click()
    scrn_ctrl().click(0.835, 0.682, sleep_time=2)

    Getxy(tgt_pic="fubensaodang", success_msg="尝试点击连续扫荡").click()
    Getxy(
        tgt_pic="fubensaodangkaishi", success_msg="尝试点击开始", sleep_time=10
    ).click()
    if (
        Getxy(tgt_pic="done", success_msg="尝试点击完成", retry_enabled=False).coords
        is None
    ):
        Getxy(tgt_pic="cancell", success_msg="次数用光，取消扫荡").click()
    log.logit().img()
    topquit()
    homequit()
    log.logit("完成：锈河副本").text()


def raid11():  # 刷11章
    log.logit("开始：raid任务").text()
    log.logit().img()
    Getxy(tgt_pic="fuben1", sleep_time=4, success_msg="尝试打开副本界面").click()
    scrn_ctrl().click(0.98, 0.41, sleep_time=2)  # 点击切换到右侧
    Getxy(tgt_pic="fuben3-11", sleep_time=2, success_msg="尝试打开11章").click()
    [
        scrn_ctrl().swipe(0.965, 0.578, 0.27, 0.611, sleep_time=1)
        for _ in range(2)
    ]
    scrn_ctrl().click(0.078, 0.541, sleep_time=2)  # 点击11-6
    Getxy(tgt_pic="fubensaodang", sleep_time=2, success_msg="尝试点击连续扫荡").click()
    [scrn_ctrl().click(0.712, 0.683) for _ in range(6)]  # 点击+号
    Getxy(tgt_pic="fubensaodangkaishi", success_msg="尝试点击开始").click()
    Getxy(tgt_pic="done", sleep_time=2, success_msg="尝试点击完成").click()
    log.logit().img()
    homequit()
    log.logit("结束：raid任务").text()


def raiddark():  ## 深井
    log.logit("开始：深井扫荡").text()
    log.logit().img()
    Getxy(tgt_pic="fuben1", sleep_time=4, success_msg="尝试打开副本界面").click()
    scrn_ctrl().click(0.837, 0.891, sleep_time=2)  # 内海
    scrn_ctrl().click(0.193, 0.523, sleep_time=2)  # 浊暗之井
    while True:
        find_xy = Getxy(tgt_pic="fuben4", retry_enabled=False, sleep_time=3)
        log.logit().img()  # TODO debug 偶尔失效问题
        if find_xy.coords:
            find_xy.click()
            Getxy(tgt_pic="fuben4", retry_enabled=False, sleep_time=3).click()
            scrn_ctrl().click(0.587, 0.86, sleep_time=3)  # 点击扫荡
            break
        else:
            Getxy(
                tgt_pic="fuben4-1",
                retry_enabled=False,
                sleep_time=3,
                success_msg="非乐园副本，切换页面",
            ).click()
    log.logit().img()
    topquit()
    homequit()
    log.logit("完成：深井扫荡").text()


def supervision():
    # TODO 每周领取数据包的任务需要测试。
    log.logit("开始：监察密令 领取奖励, 预计持续75秒").text()
    log.logit().img()
    scrn_ctrl().click(0.72, 0.78, sleep_time=2)  # 进入监察密令
    Getxy(tgt_pic="supervision01", sleep_time=1).click()  # 切换到检查任务
    find_xy = Getxy(
        tgt_pic="supervision07", sleep_time=1, retry_enabled=False
    )  # 检查每周领取数据包任务
    if find_xy.coords:
        find_xy.click()
        Getxy(
            tgt_pic="supervision08", sleep_time=1, retry_enabled=False
        ).click()
    Getxy(tgt_pic="supervision01", sleep_time=1).click()  # 切换到检查任务
    # 重复三次，领取每日、每周、密令三种奖励
    supervision_get()
    Getxy(tgt_pic="supervision_week", sleep_time=1).click()  # 切换到每周任务
    supervision_get()
    Getxy(tgt_pic="supervision_total", sleep_time=1).click()  # 切换到密令任务
    supervision_get()
    Getxy(tgt_pic="supervision03", sleep_time=1).click()  # 切换到密令
    # 领取奖励
    find_xy = Getxy(tgt_pic="supervision02", sleep_time=1, retry_enabled=False)
    if find_xy.coords:
        find_xy.click()
        # 检查是否出现了二选一
        find_xy = Getxy(
            tgt_pic="supervision06", sleep_time=1, retry_enabled=False
        )
        if find_xy.coords:
            scrn_ctrl().click(0.63, 0.71, sleep_time=2)
            Getxy(
                tgt_pic="supervision09", sleep_time=2, retry_enabled=False
            ).click()
    scrn_ctrl().click(0.916, 0.935, sleep_time=2)  # 右下角退出物品领取界面
    log.logit().img()
    homequit()
    log.logit("完成：监察密令 领取奖励").text()


def supervision_get():
    find_xy = Getxy(tgt_pic="supervision02", sleep_time=1, retry_enabled=False)
    if find_xy.coords:
        find_xy.click()
    scrn_ctrl().click(0.5, 0.8, sleep_time=1)  # 右下角退出物品领取界面


def raid_fight():
    """
    Consume stamina and obtain materials based on the selected raid.
    The options are maintained in the `select_fights` function.
    """
    fight = cfg.config["fights"]
    raid_mapping = {
        "副本-11-6": raid11,
        "狄斯币": lambda: raidriver("gold"),
        "狂厄结晶": lambda: raidriver("crystal"),
    }
    if fight in raid_mapping:
        raid_mapping[fight]()
    else:
        log.logit("没有配置目标副本, 请重新配置", shown=True)


def select_option(prompt, options, config_key):
    """
    Selects an option from a list of options and handles any exceptions that may occur during the selection process.

    Args:
        prompt (str): The prompt message to display to the user.
        options (list): The list of options to display to the user.
        config_key (str): The key to use in the configuration dictionary to store the selected option.

    Returns:
        str: The option selected by the user.
    """
    try:
        selected_option = pw.input.select(
            prompt, options=options, value=cfg.config[config_key]
        )
    except Exception as e:
        # Handle the exception here
        log.logit(f"An error occurred: {e}", shown=True)
        selected_option = cfg.config[config_key]
    log.logit(f"Selected option: {selected_option}")
    cfg.config[config_key] = selected_option
    cfg.save_config()
    return selected_option


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
        "副本-深井",
        "消耗体力刷材料",
        "监察密令",
        "肉鸽",
    ]
    selected_options = pw.input.checkbox("Selection", options=options, value=cfg.saved_selections)  # type: ignore

    cfg.config["saved_selections"] = selected_options
    cfg.save_config()
    log.logit(f"Selected option: {selected_options}")
    return selected_options


def select_sever():
    options = [
        "官服",
        "B服",
    ]
    return select_option("服务器", options, "sever_type")


def select_fights():
    options = ["无", "狄斯币", "狂厄结晶", "副本-11-6"]
    return select_option("体力消耗", options, "fights")


def select_last_action():
    options = ["无动作", "退出模拟器(未生效)", "退出无期迷途"]
    return select_option("完成后执行", options, "last_action")
