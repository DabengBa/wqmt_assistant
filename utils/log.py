from os import path, listdir, remove
import time as time
import utils.config as cfg
from pywebio.output import put_text as pw_put_text

days_to_keep = 7
log_folder = path.join(cfg.curr_dir, 'log')

# 遍历日志文件夹中的所有文件
for filename in listdir(log_folder):
    file_dir = path.join(log_folder, filename)
    # 检查文件是否是普通文件并且是否在log文件夹中
    if path.isfile(file_dir) and filename[:4] != '.DS_':
        # 获取文件的创建时间和当前时间之间的时间差
        create_time = path.getctime(file_dir)
        current_time = time.time()
        time_diff = current_time - create_time
        days_since_created = time_diff / (24 * 60 * 60)

        # 如果文件创建时间超过7天，则删除该文件
        if days_since_created > days_to_keep:
            remove(file_dir)
            print(f"Deleted file: {filename}")


def logit(content, shown=True):
    if cfg.log_switch == 'open':
        file_dir = path.join(cfg.curr_dir, 'log', cfg.formatted_today + '.txt')
        formatted_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        with open(file_dir, 'a', encoding='utf-8') as f:  # 使用追加模式打开文件
            f.write(content + ' ' + formatted_time + '\n')
            if shown:
                pw_put_text(content + ' ' + formatted_time + '\n')