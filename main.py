from utils.functions import *
import wqmt as wq
import pywebio as pw
import utils.log as log
import utils.adb as adb

if __name__ == "__main__":
    adb.connect()
    pw.output.put_text("建议按照12小时间隔，早晚各一次。晚上执行的时候请在17点之后，以便领取体力")
    last = ["无", "退出模拟器", "退出无期迷途"]
    selected_last = pw.input.select("结束选择", last)  # type: ignore
    # pw.input.
    if cfg.log_switch == "close":
        pw.output.put_text("config.yaml中已经关闭日志输出，之后本窗口可以关闭")
    agree = wq.select_jobs()  # type: ignore

    fight_options = ["无", "狄斯币", "狂厄结晶", "副本-11-6"]
    fight = pw.input.select("Fight", fight_options, value=["狄斯币"])  # type: ignore
    if "启动" in agree:
        wq.starttohome()
    if "签到" in agree:
        wq.dailycheckin()
    if "公会" in agree:
        wq.guild()
    if "邮件" in agree:
        wq.getmail()
    if "采购中心-每日免费体力" in agree:
        wq.purchase()
    if "基建收菜" in agree:
        wq.construction()
    if "管理局" in agree:
        wq.Bureau()
    if "好友" in agree:
        wq.friends()
    if "副本-锈河记忆" in agree:
        wq.raidriver("storm")
    if "副本-深井" in agree:
        wq.raiddark()
    if "无" not in fight:
        if "副本-11-6" in fight:
            wq.raid11()
        if "狄斯币" in fight:
            wq.raidriver("gold")
        if "狂厄结晶" in fight:
            wq.raidriver("crystal")
    if "监察密令" in agree:
        wq.supervision()
    if "肉鸽" in agree:
        wq.rouge()
    log.logit("完成所有任务").text()
    if "退出无期迷途" in selected_last:
        wq.wqmtclose()
        log.logit("退出完成").text()
