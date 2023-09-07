from os import path, listdir, remove
import time
import utils.config as cfg

days_to_keep = 7
log_folder = path.join(cfg.main_path, 'log')
for filename in listdir(log_folder):  
    file_path = path.join(log_folder, filename)  
    # 检查文件是否是普通文件并且是否在log文件夹中  
    if path.isfile(file_path) and filename[:4] != '.DS_':  
        # 获取文件的创建时间和当前时间之间的时间差  
        create_time = path.getctime(file_path)
        current_time = time.time()
        time_diff = current_time - create_time
        days_since_created = time_diff / (24 * 60 * 60) 
          
        # 如果文件创建时间超过7天，则删除该文件  
        if days_since_created > days_to_keep:  
            remove(file_path)  
            print(f"Deleted file: {filename}")

def write_log(content):
    file_path = path.join(cfg.main_path, 'log', cfg.formatted_today + '.txt') 
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    with open(file_path, 'a', encoding='utf-8') as f:  # 使用追加模式打开文件  
        f.write(content + ' ' + formatted_time + '\n')

# 使用示例  
write_log("需要记录的内容2")