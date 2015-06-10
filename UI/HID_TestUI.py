#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
USB设备主界面
'''
__author__ = "jakey.chen"
__version__ = "v1.0"


import Tkinter as tk
import ttk
import PyTkinter as pytk
import Adaptive

g_font = Adaptive.monaco_font
g_size_dict = Adaptive.size_dict
g_default_theme = pytk.g_default_theme


class HIDTestUI(object):

    def __init__(self, master=None):
        self.root = master
        self.create_frame()

    def create_frame(self):
        '''
        新建窗口，分为上下2个部分，下半部分为状态栏
        '''
        self.frm = pytk.PyLabelFrame(self.root)
        self.frm_status = pytk.PyLabelFrame(self.root)

        self.frm.grid(row=0, column=0, sticky="wesn")
        self.frm_status.grid(row=1, column=0, sticky="wesn")

        self.create_frm()
        self.create_frm_status()

    def create_frm(self):
        '''
        上半部分窗口分为左右2个部分
        '''
        self.frm_left = pytk.PyLabelFrame(self.frm)
        self.frm_right = pytk.PyLabelFrame(self.frm)

        self.frm_left.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")
        self.frm_right.grid(row=0, column=1, padx=5, pady=5, sticky="wesn")

        self.create_frm_left()
        self.create_frm_right()

    def create_frm_left(self):
        '''
        上半部分左边窗口：
        Listbox显示连接的USB设备
        Button按钮点击连接设备
        '''
        self.frm_left_label = pytk.PyLabel(self.frm_left,
                                           text="HID Devices",
                                           font=g_font)
        self.frm_left_listbox = pytk.PyListbox(self.frm_left,
                                               height=g_size_dict[
                                                   "list_box_height"],
                                               font=g_font)
        self.frm_left_btn = pytk.PyButton(self.frm_left,
                                          text="Open",
                                          font=g_font,
                                          command=self.Toggle)

        self.frm_left_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.frm_left_listbox.grid(
            row=1, column=0, padx=5, pady=5, sticky="wesn")
        self.frm_left_btn.grid(row=2, column=0, padx=5, pady=5, sticky="wesn")

        self.frm_left_listbox.bind("<Double-Button-1>", self.Open)

    def create_frm_right(self):
        '''
        上半部分右边窗口：
        分为4个部分：
        1、Label显示和重置按钮和发送按钮
        2、Entry显示（发送的数据）
        3、Label显示和十进制选择显示和清除接收信息按钮
        4、Text显示接收到的信息
        '''
        self.frm_right_reset = pytk.PyLabelFrame(self.frm_right)
        self.frm_right_send = pytk.PyLabelFrame(self.frm_right)
        self.frm_right_clear = pytk.PyLabelFrame(self.frm_right)
        self.frm_right_receive = pytk.PyText(self.frm_right,
                                             width=50,
                                             height=20,
                                             font=("Monaco", 9))

        self.frm_right_reset.grid(row=0, column=0, padx=1, sticky="wesn")
        self.frm_right_send.grid(row=1, column=0, padx=1, sticky="wesn")
        self.frm_right_clear.grid(row=2, column=0, padx=1, sticky="wesn")
        self.frm_right_receive.grid(row=3, column=0, padx=1, sticky="wesn")

        self.frm_right_receive.tag_config("green", foreground="#228B22")

        self.create_frm_right_reset()
        self.create_frm_right_send()
        self.create_frm_right_clear()

    def create_frm_right_reset(self):
        '''
        1、Label显示和重置按钮和发送按钮
        '''
        self.frm_right_reset_label = pytk.PyLabel(self.frm_right_reset,
                                                  text="Hex Bytes" + " " *
                                                  g_size_dict[
                                                      "reset_label_width"],
                                                  font=g_font)
        self.frm_right_reset_btn = pytk.PyButton(self.frm_right_reset,
                                                 text="Reset",
                                                 width=10,
                                                 font=g_font,
                                                 command=self.Reset)
        self.frm_right_send_btn = pytk.PyButton(self.frm_right_reset,
                                                text="Send",
                                                width=10,
                                                font=g_font,
                                                command=self.Send)

        self.frm_right_reset_label.grid(row=0, column=0, sticky="w")
        self.frm_right_reset_btn.grid(
            row=0, column=1, padx=5, pady=5, sticky="wesn")
        self.frm_right_send_btn.grid(
            row=0, column=2, padx=5, pady=5, sticky="wesn")

    def create_frm_right_send(self):
        '''
        2、Entry显示（发送的数据）用64个Entry来显示
        '''
        self.entry_list = list()
        for i in range(64):
            temp_str = tk.StringVar()
            temp_entry = pytk.PyEntry(self.frm_right_send,
                                      textvariable=temp_str,
                                      width=3,
                                      fg="#1E90FF",
                                      font=g_font)
            temp_str.set("00")
            temp_entry.grid(row=i//16, column=i %
                            16, padx=1, pady=1, sticky="wesn")
            self.entry_list.append(temp_str)

    def create_frm_right_clear(self):
        '''
        3、Label显示和清除接收信息按钮
        '''
        self.checkValue = tk.IntVar()
        self.frm_right_clear_label = pytk.PyLabel(self.frm_right_clear,
                                                  text="Data Received" + " " *
                                                  g_size_dict[
                                                      "clear_label_width"],
                                                  font=g_font)
        self.frm_right_decimal_checkbtn = pytk.PyCheckbutton(self.frm_right_clear,
                                                             text="Decimal",
                                                             variable=self.checkValue,
                                                             relief="flat",
                                                             font=g_font)
        self.frm_right_clear_btn = pytk.PyButton(self.frm_right_clear,
                                                 text="Clear",
                                                 width=10,
                                                 font=g_font,
                                                 command=self.Clear)

        self.frm_right_clear_label.grid(
            row=0, column=0, padx=5, pady=5, sticky="w")
        self.frm_right_decimal_checkbtn.grid(
            row=0, column=1, padx=5, pady=5, sticky="wesn")
        self.frm_right_clear_btn.grid(
            row=0, column=2, padx=5, pady=5, sticky="wesn")

    def create_frm_status(self):
        '''
        下半部分状态栏窗口
        '''
        self.frm_status_label = pytk.PyLabel(self.frm_status,
                                             text="Ready",
                                             font=g_font)
        self.frm_status_label.grid(
            row=0, column=0, padx=5, pady=5, sticky="wesn")

    def Toggle(self):
        pass

    def Open(self, event):
        pass

    def Reset(self):
        for entry in self.entry_list:
            entry.set("00")

    def Send(self):
        pass

    def Clear(self):
        self.frm_right_receive.delete("0.0", "end")


if __name__ == '__main__':
    '''
    main loop
    '''
    root = tk.Tk()
    root.title("HID-Test")
    HIDTestUI(master=root)
    root.resizable(False, False)
    root.mainloop()
