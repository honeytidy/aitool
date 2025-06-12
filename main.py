import threading
import tkinter as tk
from tkinter import scrolledtext, ttk
import sys
from openai import OpenAI
import io
from contextlib import redirect_stdout
import requests
import traceback
import PyPDF2
import moviepy
from tkinter import font
import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem as item
from ctypes import windll
import os
windll.shcore.SetProcessDpiAwareness(1)

class EnhancedMultiLineDialog:
    def __init__(self, title="多行文本输入", default_text="", prompt="请输入内容："):
        self.root = tk.Tk()
        self.root.title(title)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width  = int(screen_width  * 0.60)   # 60 %
        window_height = int(screen_height * 0.70)   # 70 %
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 提示标签
        self.label = tk.Label(self.root, text=prompt)
        self.label.pack(padx=10, pady=5)

        # 创建多行文本框
        self.text_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=50,
            height=5,
            font=('Microsoft YaHei UI', 9)
        )
        self.text_area.pack(padx=10, pady=3, expand=True, fill='both')
        if default_text:
            self.text_area.insert("1.0", default_text)

        # 按钮框架
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=5)

        # 取消按钮
        self.cancel_button = ttk.Button(
            button_frame,
            text="取消(Esc)",
            command=self.cancel
        )
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        # 清空按钮
        self.clear_button = ttk.Button(
            button_frame,
            text="清空",
            command=lambda: self.text_area.delete("1.0", tk.END)
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # 确定按钮
        self.ok_button = ttk.Button(
            button_frame,
            text="运行(Ctrl+Enter)",
            command=self.start_task
        )
        self.ok_button.pack(side=tk.LEFT, padx=5)

        status_frame = ttk.Frame(self.root)
        status_frame.pack(padx=5, fill='x', expand=True)
        # 进度条
        self.progress = ttk.Progressbar(status_frame, mode="indeterminate")
        self.progress.pack(padx=5, expand=True, fill='x', side=tk.LEFT)
        # 模型选择
        self.model_var = tk.StringVar(value="fast")
        self.fast_model = ttk.Radiobutton(status_frame, text="快模型", variable=self.model_var, value="fast")
        self.slow_model = ttk.Radiobutton(status_frame, text="慢模型", variable=self.model_var, value="slow")
        self.fast_model.pack(side=tk.LEFT, padx=5)
        self.slow_model.pack(side=tk.LEFT, padx=5)

        # 复选框（默认选中）
        self.show_middle_result = tk.BooleanVar(value=False)
        self.check_box = ttk.Checkbutton(status_frame, text="输出中间结果", variable=self.show_middle_result)
        self.check_box.pack(padx=5, pady=5, side=tk.LEFT, expand=True, fill='x')

        # 创建多行文本框
        self.output_text = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=50,
            height=20,
            font=('Microsoft YaHei UI', 9)
        )
        self.output_text.pack(padx=10, pady=1, expand=True, fill='both')

        # 绑定快捷键
        self.root.bind('<Control-Return>', lambda e: self.start_task())
        self.root.bind('<Escape>', lambda e: self.cancel())
        self.text_area.bind('<Control-Return>', lambda e: (self.start_task() or "break"))
        
        # 初始化托盘功能
        self.setup_tray()
        
    def setup_tray(self):
        """设置系统托盘"""
        # 创建托盘图标
        def resource_path(rel_path: str) -> str:
            """兼容 PyInstaller — 返回打包后资源的真实路径"""
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, rel_path)
            return os.path.join(os.path.abspath("."), rel_path)
        image = Image.open(resource_path("aitool.ico"))

        
        # 创建托盘菜单
        menu = (
            item('显示窗口', self.show_window, default=True),
            item('退出', self.quit_app)
        )
        
        self.tray_icon = pystray.Icon("AI工具箱", image, menu=menu)
        
        # 绑定窗口关闭事件到最小化到托盘
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        
    def show_window(self, icon=None, item=None):
        """显示窗口"""
        self.root.after(0, self._show_window)
        
    def _show_window(self):
        """在主线程中显示窗口"""
        self.root.deiconify()
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after_idle(lambda: self.root.attributes("-topmost", False))
        
    def hide_window(self, icon=None, item=None):
        """隐藏窗口到托盘"""
        self.root.withdraw()
        if not hasattr(self, '_tray_started'):
            self._tray_started = True
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
            
    def quit_app(self, icon=None, item=None):
        """退出应用"""
        self.tray_icon.stop()
        self.root.quit()
        
    def start_task(self):
        self.progress.start(10)
        self.ok_button.config(state=tk.DISABLED, text="运行中...")
        threading.Thread(target=self.run_task, daemon=True).start()

    def run_task(self):
        self.result = self.text_area.get("1.0", tk.END).strip()
        try:
            prompt = f"{self.result}"
            if len(sys.argv) > 2:
                prompt = f"{self.result}，代码必须要用这个真实的文件路径：{sys.argv[1]}"
            self.show_output("提示词", prompt)
            self.root.update()
            code = self.send2ai(prompt)
            self.show_output("开始运行任务", "运行中...")
            self.root.update()
            if self.show_middle_result.get():
                self.show_output("代码", code)
                self.root.update()
            output_buffer = io.StringIO()
            with redirect_stdout(output_buffer):
                exec(code, globals())
            captured_output = output_buffer.getvalue()
            self.show_output("执行成功，结果：", captured_output)
        except Exception as e:
            print("错误：", e)
            self.show_output("执行失败", f"{e}\n{traceback.format_exc()}")
        self.ok_button.config(state=tk.NORMAL, text="运行(Ctrl+Enter)")
        self.progress.stop()

    def cancel(self):
        self.result = None
        self.root.quit()

    def run(self):
        # 置顶窗口
        # self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.mainloop()

    def show_output(self, title, msg):
        self.output_text.tag_config("bold_red", foreground="red")
        self.output_text.insert(tk.END, f"{title.center(50, '=')}\n", "bold_red")
        self.output_text.tag_config("highlight", background="white")
        self.output_text.insert(tk.END, f"{msg}\n")
        self.output_text.see(tk.END)
        # self.output_text.config(state="disabled")

    def send2ai(self, prompt):
        url = "https://aitool.center/api"
        payload = {"prompt": prompt, "model": self.model_var.get()}
        response = requests.post(url, json=payload, timeout=None)
        code = response.json()['result']
        return code

# 使用示例
if __name__ == "__main__":
    # close_splash.py
    try:
        import pyi_splash
        pyi_splash.close()
    except ImportError:
        pass
    default_text = f"在D盘创建一个文件夹，文件夹名称为：test，并生成一个txt文件，文件内容为：hello world，完成后用文件浏览器打开D盘"
    dialog = EnhancedMultiLineDialog(
        title="AI工具箱",
        default_text=default_text,
        prompt="输入要求："
    )
    dialog.run()