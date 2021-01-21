#-*-coding:utf-8-*-
import time
from numba import jit

import os

import _thread



class APN():
    """ APNdata """

    def __init__(self):
        self.default = 1800
        self.is_loop = True
        self.is_finish = False
        self.tmpname = 'tmpfile.txt'
        self.savename = 'spent.txt'
        

def tcpdump_data(name):
    full = 'adb shell "ifconfig |grep ' + name + '"'
    print(full)

    while True:
        while os.system(full) != 0:
            time.sleep(0.1)
        else:
            os.popen('adb root')
            localtime = time.asctime(time.localtime(time.time()))
            now = time.strftime("%Y-%m-%d-%H_%M_%S",
                                time.localtime(time.time()))
            savefile = now + '.cap'
            path = '/sdcard/' + name + '/' + savefile
            cmd = 'adb shell ' + '"tcpdump -c 65535 -i ' + name + ' -w ' + path + '"'
            os.popen(cmd)

            while os.system(full) == 0:
                time.sleep(0.1)


def reboot(apn):
    print(os.popen("adb root").read())
    print(os.popen("adb remount").read())

    try:
        if os.path.exists(apn.tmpname):
            os.remove(apn.tmpname)
    except Exception:
        pass

    os.popen('adb logcat | find "NetworkPing" >' + apn.tmpname)

    while os.path.exists(apn.tmpname) is not True:
        time.sleep(1)


    # 判断请求是否都成功
    while apn.is_loop:
        with open(apn.tmpname, 'r') as f:
            for line in f.readlines():
                if line.find('ping end')>=0:
                    apn.is_finish = True
                    apn.default = 180

        time.sleep(1)



    #保存数据
    with open(apn.tmpname, 'r') as f:
        spentfile = open(apn.savename, 'a', encoding='utf-8')
        for line in f.readlines():
            spentfile.writelines(line)

    print("output finished")


                
def expired(apn):

    is_expired = 0
    while True:
        time.sleep(1)
        is_expired = is_expired + 1
        print("is_expired: " +str(is_expired))
        if is_expired >= apn.default:
            apn.is_loop = False
            break
    
    print('expired success')


while True:

    apn = APN()

    is_loop = True
    is_finish = False
    # 创建线程 两个socket成功连接，则三分钟后重启，否则最大超时时间为1800秒
    try:
        _thread.start_new_thread(expired, (apn,))
    except:
        print("Error: start failed")


    # os.system('adb version')
    # os.system('adb devices')  # os.system是不支持读取操作的

    while os.system('adb root') != 0:
        time.sleep(1)

    print('device is restarted')

    reboot(apn)

    while os.system("adb reboot"):
        time.sleep(1)
