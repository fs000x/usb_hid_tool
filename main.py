#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import Tkinter as tk
import threading
import datetime

import usb.core

from UI import HID_TestUI
from COM import usbHelper

class MainUSBToolUI(HID_TestUI.HIDTestUI):
    def __init__(self, master=None):
        super(MainUSBToolUI, self).__init__()
        self.list_box_pyusb = list()
        self.usbDev = None
        self.vid = 0x1391
        self.pid = 0x2111
        self.receive_data = list()
        self.find_all_devices()

    def __del__(self):
        time.sleep(1)
        if self.usbDev:
            try:
                self.usbDev.stop()
            except:
                pass

    def find_all_devices(self):
        try:
            self.temp_pyusb = list()
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
                    index = list(self.frm_left_listbox.get(0, self.frm_left_listbox.size())).index(item)
                    self.frm_left_listbox.delete(index)
            self.list_box_pyusb = self.temp_pyusb

            self.thread_find_all_devices = threading.Thread(target=self.find_all_devices)
            self.thread_find_all_devices.setDaemon(True)
            self.thread_find_all_devices.start()
        except:
            pass

    def fill_zero(self, strHex, strLen=4):
        if len(strHex) > strLen:
            strHex = strHex[0:strLen]
        elif len(strHex) < strLen:
            strHex = (strLen-len(strHex))*"0" + strHex
        return strHex.upper()

    def Toggle(self):
        if self.frm_left_btn["text"] == "Open":
            try:
                try:
                    self.currentStrUsb = self.frm_left_listbox.get(self.frm_left_listbox.curselection())
                except:
                    self.frm_status_label["text"] = "Please select device first!"
                    return

                self.vid = int(self.currentStrUsb[4:8], 16)
                self.pid = int(self.currentStrUsb[13:17], 16)

                self.usbDev = usbHelper.UsbHelper(self.vid, self.pid)
                self.usbDev.start()
                if self.usbDev.alive:
                    self.frm_status_label["text"] = "Open Device [{0}] Successful!".format(self.currentStrUsb)
                    self.frm_status_label["fg"] = "#66CD00"
                    self.frm_left_btn["text"] = "Close"
                    self.frm_left_btn["bg"] = "#F08080"

                    self.thread_read = threading.Thread(target=self.UsbRead)
                    self.thread_read.setDaemon(True)
                    self.thread_read.start()
            except Exception as e:
                print e
        elif self.frm_left_btn["text"] == "Close":
            try:
                self.usbDev.stop()
            except:
                pass
            self.frm_left_btn["text"] = "Open"
            self.frm_left_btn["bg"] = "#008B8B"
            self.frm_status_label["text"] = "Close USB Device Successful!"
            self.frm_status_label["fg"] = "#8DEEEE"

    def Send(self):
        send_list = self.GetSendList()
        if self.usbDev:
            try:
                if self.usbDev.alive:
                    self.usbDev.write(send_list)
            except Exception as e:
                self.frm_right_receive.insert("end", str(e) + "\n")

    def GetSendList(self):
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
        temp_string = ""
        if strFormat == "str": 
            for index,item in enumerate(receive_list):
                if (index+1)%16 == 0:
                    temp_string += "\n"
                else:
                    item = self.fill_zero(hex(item)[2:], strLen=2)
                    temp_string += "%-5s"%item
            return temp_string
        else:
            for index,item in enumerate(receive_list):
                if (index+1)%16 == 0:
                    temp_string += "\n"
                else:
                    item = self.fill_zero(str(item), strLen=3)
                    temp_string += "%-5s"%item
            return temp_string

    def UsbRead(self):
        while self.usbDev.alive:
            try:
                temp_list = self.usbDev.read()
                # self.receive_data.append(temp_list)

                if self.checkValue.get() == 0:
                    temp_string = self.ListStringFormat(temp_list)
                else:
                    temp_string = self.ListStringFormat(temp_list, lineNum=16, strFormat="int")
                self.frm_right_receive.insert("end", "[" + str(datetime.datetime.now()) + "]:\n", "green")
                self.frm_right_receive.insert("end", temp_string)
                self.frm_right_receive.see("end")
                # self.receive_data[0:]
            except Exception as e:
                pass


if __name__ == '__main__':
    '''
    main loop
    '''
    root = tk.Tk()
    root.title("HID-Test")
    MainUSBToolUI(master=root)
    root.resizable(False, False)
    root.mainloop()