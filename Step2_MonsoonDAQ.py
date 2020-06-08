import Monsoon.LVPM as LVPM
import Monsoon.sampleEngine as sampleEngine

import Step3_DeviceSetup

import numpy
import time
import subprocess

from datetime import datetime
from time import sleep

import threading

x = 0
y = 0
count = 0

val_a = 0
val_ac = 0
val_ab = 0
val_abcd = 0

bc = "  :  :  .      "

col = Step3_DeviceSetup.col
pos = 8*(col-1)

class MonsoonDAQ:

    # print("Monsoon Set up...")  # 이거 뭐지..왜 돌지
    mymon = LVPM.Monsoon()
    mymon.setup_usb()

    myengine = sampleEngine.SampleEngine(mymon)
    myengine.disableCSVOutput()
    myengine.ConsoleOutput(False)

    print("Monsoon Setting Finished...")

    def __init__(self):
        pass

    def getsamples(self):
        global count
        global bc
        global pos

        global val_a, val_ab, val_ac, val_abcd

        print("Start Sampling")
        self.myengine.startSampling(5000)
        mysamples1 = self.myengine.getSamples()

        self.myengine.startSampling(5000)
        mysamples2 = self.myengine.getSamples()

        self.myengine.startSampling(5000)
        mysamples3 = self.myengine.getSamples()

        self.myengine.startSampling(5000)
        mysamples4 = self.myengine.getSamples()

        self.myengine.startSampling(5000)
        mysamples5 = self.myengine.getSamples()
        print("End Sampling")

        # sample 중에서 전류채널은 [1]입니다. API guide 참고
        mysamples_5 = mysamples1[1] + mysamples2[1] + mysamples3[1] + mysamples4[1] + mysamples5[1]

        # 샘플 처리 시작
        sample_mean = numpy.mean(mysamples_5)
        sample_std = numpy.std(mysamples_5)

        sig_50 = 0.6745 * sample_std

        val_count50 = 0
        mycurrents50 = 0

        for i in range(len(mysamples_5)):
            if sample_mean - sig_50 < mysamples_5[i] < sample_mean + sig_50 :
                mycurrents50 = mycurrents50 + mysamples_5[i]
                val_count50 += 1

        current50 = mycurrents50 / val_count50

        # current50 = numpy.mean(mysamples_5)

        ac = datetime.utcnow().strftime('%H:%M:%S.%f')
        print("[%s] " % ac, "[%s] " % bc, "/[%d] measured : " % count, repr(current50))
        bc = ac

        if count%4 == 0:
            val_a = current50
        elif count%4 == 1:
            val_ab = current50
        elif count%4 == 2:
            val_ac = current50
        elif count%4 == 3:
            val_abcd = current50

        if count % 4 == 3:
            grid_val = val_abcd - val_ab - val_ac + val_a
            self.store_val(int(pos/8), pos % 8, grid_val)
            pos += 1
            if pos >= 64:
                self.send_data()
                return

        threading.Timer(1.4, self.getsamples).start()
        count += 1

    def store_val(self, x, y, value):
        # t에 값을 저장함.
        global col
        f = open("val_t", 'r')
        mymy = f.read().split(',')
        f.close()

        mymy[8*x+y] = value

        f = open("val_t", 'w')
        f.write(','.join(map(str,mymy)))
        f.close()

    def store_init(self):
        # t에 있던 값을 init로 옮겨서 저장함
        f = open("val_t", 'r')
        old = f.read().split(',')
        f.close()

        f = open("val_init", 'w')
        f.write(','.join(map(str,old)))
        f.close()

    def store_old_value(self):
        # t에 있던 값을 t-1로 옮겨서 저장함
        f = open("val_t", 'r')
        old = f.read().split(',')
        f.close()

        f = open("val_t-1", 'w')
        f.write(','.join(map(str,old)))
        f.close()

    def send_data(self):
        # val_* 전체를 adb를 이용하여 전송
        subprocess.call("adb shell push ./val_* /data/local/tmp", shell=True)

def main():
    mymonsoon = MonsoonDAQ()

    thread1 = threading.Thread(target=mymonsoon.getsamples(), args=())

    sleep(10)

    thread1.start()


if __name__ == "__main__":
    main()
