import os
import time

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        pass

    return False


def adb_shell():
    adb='/Users/nemausa/OneDrive/Tool/Mac/adb-support-host/mac/adb'
    cmd = adb + ' -host shell ps -eo pid,command'
    r = os.popen(cmd).read()
    # print(r)

    ps = list(r.split('\n'))
    # print(ps)
    lines = []
    for var in ps:
        var = var.replace('\t', '')
        var = var.replace('\n', '')
        var = var.replace(',', ' ')
        pid = var[0:5]
        command = var[5:]
        if is_number(pid) is not True:
            continue
        cmd = adb + ' -host shell cat proc/' + str(int(pid)) + '/status | grep VmRSS'
        # print(cmd)
        r = os.popen(cmd).read()
        r = r.replace('VmRSS:', '')
        line = pid + ',' + command + ',' + r + '\n'
        line = "".join([s for s in line.splitlines(True) if s.strip()])
        lines.append(line)
        # print(line)

    with open('test.csv', 'a') as f:
        f.writelines(lines)

count = 0
while True:
    ++count
    print('I am working ' + str(count))
    adb_shell()
    time.sleep(10)