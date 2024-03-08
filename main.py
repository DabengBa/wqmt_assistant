from utils.functions import *
import wqmt as wq
import pywebio as pw
import utils.log as log
import utils.adb as adb

job_functions = {
    "启动": wq.starttohome,
    "签到": wq.dailycheckin,
    "公会": wq.guild,
    "邮件": wq.getmail,
    "采购中心-每日免费体力": wq.purchase,
    "基建收菜": wq.construction,
    "管理局": wq.Bureau,
    "好友": wq.friends,
    "副本-锈河记忆": lambda: wq.raidriver("storm"),
    "副本-深井": wq.raiddark,
    "消耗体力刷材料": wq.raid_fight,
    "监察密令": wq.supervision,
    "肉鸽": wq.rouge,
}


def start_options():
    while True:
        button_clicked = pw.input.actions("请选择操作", ["直接开始", "配置"])

        if button_clicked == "配置":
            wq.select_sever()
            jobs = wq.select_jobs()
            wq.select_fights()
            last_action = wq.select_last_action()

        elif button_clicked == "直接开始":
            jobs = cfg.config["saved_selections"]
            last_action = cfg.config["last_action"]

        for job in jobs:
            if job in job_functions:
                job_functions[job]()

        log.logit("完成所有任务").text()
        if "退出无期迷途" in last_action:
            wq.wqmtclose()
            log.logit("退出完成").text()


if __name__ == "__main__":
    adb.connect()
    pw.output.put_text(
        "建议按照12小时间隔，早晚各一次。晚上执行的时候请在17点之后，以便领取体力"
    )
    # pw.input.
    if cfg.log_switch == "close":
        pw.output.put_text("config.yaml中已经关闭日志输出，之后本窗口可以关闭")

    start_options()
