#! /usr/bin/env python
# -*- coding: utf-8 -*-

import platform

g_systemName = platform.system()
g_systemInfo = platform.platform()
g_pyVersion = platform.python_version()
size_dict = dict()

# System will be Linux and python == 2.7
if g_systemName == "Linux" and g_pyVersion[:3] == "2.7":
    if "Ubuntu" in g_systemInfo:
        size_dict = {
                        "list_box_height": 23,
                        "reset_label_width": 24,
                        "clear_label_width": 22
                    }

    # raspberry pi
    elif "armv61" in g_systemInfo:
        size_dict = {}

# font
monaco_font = ('Monaco', 12)
