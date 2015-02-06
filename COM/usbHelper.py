#! /usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import usb.util
import usb.core

class UsbHelper(object):
    def __init__(self, vid=0x1391, pid=0x2111):
        self.alive = False
        self.handle = None
        self.vid = vid
        self.pid = pid

    def SetStopEvent(self):
        self.alive = False
        self.stop()

    def start(self):
        try:
            self.dev = usb.core.find(idVendor=self.vid, idProduct=self.pid)
            if self.dev != None:
                self.ep_in = self.dev[0][(0,0)][0].bEndpointAddress
                self.ep_out = self.dev[0][(0,0)][1].bEndpointAddress
                self.size = self.dev[0][(0,0)][1].wMaxPacketSize
            self.open()
            self.alive = True
        except Exception as e:
            self.alive = False

    def stop(self):
        self.alive = False
        if self.handle:
            self.handle.releaseInterface()

    def open(self):
        busses = usb.busses()
        for bus in busses:
            devices = bus.devices
            for device in devices:
                if device.idVendor == self.vid and device.idProduct == self.pid:
                    self.handle = device.open()
                    # Attempt to remove other drivers using this device.
                    if self.dev.is_kernel_driver_active(0):
                        try:
                            self.handle.detachKernelDriver(0)
                        except Exception as e:
                            self.alive = False
                    try:
                        self.handle.claimInterface(0)
                    except Exception as e:
                        self.alive = False

    def read(self, size=64, timeout=50):
        if size >= self.size:
            self.size = size

        if self.handle:
            data = self.handle.interruptRead(self.ep_in, self.size, timeout)
            return data.tolist()

    def write(self, send_list, timeout=50):
        if self.handle:
            bytes_num = self.handle.interruptWrite(self.ep_out, send_list, timeout)
            return bytes_num

if __name__ == '__main__':
    import time
    dev = UsbHelper()

    dev.start()

    send_list = [0xAA for i in range(64)]
    dev.write(send_list)
    # time.sleep(0.25)
    while True: 
        try:
            mylist = dev.read()
            print mylist
            if mylist[1] == 0x02: 
                break
        except:
            dev.stop()
            break
    dev.stop()