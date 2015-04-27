USB调试工具<br>
用python2.7、Tkinter、pywinusb(pyusb-linux)模块开发的USB调试工具<br>
安装使用
================================================================
需要安装的模块：<br>
在Windows下:<br>
    默认是有安装Tkinter的，因此只需要安装pywinusb<br>
    可以通过pip来安装：<br>
        pip install pywinusb<br>
    或者到 https://pypi.python.org/pypi/pywinusb 下载最新版安装<br>
        python setup.py install<br>
在Ubuntu下：<br>
    默认是没有安装Tkinter的<br>
    需要先进行必要模块的安装<br>
    使用apt-get安装tk<br>
        sudo apt-get install python-tk<br>
    pyusb可以通过pip来安装：<br>
        pip install pyusb<br>
    或者到 https://pypi.python.org/pypi/pyusb 下载最新版安装<br>
        python setup.py install<br>
执行python main.py即可开始使用(ubuntu下需要使用root权限 sudo python main.py)<br>

使用技巧
================================================================
在左侧列表框，可以显示出当前连接的USB设备。<br>
可以通过双击打开设备（或者点击下面的Open打开设备）<br>
状态栏会有相应的提示信息<br>
与USB设备的通讯为64个字节<br>
16x4 在对应的位置填写对应的【十六进制】对应的数字即可，比如要发送10，应填 0A<br>
接收框会实时显示收到的数据，第一位为计数位，可以知道一共收到了几条数据<br>
点击Clear可以清楚计数和接收的数据<br>
其他待定，暂使用良好，暂未发现Bug和需要改进的地方。<br>