from subprocess import run as adb_run, DEVNULL, PIPE
import utils.functions

for _ in range(10):
    center = utils.functions.gen_ran_time(1)
    print(center)
