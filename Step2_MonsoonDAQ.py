import Monsoon.LVPM as LVPM
import Monsoon.sampleEngine as sampleEngine

import numpy
import time

from datetime import datetime
from time import sleep

import threading

count = 0
bc = datetime.utcnow().microsecond
bcc = datetime.utcnow().second
param = 1.5  # 간격에 따라 설정

duty = 7

starttime = time.time() - param

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
        global bc, bcc
        global param

        global starttime

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

        # print("[%6d][ 5samples][sig=50]" % count)
        # print(repr(current50))

        ac = datetime.utcnow()
        print("[%s] " % ac, "[%s] " % bc, end=' ')
        diff = ac.microsecond-bc
        bc = ac.microsecond


        if diff < 0:
            param = 1.35
        elif diff > 0:
            param = 1.5
        else:
            param = 1.5

        print("%d " % diff, "%d " %(ac.second-bcc))
        bcc = ac.second
        temp = starttime
        starttime = time.time()
        print(starttime-temp)

        hey = datetime.utcnow().strftime('%H:%M:%S.%f')
        print("[%s]" % hey)
        threading.Timer(param, self.getsamples).start()
        count += 1


def main():
    mymonsoon = MonsoonDAQ()

    thread1 = threading.Thread(target=mymonsoon.getsamples(), args=())

    sleep(10)

    thread1.start()


if __name__ == "__main__":
    main()
