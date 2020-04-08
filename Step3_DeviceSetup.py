import subprocess
import threading

port_num = 5558
col = 5


def daemon_call():
    # print("thread 1 start!")
    subprocess.call("adb shell nohup /data/local/tmp/DAQDaemon %d > /dev/null" % col, shell=True)


def wifi_off():
    # print("thread 2 start!")
    subprocess.call("adb shell svc wifi disable", shell=True)


def main():
    subprocess.call("adb connect 202.,,,:%d" % port_num, shell=True)
    subprocess.call("adb root", shell=True)
    subprocess.call("adb connect 202.3,,,:%d" % port_num, shell=True)

    print("Daemon start! Wait 7s.... ")

    myt1 = threading.Thread(target=daemon_call(), args=())
    # myt2 = threading.Thread(target=wifi_off(), args=())

    myt1.start()
    # myt2.start() # thread not working.......





if __name__ == "__main__":
    main()

