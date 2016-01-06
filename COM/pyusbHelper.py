#! /usr/bin/env python
# -*- coding: utf-8 -*-

import usb.util
import usb.core


class pyusbHelper(object):

    def __init__(self, vid=0x1391, pid=0x2111):
        self.alive = False
        self.handle = None
        self.size = 64
        self.vid = vid
        self.pid = pid

    def start(self):
        try:
            self.dev = usb.core.find(idVendor=self.vid, idProduct=self.pid)
            if self.dev != None:
                self.ep_in = self.dev[0][(0, 0)][0].bEndpointAddress
                self.ep_out = self.dev[0][(0, 0)][1].bEndpointAddress
                self.size = self.dev[0][(0, 0)][1].wMaxPacketSize
            self.open()
            self.alive = True
            return True
        except Exception as e:
            self.alive = False
            return False

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
                    if self.dev.is_kernel_driver_active(0):
                        self.handle.detachKernelDriver(0)
                    self.handle.claimInterface(0)

    def read(self, size=64, timeout=0):
        if size >= self.size:
            self.size = size

        if self.handle:
            data = self.handle.interruptRead(self.ep_in, self.size, timeout)

        try:
            data_list = data.tolist()
            return data_list
        except Exception as e:
            return list()

    def write(self, send_list, timeout=2500):
        if self.handle:
            bytes_num = self.handle.interruptWrite(
                self.ep_out, send_list, timeout)
            return bytes_num
        return 0

if __name__ == '__main__':
    import time
    dev = UsbHelper()
    if dev.start():
        send_list = [0xAA for i in range(64)]
        dev.write(send_list)
        time.sleep(1)
        while True:
            try:
                mylist = dev.read()
                print mylist
                if mylist == []:
                    continue
                if mylist[1] == 0x02:
                    break
            except Exception as e:
                print(e)
                dev.stop()
                break
        dev.stop()
