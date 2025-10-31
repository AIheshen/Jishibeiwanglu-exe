import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
import sys


class TopNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 记事本便签")
        self.root.geometry("500x620")
        self.root.attributes("-topmost", True)
        self.root.resizable(True, True)

        # 透明度控制
        self.transparency = 1.0
        self.root.attributes('-alpha', self.transparency)

        # 字体定义
        self.default_font = ("Microsoft YaHei", 12)
        self.small_font = ("Microsoft YaHei", 10)

        # 初始化变量
        self.mode = "note"
        self.filename = None
        self.memo_data = []
        self.note_content = ""
        self.select_mode = False

        # 控件引用
        self.entry = None
        self.select_btn = None
        self.del_selected_btn = None
        self.task_frame = None
        self.text = None
        self.stats_label = None  # ✅ 新增统计标签引用

        # 加载备忘录长期记忆
        self.memo_file = "memo_data.json"
        self.load_memo_data()

        # 创建菜单
        self.create_menu()
        self.root.config(menu=self.menu_bar)

        # 创建记事本模式界面
        self.create_note_mode()

        # 绑定退出事件保存备忘录
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_memo_data(self):
        """加载备忘录数据"""
        if os.path.exists(self.memo_file):
            try:
                with open(self.memo_file, "r", encoding="utf-8") as f:
                    self.memo_data = json.load(f)
            except Exception:
                self.memo_data = []

    def save_memo_data(self):
        """保存备忘录数据"""
        with open(self.memo_file, "w", encoding="utf-8") as f:
            json.dump(self.memo_data, f, ensure_ascii=False, indent=2)

    def on_close(self):
        """关闭窗口时保存备忘录"""
        self.save_memo_data()
        self.root.destroy()

    def create_menu(self):
        """创建菜单栏"""
        self.menu_bar = tk.Menu(self.root)

        # 文件菜单
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="新建 (Ctrl+N)", command=self.new_file)
        self.file_menu.add_command(label="打开 (Ctrl+O)", command=self.open_file)
        self.file_menu.add_command(label="保存 (Ctrl+S)", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="退出", command=self.root.quit)
        self.menu_bar.add_cascade(label="文件", menu=self.file_menu)

        # 模式菜单
        self.mode_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.mode_menu.add_command(label="📝 记事本模式", command=lambda: self.switch_mode("note"))
        self.mode_menu.add_command(label="✅ 横线备忘录模式", command=lambda: self.switch_mode("memo"))
        self.menu_bar.add_cascade(label="模式", menu=self.mode_menu)

        # 透明度菜单
        self.transparency_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.transparency_menu.add_command(label="🔧 透明度调节面板", command=self.show_transparency_panel)
        self.transparency_menu.add_separator()
        self.transparency_menu.add_command(label="💎 完全不透明 (100%)", command=lambda: self.set_transparency(1.0))
        self.transparency_menu.add_command(label="☁️  90% 透明", command=lambda: self.set_transparency(0.90))
        self.transparency_menu.add_command(label="🌫️  80% 透明", command=lambda: self.set_transparency(0.80))
        self.transparency_menu.add_command(label="🎭  70% 透明", command=lambda: self.set_transparency(0.70))
        self.transparency_menu.add_command(label="👻  60% 透明", command=lambda: self.set_transparency(0.60))
        self.transparency_menu.add_command(label="💨  50% 透明", command=lambda: self.set_transparency(0.50))
        self.transparency_menu.add_command(label="🫧  40% 透明", command=lambda: self.set_transparency(0.40))
        self.transparency_menu.add_command(label="🌸  30% 透明", command=lambda: self.set_transparency(0.30))
        self.menu_bar.add_cascade(label="透明度", menu=self.transparency_menu)

        # 窗口菜单
        self.window_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.window_menu.add_command(label="🖥️ 全屏/退出全屏 (F11)", command=self.toggle_fullscreen)
        self.window_menu.add_command(label="📐 恢复默认大小", command=self.restore_size)
        self.menu_bar.add_cascade(label="窗口", menu=self.window_menu)

        # 置顶菜单
        self.top_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.top_menu.add_command(label="🔒 取消置顶", command=self.toggle_topmost)
        self.menu_bar.add_cascade(label="置顶", menu=self.top_menu)

    def set_transparency(self, value):
        self.transparency = value
        self.root.attributes('-alpha', value)
        messagebox.showinfo("透明度设置", f"透明度已调整为：{int(value * 100)}%")

    def show_transparency_panel(self):
        panel = tk.Toplevel(self.root)
        panel.title("🎚️ 透明度调节")
        panel.geometry("300x150")
        panel.transient(self.root)
        panel.grab_set()
        panel.attributes('-topmost', True)

        title = tk.Label(panel, text="🎚️ 透明度调节面板", font=("Microsoft YaHei", 14, "bold"),
                         bg="#e8f4fd", fg="#2196f3")
        title.pack(pady=10)

        slider_frame = tk.Frame(panel, bg="#fafafa")
        slider_frame.pack(pady=10, padx=20, fill=tk.X)

        tk.Label(slider_frame, text="透明度：", font=self.default_font, bg="#fafafa").pack(anchor=tk.W)

        slider = tk.Scale(slider_frame, from_=0.3, to=1.0, resolution=0.05,
                          orient=tk.HORIZONTAL, font=self.small_font,
                          bg="#fafafa", highlightthickness=0,
                          command=lambda v: (self.root.attributes('-alpha', float(v)),
                                             label.config(text=f"{int(float(v) * 100)}%")),
                          length=200)
        slider.set(self.transparency)
        slider.pack(pady=10)

        label = tk.Label(slider_frame, text=f"{int(self.transparency * 100)}%",
                         font=("Microsoft YaHei", 16, "bold"),
                         bg="#fafafa", fg="#4caf50")
        label.pack()

        btn_frame = tk.Frame(panel, bg="#fafafa")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="✅ 应用", command=lambda: panel.destroy(),
                  font=self.small_font, bg="#c8e6c9", fg="#2e7d32").pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="🔄 重置(100%)",
                  command=lambda: (self.root.attributes('-alpha', 1.0), panel.destroy()),
                  font=self.small_font, bg="#fff3e0", fg="#ef6c00").pack(side=tk.LEFT, padx=10)

    def toggle_fullscreen(self):
        current = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current)
        if not current:
            self.root.attributes('-topmost', False)

    def restore_size(self):
        self.root.attributes('-fullscreen', False)
        self.root.geometry("500x620")
        self.root.attributes('-topmost', True)

    def switch_mode(self, mode):
        if mode == self.mode:
            return
        if self.mode == "note" and self.text:
            self.note_content = self.text.get("1.0", tk.END).strip()
        elif self.mode == "memo":
            self.memo_data = self.collect_tasks()
            self.save_memo_data()

        # 清空所有子控件
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Menu):
                widget.destroy()

        self.mode = mode
        if mode == "note":
            self.create_note_mode()
        else:
            self.create_memo_mode()

    def create_note_mode(self):
        title_frame = tk.Frame(self.root, bg="#e8f4fd", relief="ridge", bd=1)
        title_frame.pack(fill=tk.X, pady=(5, 0))
        tk.Label(title_frame, text="📝 记事本模式", font=("Microsoft YaHei", 14, "bold"),
                 bg="#e8f4fd", fg="#2196f3", pady=8).pack()

        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        self.text = tk.Text(frame, wrap=tk.WORD, font=self.default_font,
                            bg="#fafcff", relief="flat", padx=10, pady=10,
                            insertbackground="#2196f3", selectbackground="#bbdefb")
        self.text.pack(fill=tk.BOTH, expand=True)

        if self.note_content:
            self.text.insert(tk.END, self.note_content)

    def create_memo_mode(self):
        """✅ 完美布局：任务列表 → 按钮 → 提示"""
        title_frame = tk.Frame(self.root, bg="#e8f5e8", relief="ridge", bd=1)
        title_frame.pack(fill=tk.X, pady=(5, 0))
        tk.Label(title_frame, text="✅ 横线备忘录模式", font=("Microsoft YaHei", 14, "bold"),
                 bg="#e8f5e8", fg="#4caf50", pady=8).pack()

        # 主容器
        main_container = tk.Frame(self.root, padx=10, pady=10)
        main_container.pack(fill=tk.BOTH, expand=True)

        # 1. 输入区域
        input_frame = tk.Frame(main_container, relief="groove", bd=1, bg="#f1f8e9")
        input_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(input_frame, text="➕ 新增任务:", font=self.small_font,
                 bg="#f1f8e9", fg="#689f38").pack(side=tk.LEFT, padx=10, pady=8)

        self.entry = tk.Entry(input_frame, font=self.default_font, relief="solid", bd=1,
                              bg="#ffffff", insertbackground="#4caf50")
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=8)
        self.entry.bind("<Return>", lambda e: self.add_task())

        add_btn = tk.Button(input_frame, text="添加任务 🚀", command=self.add_task,
                            font=self.small_font, bg="#c8e6c9", fg="#2e7d32",
                            relief="raised", bd=2, padx=15, pady=6)
        add_btn.pack(side=tk.RIGHT, padx=10, pady=8)

        # 2. 任务列表容器
        tasks_container = tk.Frame(main_container)
        tasks_container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.task_frame = tk.Frame(tasks_container, relief="sunken", bd=1, bg="#f8f9fa")
        self.task_frame.pack(fill=tk.BOTH, expand=True)

        # 3. 控制按钮（右下角）
        buttons_frame = tk.Frame(main_container)
        buttons_frame.pack(fill=tk.X, pady=(0, 5))

        button_container = tk.Frame(buttons_frame)
        button_container.pack(anchor=tk.E, padx=10)

        self.select_btn = tk.Button(button_container, text="选择",
                                    command=self.toggle_select_mode,
                                    font=self.small_font, bg="#fff3e0", fg="#ef6c00")
        self.select_btn.pack(side=tk.RIGHT, padx=(0, 5))

        self.del_selected_btn = tk.Button(button_container, text="删除",
                                          command=self.delete_selected,
                                          state=tk.DISABLED,
                                          font=self.small_font, bg="#ffcdd2", fg="#c62828")
        self.del_selected_btn.pack(side=tk.RIGHT)

        # 4. 黄色提示（最底部）
        hint_frame = tk.Frame(main_container, bg="#fff8e8", relief="groove", bd=1)
        hint_frame.pack(fill=tk.X, pady=(0, 0))
        hint = tk.Label(hint_frame,
                        text="💡 右键任务可单独删除 | 完成任务自动变灰 | 最多500条 | F11全屏 | 透明度菜单调节",
                        font=("Microsoft YaHei", 9), fg="#f57c00", bg="#fff8e8")
        hint.pack(pady=8)

        # 渲染任务
        self.render_tasks()

    def render_tasks(self):
        """✅ 修复：正确清空+统计"""
        if not self.task_frame:
            return

        # 清空任务列表
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        # 渲染任务项
        for i, task in enumerate(self.memo_data):
            task_item = tk.Frame(self.task_frame, relief="ridge", bd=1)
            task_item.pack(fill=tk.X, padx=5, pady=2)

            var_done = tk.BooleanVar(value=task["done"])
            cb_done = tk.Checkbutton(
                task_item,
                text=f"  {task['text']}",
                variable=var_done,
                font=self.default_font,
                anchor='w',
                justify='left',
                padx=15,
                pady=8,
                command=lambda idx=i, v=var_done: self.toggle_task(idx, v),
                bg="#e8f5e8" if not task["done"] else "#f5f5f5",
                selectcolor="#c8e6c9" if not task["done"] else "#e0e0e0"
            )
            cb_done.pack(side=tk.LEFT, fill=tk.X, expand=True)

            if task["done"]:
                cb_done.config(fg="#9e9e9e", relief="sunken")

            cb_done.bind("<Button-3>", lambda e, idx=i: self.confirm_delete(idx))

            if self.select_mode:
                var_sel = tk.BooleanVar(value=False)
                sel_container = tk.Frame(task_item)
                sel_container.pack(side=tk.RIGHT, padx=5, pady=5)
                sel_box = tk.Checkbutton(sel_container, variable=var_sel, bg="white",
                                         selectcolor="#fff3e0")
                sel_box.pack()
                task["selected"] = var_sel
            else:
                task.pop("selected", None)

        # ✅ 添加统计信息
        stats_frame = tk.Frame(self.task_frame, bg="#f8f9fa")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)

        stats_text = f"📊 总计: {len(self.memo_data)} 条 | "
        done_count = sum(1 for t in self.memo_data if t["done"])
        stats_text += f"已完成: {done_count} 条"

        self.stats_label = tk.Label(stats_frame, text=stats_text,
                                    font=("Microsoft YaHei", 9), fg="#757575", bg="#f8f9fa")
        self.stats_label.pack()

    def add_task(self):
        task_text = self.entry.get().strip()
        if not task_text:
            return
        if len(self.memo_data) >= 500:
            messagebox.showwarning("超出限制", "任务已达 500 条上限！\n请先清理旧任务 🗑️")
            return
        self.memo_data.insert(0, {"text": task_text, "done": False})
        self.entry.delete(0, tk.END)
        self.render_tasks()
        self.save_memo_data()

    def toggle_task(self, index, var):
        self.memo_data[index]["done"] = var.get()
        self.render_tasks()
        self.save_memo_data()

    def confirm_delete(self, index):
        task_text = self.memo_data[index]["text"]
        if messagebox.askyesno("🗑️ 确认删除", f"确定删除任务吗？\n\n『{task_text}』"):
            self.memo_data.pop(index)
            self.render_tasks()
            self.save_memo_data()

    def toggle_select_mode(self):
        self.select_mode = not self.select_mode
        if self.select_mode:
            self.select_btn.config(text="退出", bg="#ffebee")
            self.del_selected_btn.config(state=tk.NORMAL)
        else:
            self.select_btn.config(text="选择", bg="#fff3e0")
            self.del_selected_btn.config(state=tk.DISABLED)
        self.render_tasks()

    def delete_selected(self):
        to_delete = [i for i, t in enumerate(self.memo_data)
                     if t.get("selected") and t["selected"].get()]
        if not to_delete:
            messagebox.showinfo("提示", "⚠️ 未选择任何任务！")
            return
        if messagebox.askyesno("🗑️ 确认删除", f"确定删除 {len(to_delete)} 个选中的任务？"):
            for i in reversed(to_delete):
                del self.memo_data[i]
            self.render_tasks()
            self.save_memo_data()

    def collect_tasks(self):
        return [{"text": t["text"], "done": t["done"]} for t in self.memo_data]

    def new_file(self):
        if messagebox.askyesno("🆕 新建文件", "是否清空当前内容？"):
            if self.mode == "note":
                if self.text:
                    self.text.delete("1.0", tk.END)
                self.note_content = ""
            else:
                self.memo_data = []
                self.render_tasks()
                self.save_memo_data()
            self.filename = None

    def open_file(self):
        filetypes = [("所有文件", "*.*"), ("文本文件", "*.txt"), ("备忘录文件", "*.json")]
        path = filedialog.askopenfilename(filetypes=filetypes, title="📂 打开文件")
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            try:
                data = json.loads(content)
                if isinstance(data, list) and all(
                        isinstance(item, dict) and "text" in item and "done" in item for item in data):
                    if messagebox.askyesno("导入备忘录", "检测到备忘录格式内容，是否导入为备忘录？"):
                        if messagebox.askyesno("添加方式", "是否在原内容基础上增加？"):
                            self.memo_data = data + self.memo_data
                        else:
                            if messagebox.askyesno("删除原有", "是否删除原有所有任务？"):
                                self.memo_data = data
                            else:
                                self.switch_mode("note")
                                if self.text:
                                    self.text.delete("1.0", tk.END)
                                    self.text.insert(tk.END, content)
                                return
                        self.switch_mode("memo")
                        self.save_memo_data()
                    else:
                        self.switch_mode("note")
                        if self.text:
                            self.text.delete("1.0", tk.END)
                            self.text.insert(tk.END, content)
                        return
                else:
                    raise ValueError("Not memo format")
            except (ValueError, json.JSONDecodeError):
                self.switch_mode("note")
                if self.text:
                    self.text.delete("1.0", tk.END)
                    self.text.insert(tk.END, content)

            self.filename = path
            messagebox.showinfo("✅ 打开成功", f"文件已加载：\n{os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("❌ 打开失败", f"无法打开文件：\n{str(e)}")

    def save_file(self):
        if not self.filename:
            filetypes = [("文本文件", "*.txt"), ("备忘录文件", "*.json")]
            self.filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=filetypes,
                title="💾 保存文件"
            )
            if not self.filename:
                return
        try:
            if self.mode == "note":
                if self.text:
                    content = self.text.get("1.0", tk.END)
                    with open(self.filename, "w", encoding="utf-8") as f:
                        f.write(content)
            else:
                data = self.collect_tasks()
                with open(self.filename, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("✅ 保存成功", f"文件已保存到：\n{self.filename}")
        except Exception as e:
            messagebox.showerror("❌ 保存失败", f"保存失败：\n{str(e)}")

    def toggle_topmost(self):
        current = self.root.attributes("-topmost")
        self.root.attributes("-topmost", not current)
        label = "🔓 恢复置顶" if not current else "🔒 取消置顶"
        self.top_menu.entryconfig(0, label=label)


# 终极图标加载
def setup_icon(root):
    import sys, os
    def try_load_icon(icon_path):
        try:
            root.iconbitmap(icon_path)
            print(f"✓ 图标加载成功: {icon_path}")
            return True
        except:
            return False

    if not getattr(sys, 'frozen', False):
        for icon_name in ['notepad.ico']:
            if os.path.exists(icon_name) and try_load_icon(icon_name):
                return
    else:
        temp_dir = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
        for icon_name in ['notepad.ico']:
            icon_path = os.path.join(temp_dir, icon_name)
            if try_load_icon(icon_path):
                return


if __name__ == "__main__":
    root = tk.Tk()
    setup_icon(root)
    app = TopNotepad(root)
    root.bind('<F11>', lambda e: app.toggle_fullscreen())
    root.mainloop()