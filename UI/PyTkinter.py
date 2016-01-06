#! /usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk

g_default_theme = "dark"
# g_default_theme = "default"

class PyButton(tk.Button):
    '''
    Button
    '''
    def __init__(self, master, theme=g_default_theme, **kw):
        self.theme = theme
        self.kw = kw
        self.temp = dict()
        self.choose_theme()
        tk.Button.__init__(self, master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "activebackground": "#00B2EE",
                                "activeforeground": "#E0EEEE",
                                "bg": "#008B8B",
                                "fg": "#FFFFFF"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

        for key,value in self.kw.items():
            self.temp[key] = value


class PyLabel(tk.Label):
    '''
    Label
    '''
    def __init__(self, master, theme=g_default_theme, **kw):
        self.theme = theme
        self.kw = kw
        self.temp = dict()
        self.choose_theme()
        tk.Label.__init__(self, master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#E0EEEE"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

        for key,value in self.kw.items():
            self.temp[key] = value

            
class PyFrame(tk.Frame):
    '''
    Frame
    '''
    def __init__(self, master, theme=g_default_theme, **kw):
        self.theme = theme
        self.kw = kw
        self.temp = dict()
        self.choose_theme()
        tk.Frame.__init__(self, master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

        for key,value in self.kw.items():
            self.temp[key] = value


class PyLabelFrame(tk.LabelFrame):
    '''
    LabelFrame
    '''
    def __init__(self, master, theme=g_default_theme, **kw):
        self.theme = theme
        self.kw = kw
        self.temp = dict()
        self.choose_theme()
        tk.LabelFrame.__init__(self, master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#1E90FF"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value
        
        for key,value in self.kw.items():
            self.temp[key] = value

class PyListbox(tk.Listbox):
    '''
    Listbox
    '''
    def __init__(self, master, theme=g_default_theme, **kw):
        self.theme = theme
        self.kw = kw
        self.temp = dict()
        self.choose_theme()
        tk.Listbox.__init__(self, master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#1E90FF",
                                "selectbackground": "#00B2EE"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

        for key,value in self.kw.items():
            self.temp[key] = value
            

class PyText(tk.Text):
    '''
    Text
    '''
    def __init__(self, master, theme=g_default_theme, **kw):
        self.theme = theme
        self.kw = kw
        self.temp = dict()
        self.choose_theme()
        tk.Text.__init__(self, master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#1E90FF"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

        for key,value in self.kw.items():
            self.temp[key] = value


class PyCheckbutton(tk.Checkbutton):
    '''
    Checkbutton
    '''
    def __init__(self, master, theme=g_default_theme, **kw):
        self.theme = theme
        self.kw = kw
        self.temp = dict()
        self.choose_theme()
        tk.Checkbutton.__init__(self, master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#FFFFFF",
                                "activebackground": "#292929",
                                "activeforeground": "#FFFFFF",
                                "selectcolor": "#292929"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

        for key,value in self.kw.items():
            self.temp[key] = value
            

class PyEntry(tk.Entry):
    '''
    Entry
    '''
    def __init__(self, master, theme=g_default_theme, **kw):
        self.theme = theme
        self.kw = kw
        self.temp = dict()
        self.choose_theme()
        tk.Entry.__init__(self, master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#E0EEEE",
                                "insertbackground": "red"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value   

        for key,value in self.kw.items():
            self.temp[key] = value       

class PyRadiobutton(tk.Radiobutton):
    '''
    Radiobutton
    '''
    def __init__(self, master, theme=g_default_theme, **kw):
        self.theme = theme
        self.kw = kw
        self.temp = dict()
        self.choose_theme()
        tk.Radiobutton.__init__(self, master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#FFFFFF",
                                "activebackground": "#292929",
                                "activeforeground": "#FFFFFF",
                                "selectcolor": "#292929"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

        for key,value in self.kw.items():
            self.temp[key] = value
