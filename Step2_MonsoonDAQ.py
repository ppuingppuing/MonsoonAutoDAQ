import Monsoon.LVPM as LVPM
import Monsoon.sampleEngine as sampleEngine

import numpy
import time

from datetime import datetime
from time import sleep

import threading

count = 0
bc = "  :  :  .      "


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

        print(repr(current50))

        ac = datetime.utcnow().strftime('%H:%M:%S.%f')
        print("[%s] " % ac, "[%s]" % bc)
        bc = ac

        print("Get ready for the next measurements...")
        threading.Timer(1.4, self.getsamples).start()
        count += 1


def main():
    mymonsoon = MonsoonDAQ()

    thread1 = threading.Thread(target=mymonsoon.getsamples(), args=())

    sleep(10)

    thread1.start()


if __name__ == "__main__":
    main()
