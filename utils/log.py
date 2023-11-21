from os import path, listdir, remove
import time as time
import utils.config as cfg
import utils.adb as adb
import pywebio as pw

days_to_keep = 7
log_folder = path.join(cfg.curr_dir, "log")

# 遍历日志文件夹中的所有文件
for filename in listdir(log_folder):
    file_dir = path.join(log_folder, filename)
    # 检查文件是否是普通文件并且是否在log文件夹中
    if path.isfile(file_dir) and filename[:4] != ".DS_":
        # 获取文件的创建时间和当前时间之间的时间差
        create_time = path.getctime(file_dir)
        current_time = time.time()
        time_diff = current_time - create_time
        days_since_created = time_diff / (24 * 60 * 60)

        # 如果文件创建时间超过7天，则删除该文件
        if days_since_created > days_to_keep:
            remove(file_dir)
            print(f"Deleted file: {filename}")

# 如果config.yaml中打开了日志功能，则创建一个滚动区域用来输出log
if cfg.log_switch == "open":
    pw.output.put_scrollable(
        pw.output.put_scope("log_area"), height=500, keep_bottom=True
    )
else:
    print("日志功能未打开,请查看config.yaml")


class logit:
    def __init__(self, content: str = "", shown: bool = True) -> None:
        # get
        self.content = content
        self.shown = shown
        if cfg.log_switch == "open":  # 只有在config.yaml中开启了日志输出才会执行
            # generated
            self.enabled = True
            self.file_dir = path.join(cfg.curr_dir, f"log/{cfg.formatted_today}.txt")
            self.formatted_time = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(time.time())
            )
        else:
            self.enabled = False
            return

    def text(self):
        if self.enabled:
            with open(self.file_dir, "a", encoding="utf-8") as f:  # 使用追加模式打开文件
                f.write(f"{self.content} {self.formatted_time}" + "\n")
            if self.shown:
                pw.output.put_text(
                    f"{self.content} {self.formatted_time}", scope="log_area"
                )

    def warning(self):
        if self.enabled:
            with open(self.file_dir, "a", encoding="utf-8") as f:  # 使用追加模式打开文件
                f.write(f"{self.content} {self.formatted_time}" + "\n")
        pw.output.popup("警告", self.content, size="normal")

    def toast(self):
        if self.enabled:
            with open(self.file_dir, "a", encoding="utf-8") as f:  # 使用追加模式打开文件
                f.write(f"{self.content} {self.formatted_time}" + "\n")
            if self.shown:
                pw.output.toast(
                    self.content, position="right", color="#2188ff", duration=0
                )

    def img(self):
        if self.enabled:
            adb.cap_scrn()
            pw.output.put_image(
                open(cfg.scrn_dir, "rb").read(), width="500px", scope="log_area"
            )
