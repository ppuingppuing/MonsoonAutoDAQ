import Monsoon.LVPM as LVPM
import Monsoon.sampleEngine as sampleEngine

import csv
import numpy

from datetime import datetime
from time import sleep

import threading

count = 0
f = open('data.csv', 'w', newline='')
wr = csv.writer(f)


class MonsoonDAQ:

    print("Monsoon Set up...")  # 이거 뭐지..왜 돌지
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

        print("getSamples() start...")
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

        self.myengine.startSampling(5000)
        mysamples6 = self.myengine.getSamples()

        self.myengine.startSampling(5000)
        mysamples7 = self.myengine.getSamples()

        self.myengine.startSampling(5000)
        mysamples8 = self.myengine.getSamples()

        self.myengine.startSampling(5000)
        mysamples9 = self.myengine.getSamples()

        self.myengine.startSampling(5000)
        mysamples10 = self.myengine.getSamples()

        # sample 중에서 전류채널은 [1]입니다. API guide 참고
        mysamples = mysamples1[1] + mysamples2[1] + mysamples3[1] + mysamples4[1] + mysamples5[1] \
            + mysamples6[1] + mysamples7[1] + mysamples8[1] + mysamples9[1] + mysamples10[1]

        print("getSamples() end...")

        sample_mean = numpy.mean(mysamples)
        sample_std = numpy.std(mysamples)

        val_count = 0
        mycurrents = 0
        for i in range(len(mysamples)):
            if mysamples[i] < sample_mean + sample_std and mysamples[i] > sample_mean - sample_std:
                mycurrents = mycurrents + mysamples[i]
                val_count += 1

        current = mycurrents / val_count

        print("[", datetime.utcnow().strftime('%H:%M:%S.%f'), "] [%6d]" % count)
        print(repr(current))

        threading.Timer(8.83, self.getsamples).start()
        count += 1

    def setimages(self):
        # subprocess.call("adb devices", shell=True)
        # 원래는 여기서 데몬을 켜주려고 했으나 싱크를 맞추기 어려워서 직접 시작시키려고 새로 Step3를 만들었음,
        print("[", datetime.utcnow().strftime('%H:%M:%S.%f'), "] Daemon start... Unplug the phone!!!")


def main():
    mymonsoon = MonsoonDAQ()
    # mymonsoon.getsamples()

    thread1 = threading.Thread(target=mymonsoon.getsamples(), args=())
    thread2 = threading.Thread(target=mymonsoon.setimages(), args=())

    sleep(10)

    thread1.start()
    thread2.start()


if __name__ == "__main__":
    main()
