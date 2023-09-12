# Py
import random as rd

# Pip
from subprocess import run as adb_run, DEVNULL, PIPE


# Private
import utils.config as cfg

def touch(x, y, xx=0, yy=0):
    if xx != 0:
        duration= rd.randint(150, 250)
        adb_run([cfg.adb_dir, "-s", cfg.device_name, "shell", "input", "swipe", str(x), str(y), str(xx), str(yy), str(duration)])
    else:
        adb_run([cfg.adb_dir, "-s", cfg.device_name, "shell", "input", "tap", str(x), str(y)])

def cap_scrn():
    adb_run(
        [cfg.adb_dir, "-s", cfg.device_name, "shell", "screencap", cfg.remote_dir],
        stdout=DEVNULL,
        stderr=DEVNULL,
    )
    adb_run(
        [cfg.adb_dir, "-s", cfg.device_name, "pull", cfg.remote_dir, cfg.scrn_dir],
        stdout=DEVNULL,
        stderr=DEVNULL,
    )