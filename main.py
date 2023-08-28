from pywebio.input import *
from pywebio.output import *
import yaml
from utils import *
from wqmt import *

with open('config.yaml', 'r', encoding='utf-8') as f:
  config = yaml.safe_load(f)

def select_jobs():
    options = ['启动', '签到', '公会','邮件','采购中心-每日免费体力','基建收菜','管理局','好友','副本-锈河记忆','副本-11-6','副本-深井']
    default_value = config['default_options']
    selected_options = checkbox("Selection", options=options, value=default_value)
    config['default_options'] = selected_options
    with open('config.yaml', 'w') as f:
        yaml.dump(config, f)
    return selected_options

if __name__ == '__main__':
    [put_text(" ") for i in range(5)]
    put_text("请提前在Config.yaml中配置好mumu的ip地址和端口")
    put_text("建议按照12小时间隔，早晚各一次。晚上执行的时候请在17点之后，以便领取体力")
    put_text("请在游戏进入界面执行程序，就是有“点击开始”的哪个页面")

    options = ['早一次', '晚一次', '自选']
    selected_options = actions("嗯……", options)
    if "早一次" in selected_options:
        morning()
    if "晚一次" in selected_options:
        night()
    if "自选" in selected_options:
        agree = select_jobs()
        if "启动" in agree:
            starttohome()
        if "签到" in agree:
            dailycheckin()
        if "公会" in agree:
            guild()
        if "邮件" in agree:
            getmail()
        if "采购中心-每日免费体力" in agree:
            purchase()
        if "基建收菜" in agree:
            construction()
        if "管理局" in agree:
            Bureau()
        if "好友" in agree:
            friends()
        if "副本-锈河记忆" in agree:
            raidriver()
        if "副本-11-6" in agree:
            raid11()
        if "副本-深井" in agree:
            raiddark()

"""     starttohome()
    dailycheckin()
    guild()
    getmail()
    purchase()
    construction()
    raidriver()
    raid11()
    raiddark()
    Bureau()
    friends() """