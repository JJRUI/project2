import tkinter as tk

from tkinter import messagebox
from PIL import Image, ImageTk
from setting import *


class KnightTourApp:
    def __init__(self, root):
        self.root = root

        self.canvas = tk.Canvas(root, width=400, height=400)

        # 加载图片
        image_pil = Image.open("./马.jpeg")
        self.image = ImageTk.PhotoImage(image_pil)
        self.knight_image = None

        # 初始化
        self.square_size = 50
        self.count = 0
        self.result = None
        self.text_list = []

        # 输入组件
        self.input_frame = tk.Frame(root)
        self.start_x_label = tk.Label(self.input_frame, text="Start X Position")
        self.start_x_entry = tk.Entry(self.input_frame, width=15)
        self.start_y_label = tk.Label(self.input_frame, text="Start Y Position")
        self.start_y_entry = tk.Entry(self.input_frame, width=15)

        # 显示组件
        self.view_frame = tk.Frame(root)
        self.now_x_position_label = tk.Label(self.view_frame, text="Now X Position")
        self.result_x_label = tk.Label(self.view_frame, text="", bg='yellow', width=10)
        self.now_y_position_label = tk.Label(self.view_frame, text="Now Y Position")
        self.result_y_label = tk.Label(self.view_frame, text="", bg='yellow', width=10)
        self.step_number_label = tk.Label(self.view_frame, text="Step Number")
        self.result_step_label = tk.Label(self.view_frame, text="", bg='yellow', width=10)

        # 操作组件
        self.control_frame = tk.Frame(root)
        self.last_button = tk.Button(self.control_frame, text="Last Step", command=self.last_step)
        self.next_button = tk.Button(self.control_frame, text="Next Step", command=self.next_step)
        self.remake_button = tk.Button(self.control_frame, text="Remake", command=self.remake)
        self.quit_button = tk.Button(root, text="Quit", command=root.destroy)

    def run(self):
        # 第一层
        self.canvas.grid(row=0, columnspan=4)

        self.draw_chessboard()  # 画制棋盘

        # 第二层
        self.input_frame.grid(row=1, rowspan=2, columnspan=4)
        self.start_x_label.grid(row=0, column=0)
        self.start_x_entry.grid(row=1, column=0)
        self.start_y_label.grid(row=0, column=1)
        self.start_y_entry.grid(row=1, column=1)

        # 第三层
        self.view_frame.grid(row=3, rowspan=2, columnspan=4)
        self.now_x_position_label.grid(row=0, column=0)
        self.result_x_label.grid(row=1, column=0)
        self.now_y_position_label.grid(row=0, column=1)
        self.result_y_label.grid(row=1, column=1)
        self.step_number_label.grid(row=0, column=2)
        self.result_step_label.grid(row=1, column=2)

        # 第四层
        self.control_frame.grid(row=5, columnspan=4)
        self.last_button.grid(row=0, column=0)
        self.remake_button.grid(row=0, column=1)
        self.next_button.grid(row=0, column=2)
        self.quit_button.grid(row=6, columnspan=4)
        self.root.mainloop()

    # 画制黑白棋盘
    def draw_chessboard(self):
        for i in range(8):
            for j in range(8):
                color = "white" if (i + j) % 2 == 0 else "black"
                self.canvas.create_rectangle(
                    j * self.square_size, i * self.square_size,
                    (j + 1) * self.square_size, (i + 1) * self.square_size,
                    fill=color
                )

    # 显示位置坐标
    def view_position(self, jude):
        if jude:
            self.count += 1
        self.result_x_label.config(text=str(self.result[self.count - 1][0] + 1))
        self.result_y_label.config(text=str(self.result[self.count - 1][1] + 1))
        self.result_step_label.config(text=str(self.count))

    # 显示步数值
    def view_step_number(self):
            text =  self.canvas.create_text(
                (self.result[self.count][0] + 0.5) * self.square_size, (self.result[self.count][1] + 0.5) * self.square_size,
                text=str(self.count + 1), fill="red")
            self.text_list.append(text)

    # 可视化骑士游走
    def visualize_knight_tour(self):
        if 0 < self.count < len(self.result):
            self.canvas.move(self.knight_image, (self.result[self.count][0] - self.result[self.count - 1][0]) * self.square_size,
                             (self.result[self.count][1] - self.result[self.count - 1][1]) * self.square_size)
            self.view_position(jude=True)
        elif self.count == 0:
            self.knight_image = self.canvas.create_image(self.result[self.count][0] * self.square_size,
                                                         self.result[self.count][1] * self.square_size, anchor=tk.NW,
                                                         image=self.image)
            self.view_position(jude=True)

    def next_step(self):
        if self.count == 0:
            start_x = self.start_x_entry.get()
            start_y = self.start_y_entry.get()

            # 输入框值是否有效的判断
            if start_x == '' or start_y == '':
                messagebox.showwarning("Warning", "Please enter the starting position.")
            elif start_x.isdigit() or start_y.isdigit():
                if int(start_x)-1 < 0 or int(start_x)-1 > 7 or int(start_y)-1 < 0 or int(start_y)-1 > 7:
                    messagebox.showwarning("Warning", "Please enter the valid position.")
                else:
                    self.result = knights_tour(int(start_x)-1, int(start_y)-1)  # 得到路径列表

                    if self.result is not None:
                        # 关闭x，y输入框
                        self.start_x_entry.config(state='disabled')
                        self.start_y_entry.config(state='disabled')

                        self.view_step_number()         # 棋盘显示步数值
                        self.visualize_knight_tour()    # 可视化骑士
                    else:
                        messagebox.showwarning("Warning", "No solution.")
            else:
                messagebox.showwarning('Warning', 'Please enter the valid position.')
        elif 0 < self.count < 64:
            self.view_step_number()
            self.visualize_knight_tour()
        else:
            messagebox.showwarning('warning', 'Knight Tour Completed.')            

    def last_step(self):
        if self.count > 1:
            self.count -= 1
            self.canvas.delete(self.text_list[self.count])
            self.text_list.pop(self.count)
            self.canvas.move(self.knight_image, (self.result[self.count - 1][0] - self.result[self.count][0]) * self.square_size,
                             (self.result[self.count - 1][1] - self.result[self.count][1]) * self.square_size)
            self.view_position(jude=False)
        else:
            messagebox.showwarning('Warning', 'No more steps.')

    def remake(self):
        # 重制变量
        self.count = 0
        self.result = []
        self.start_x_entry.config(state='normal')
        self.start_x_entry.delete(0, tk.END)
        self.start_y_entry.config(state='normal')
        self.start_y_entry.delete(0, tk.END)
        self.result_x_label.config(text='')
        self.result_y_label.config(text='')
        self.result_step_label.config(text='')
        self.canvas.delete(self.knight_image)
        for item in self.text_list:
            self.canvas.delete(item)
        self.text_list.clear()
