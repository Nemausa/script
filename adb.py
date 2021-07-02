# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# @file: adb_shell.py
# @author: xiaoxiao
# @date  : 2019/9/10


import subprocess
import os



# 方法一：os.system()
# 返回值：返回对应状态码，且状态码只会有0(成功)、1、2。
# 其它说明：os.system()的返回值并不是执行程序的返回结果。而是一个16位的数，它的高位才是返回码。也就是说os.system()执行返回256即 0×0100，返回码应该是其高位0×01即1。所以要获取它的状态码的话，需要通过>>8移位获取。
# def adb_shell(cmd):
#     exit_code = os.system(cmd)
#     return exit_code>>8
    # # os.system(cmd)命令会直接把结果输出，所以在不对状态码进行分析处理的情况下，一般直接调用即可
    # os.system(cmd)


# # 方法二：os.popen()
# # 返回值：返回脚本命令输出的内容
# # 其它说明：os.popen()可以实现一个“管道”，从这个命令获取的值可以继续被调用。而os.system不同，它只是调用，调用完后自身退出，执行成功直接返回个0。
def adb_shell(cmd):
    result = os.popen(cmd).read()
    return result


# # 方法三：subprocess.Popen()
# # 返回值：Popen类的构造函数，返回结果为subprocess.Popen对象，脚本命令的执行结果可以通过stdout.read()获取。
# def adb_shell(cmd):
#     # 执行cmd命令，如果成功，返回(0, 'xxx')；如果失败，返回(1, 'xxx')
#     res = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # 使用管道
#     result = res.stdout.read()  # 获取输出结果
#     res.wait()  # 等待命令执行完成
#     res.stdout.close() # 关闭标准输出
#     return result


# # 方法四：subprocess.getstatusoutput()
# # 返回值：返回是一个元组，如果成功，返回(0, 'xxx')；如果失败，返回(1, 'xxx')
# def adb_shell(cmd):
#     result = subprocess.getstatusoutput(cmd)
#     return result


# cmd = 'adb shell dumpsys activity | grep "Run #"'
# print(adb_shell(cmd))