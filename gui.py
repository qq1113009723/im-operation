import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import configparser
import os

def load_config(config_name):
    config = configparser.ConfigParser()
    config.read(config_name)
    # 假设配置文件是键值对形式，将其转换为字典
    return {section: dict(config.items(section)) for section in config.sections()}

def execute_script(script_name, text_widget, config):
    def run_script():
        # 设置环境变量，使脚本可以读取配置
        for key, value in config.items():
            os.environ[key] = value

        process = subprocess.Popen(["python", script_name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in iter(process.stdout.readline, ''):
            text_widget.insert(tk.END, line)
            text_widget.see(tk.END)
        process.stdout.close()
        process.wait()

    thread = threading.Thread(target=run_script)
    thread.start()

def create_script_button(root, text_widget, script_name, config):
    return tk.Button(root, text=f"执行 {script_name}", command=lambda: execute_script(script_name, text_widget, config))

# 创建主窗口
root = tk.Tk()
root.title("脚本执行器")

# 创建滚动文本框用于显示日志
log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
log_text.pack(padx=10, pady=10)

# 加载配置文件
config = load_config("config/config-prepub.ini")  # 或者是其他配置文件

# 创建按钮来执行脚本
button1 = create_script_button(root, log_text, "create_accounts.py", config)
button1.pack()

button2 = create_script_button(root, log_text, "create_groups.py", config)
button2.pack()

button3 = create_script_button(root, log_text, "add_members_to_groups.py", config)
button3.pack()

# 主循环
root.mainloop()
