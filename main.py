#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
界面逻辑
'''
__author__ = "jakey.chen"
__version__ = "v1.0"

import time
import Tkinter as tk
import threading
import datetime
import platform
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

# 根据系统 引用不同的usb库
if platform.system() == "Windows":
    import pywinusb.hid as hid
    from COM import hidHelper
else:
    import usb.core
    from COM import usbHelper

from UI import HID_TestUI


class MainUSBToolUI(HID_TestUI.HIDTestUI):

    def __init__(self, master=None):
        super(MainUSBToolUI, self).__init__()
        self.list_box_pyusb = list()
        self.receive_count = 0
        self.usbDev = None
        self.vid = None
        self.pid = None
        self.find_all_devices()

    def __del__(self):
        logging.error("__del__")
        if self.usbDev:
            try:
                self.usbDev.stop()
            except:
                logging.error(e)

    def find_all_devices(self):
        '''
        线程检测USB的连接状态
        '''
        try:
            self.temp_pyusb = list()
            if platform.system() == "Windows":
                usb_dev = hid.find_all_hid_devices()
                for dev in usb_dev:
                    vid = self.fill_zero(hex(dev.vendor_id)[2:])
                    pid = self.fill_zero(hex(dev.product_id)[2:])
                    dev_info = "VID:{0} PID:{1}".format(vid, pid)
                    self.temp_pyusb.append(dev_info)
            else:
                usb_dev = usb.core.find(find_all=True)
                for dev in usb_dev:
                    vid = self.fill_zero(hex(dev.idVendor)[2:])
                    pid = self.fill_zero(hex(dev.idProduct)[2:])
                    dev_info = "VID:{0} PID:{1}".format(vid, pid)
                    self.temp_pyusb.append(dev_info)
            for item in self.temp_pyusb:
                if item not in self.list_box_pyusb:
                    self.frm_left_listbox.insert("end", item)
            for item in self.list_box_pyusb:
                if item not in self.temp_pyusb:
                    index = list(
                        self.frm_left_listbox.get(0, self.frm_left_listbox.size())).index(item)
                    self.frm_left_listbox.delete(index)
            # 检测到usb设备被拔出时，关闭usb设备
            if self.pid and self.vid:
                _vid = self.fill_zero(hex(self.vid)[2:])
                _pid = self.fill_zero(hex(self.pid)[2:])
                dev_info = "VID:{0} PID:{1}".format(_vid, _pid)
                if dev_info not in self.temp_pyusb:
                    self.Toggle()
                    self.vid = None
                    self.pid = None
            self.list_box_pyusb = self.temp_pyusb

            self.thread_find_all_devices = threading.Timer(
                1, self.find_all_devices)
            self.thread_find_all_devices.setDaemon(True)
            self.thread_find_all_devices.start()
        except:
            logging.error(e)

    def fill_zero(self, strHex, strLen=4):
        '''
        为了美观，将不足位用0填充
        '''
        if len(strHex) > strLen:
            strHex = strHex[0:strLen]
        elif len(strHex) < strLen:
            strHex = (strLen-len(strHex))*"0" + strHex
        return strHex.upper()

    def Toggle(self):
        '''
        打开/关闭 usb设备
        '''
        if self.frm_left_btn["text"] == "Open":
            try:
                try:
                    self.currentStrUsb = self.frm_left_listbox.get(
                        self.frm_left_listbox.curselection())
                except:
                    self.frm_status_label[
                        "text"] = "Please select device first!"
                    return

                self.vid = int(self.currentStrUsb[4:8], 16)
                self.pid = int(self.currentStrUsb[13:17], 16)

                if platform.system() == "Windows":
                    self.usbDev = hidHelper.hidHelper(self.vid, self.pid)
                    self.usbDev.start()
                    if self.usbDev.device:
                        self.usbDev.device.set_raw_data_handler(
                            self.HidUsbRead)
                else:
                    self.usbDev = usbHelper.usbHelper(self.vid, self.pid)
                    self.usbDev.start()
                    if self.usbDev.alive:
                        self.thread_read = threading.Thread(
                            target=self.UsbRead)
                        self.thread_read.setDaemon(True)
                        self.thread_read.start()
                if self.usbDev.alive:
                    self.frm_status_label["text"] = "Open Device [{0}] Successful!".format(
                        self.currentStrUsb)
                    self.frm_status_label["fg"] = "#66CD00"
                    self.frm_left_btn["text"] = "Close"
                    self.frm_left_btn["bg"] = "#F08080"
            except Exception as e:
                logging.error(e)
        elif self.frm_left_btn["text"] == "Close":
            try:
                self.usbDev.stop()
            except:
                logging.error(e)
            self.frm_left_btn["text"] = "Open"
            self.frm_left_btn["bg"] = "#008B8B"
            self.frm_status_label["text"] = "Close USB Device Successful!"
            self.frm_status_label["fg"] = "#8DEEEE"

    def Open(self, event):
        '''
        双击Listbox事件
        '''
        self.Toggle()

    def Send(self):
        '''
        发送数据
        '''
        send_list = self.GetSendList()
        if self.usbDev:
            try:
                if self.usbDev.alive:
                    if platform.system() == "Windows":
                        send_list.insert(0, 0x00)
                    self.usbDev.write(send_list)
            except Exception as e:
                self.frm_right_receive.insert("end", str(e) + "\n")

    def Clear(self):
        '''
        清除接收记录
        '''
        self.frm_right_receive.delete("0.0", "end")
        self.receive_count = 0

    def GetSendList(self):
        '''
        获取64个entry的数据组成发送的列表
        '''
        send_list = list()
        temp_list = list()
        for entry in self.entry_list:
            temp_list.append(entry.get())
        for i in temp_list:
            try:
                temp_value = int(i, 16)
            except:
                temp_value = 0
            send_list.append(temp_value)
        if len(send_list) == 64:
            return send_list
        else:
            return [0 for i in range(64)]

    def ListStringFormat(self, receive_list, lineNum=16, strFormat="str"):
        '''
        格式化接收数据，按照自己想要的格式输出
        '''
        temp_string = ""
        if strFormat == "str":
            for index, item in enumerate(receive_list):
                item = self.fill_zero(hex(item)[2:], strLen=2)
                temp_string += "%-5s" % item
                if (index+1) % 16 == 0:
                    temp_string += "\n"
            return temp_string
        else:
            for index, item in enumerate(receive_list):
                item = self.fill_zero(str(item), strLen=3)
                temp_string += "%-5s" % item
                if (index+1) % 16 == 0:
                    temp_string += "\n"
            return temp_string

    def HidUsbRead(self, data):
        '''
        回调事件，接收数据
        '''
        try:
            temp_list = data[1:]
            self.receive_count += 1

            if self.checkValue.get() == 0:
                temp_string = self.ListStringFormat(temp_list)
            else:
                temp_string = self.ListStringFormat(
                    temp_list, lineNum=16, strFormat="int")
            self.frm_right_receive.insert("end", "[" + str(datetime.datetime.now()) +
                                          " - " + str(self.receive_count) + "]:\n", "green")
            self.frm_right_receive.insert("end", temp_string)
            self.frm_right_receive.see("end")
        except Exception as e:
            logging.error(e)

    def UsbRead(self):
        '''
        线程检测是否有数据可读
        '''
        while self.usbDev.alive:
            try:
                temp_list = self.usbDev.read()
                self.receive_count += 1

                if self.checkValue.get() == 0:
                    temp_string = self.ListStringFormat(temp_list)
                else:
                    temp_string = self.ListStringFormat(
                        temp_list, lineNum=16, strFormat="int")
                self.frm_right_receive.insert("end", "[" + str(datetime.datetime.now()) +
                                              " - " + str(self.receive_count) + "]:\n", "green")
                self.frm_right_receive.insert("end", temp_string)
                self.frm_right_receive.see("end")
            except Exception as e:
                self.usbDev.stop()
                self.usbDev = None
                logging.error(e)


if __name__ == '__main__':
    '''
    main loop
    '''
    root = tk.Tk()
    root.title("HID-Test")
    MainUSBToolUI(master=root)
    root.resizable(False, False)
    root.mainloop()
