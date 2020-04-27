import subprocess
import threading

port_num = 5558
col = 3    # 다시 측정할것부터

ip_f = open('ip.txt', mode='rt')
ip_s = ip_f.read(13)

def daemon_call():
    # print("thread 1 start!")
    subprocess.call("adb shell nohup /data/local/tmp/DAQDaemon %d > /dev/null" % col, shell=True)


def wifi_off():
    # print("thread 2 start!")
    subprocess.call("adb shell svc wifi disable", shell=True)


def main():
    connect_command = "adb connect " + ip_s + ":" + repr(port_num)

    subprocess.call(connect_command, shell=True)
    subprocess.call("adb root", shell=True)
    subprocess.call(connect_command, shell=True)

    print("Daemon start! Wait 7s.... ")

    myt1 = threading.Thread(target=daemon_call(), args=())
    # myt2 = threading.Thread(target=wifi_off(), args=())

    myt1.start()
    # myt2.start() # thread not working.......


if __name__ == "__main__":
    main()

