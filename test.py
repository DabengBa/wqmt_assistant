from utils.functions import *
import wqmt as wq
from pywebio.input import actions as pw_actions
from pywebio.output import put_text as pw_put_text
import utils.log as log
import utils.adb as adb


adb.connect()
scrn_ctrl().click(0.4, 0.05, sleep_time=1.0)