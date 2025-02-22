import threading
import tkinter as tk
from tkinter import scrolledtext, ttk
import sys
from openai import OpenAI
import io
from contextlib import redirect_stdout
import requests
import traceback


class EnhancedMultiLineDialog:
    def __init__(self, title="多行文本输入", default_text="", prompt="请输入内容："):
        self.root = tk.Tk()
        self.root.title(title)
        # style = ttk.Style(self.root)
        # style.theme_use('winnative')

        # 设置窗口大小和位置
        window_width = 500
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
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
            font=('Arial', 10)
        )
        self.text_area.pack(padx=10, pady=3, expand=True, fill='both')

        # 设置默认文本
        if default_text:
            self.text_area.insert("1.0", default_text)

        # 按钮框架
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=5)

        # 取消按钮
        self.cancel_button = ttk.Button(
            button_frame,
            text="取消",
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
            text="运行",
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
            font=('Arial', 10)
        )
        self.output_text.pack(padx=10, pady=1, expand=True, fill='both')

        # 绑定快捷键
        self.root.bind('<Control-Return>', lambda e: self.start_task())
        self.root.bind('<Escape>', lambda e: self.cancel())
        
    def start_task(self):
        self.progress.start(10)
        self.ok_button.config(state=tk.DISABLED, text="运行中...")
        threading.Thread(target=self.run_task, daemon=True).start()

    def run_task(self):
        self.result = self.text_area.get("1.0", tk.END).strip()
        try:
            prompt = f"{self.result}，代码必须要用这个真实的文件路径：{sys.argv[1]}，代码中要有中间结果的打印输出"
            self.show_output("提示词", prompt)
            self.root.update()
            code = self.send2ai(prompt)
            if self.show_middle_result.get():
                self.show_output("代码", code)
                self.root.update()
            output_buffer = io.StringIO()
            with redirect_stdout(output_buffer):
                exec(code, globals())
            captured_output = output_buffer.getvalue()
            self.show_output("执行成功！结果如下：", captured_output)
        except Exception as e:
            print("错误：", e)
            self.show_output("执行失败", f"{e}\n{traceback.format_exc()}")
        self.ok_button.config(state=tk.NORMAL, text="运行")
        self.progress.stop()

    def cancel(self):
        self.result = None
        self.root.quit()

    def run(self):
        self.root.mainloop()

    def show_output(self, title, msg):
        self.output_text.insert(tk.END, f"{title.center(50, '=')}\n")
        self.output_text.insert(tk.END, f"{msg}\n")
        self.output_text.see(tk.END)

    def send2ai(self, prompt):
        url = "https://aitool.center/api"
        payload = {"prompt": prompt, "model": self.model_var.get()}
        response = requests.post(url, json=payload, timeout=None)
        code = response.json()['result']
        return code

# 使用示例
if __name__ == "__main__":
    default_text = f"解压这个文件并提取里面的pdf文件到一个目录"
    dialog = EnhancedMultiLineDialog(
        title="AI工具箱",
        default_text=default_text,
        prompt="输入要求："
    )
    dialog.run()