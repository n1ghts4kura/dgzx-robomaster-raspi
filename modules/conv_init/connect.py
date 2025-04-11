#基本框架直接抄的大疆开发者文档 2025.4.11:现在没抄了，基本自己写的
# -*- encoding: utf-8 -*-
import serial

class uart:

    def __init__(self):
        self.uart = serial.Serial()
        # 配置串口 波特率 115200，数据位 8 位，1 个停止位，无校验位，超时时间 0.2 秒
        self.uart.port = 'COM3'
        self.uart.baudrate = 115200
        self.uart.bytesize = serial.EIGHTBITS
        self.uart.stopbits = serial.STOPBITS_ONE
        self.uart.parity = serial.PARITY_NONE
        self.uart.timeout = 0.2
        # 打开串口
        self.uart.open()
        return self


    def conv_init(self):#握手函数
        accept=int(self.uart.readline()) #选择永久堵塞，因为你树莓派在比赛的时候毕竟是一直开着的
        if accept==1001:
            print("连接成功")
            self.uart.write(1001)
            return 
    
    def skill_accept(self):
        return int(self.uart.readline())

    def heart(self,num=1002):#心跳函数 
        #2025.4.11 P.S.因为不知道py的函数参数默认值是不是这么写所以就用c++的写了一下
        accept=self.uart.readline(2)#1.5秒超时
        if len(accept)!=0:
            self.uart.write(num)
            return 1
        else:
            print("连接丢失")
            return 0
    
    def __del__(self):
        self.uart.close()

# def connect(num):
#     conv_init()
#     while heart(num):#这个num主要是给heart函数传数据，主程序定义
#         continue

# 关闭串口
