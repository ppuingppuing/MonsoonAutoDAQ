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



        # sample 중에서 전류채널은 [1]입니다. API guide 참고
        mysamples_5 = mysamples1[1] + mysamples3[1] + mysamples5[1] + mysamples7[1] + mysamples9[1]

        mysamples_10 = mysamples_5 \
            + mysamples2[1] + mysamples4[1] + mysamples6[1] + mysamples8[1] + mysamples10[1]

        print("getSamples() end...")

        # 샘플 처리 시작
        sample_mean = numpy.mean(mysamples_5)
        sample_std = numpy.std(mysamples_5)

        sig_50 = 0.6745 * sample_std
        sig_40 = 0.4 * sample_std
        sig_20 = 0.2 * sample_std

        val_count50 = 0
        mycurrents50 = 0

        val_count40 = 0
        mycurrents40 = 0

        val_count20 = 0
        mycurrents20 = 0

        for i in range(len(mysamples_5)):
            if mysamples_5[i] < sample_mean + sig_50 and mysamples_5[i] > sample_mean - sig_50:
                mycurrents50 = mycurrents50 + mysamples_5[i]
                val_count50 += 1
                if mysamples_5[i] < sample_mean + sig_40 and mysamples_5[i] > sample_mean - sig_40:
                    mycurrents40 = mycurrents40 + mysamples_5[i]
                    val_count40 += 1
                    if mysamples_5[i] < sample_mean + sig_20 and mysamples_5[i] > sample_mean - sig_20:
                        mycurrents20 = mycurrents20 + mysamples_5[i]
                        val_count20 += 1

        current50 = mycurrents50 / val_count50
        current40 = mycurrents40 / val_count40
        current20 = mycurrents20 / val_count20

        print("[%6d][ 5samples][sig=50]" % count)
        print(repr(current50))
        print("[%6d][ 5samples][sig=40]" % count)
        print(repr(current40))
        print("[%6d][ 5samples][sig=20]" % count)
        print(repr(current20))

        sample_mean = numpy.mean(mysamples_10)
        sample_std = numpy.std(mysamples_10)

        sig_50 = 0.6745 * sample_std
        sig_40 = 0.4 * sample_std
        sig_20 = 0.2 * sample_std

        val_count50 = 0
        mycurrents50 = 0

        val_count40 = 0
        mycurrents40 = 0

        val_count20 = 0
        mycurrents20 = 0

        for i in range(len(mysamples_10)):
            if mysamples_10[i] < sample_mean + sig_50 and mysamples_10[i] > sample_mean - sig_50:
                mycurrents50 = mycurrents50 + mysamples_10[i]
                val_count50 += 1
                if mysamples_10[i] < sample_mean + sig_40 and mysamples_10[i] > sample_mean - sig_40:
                    mycurrents40 = mycurrents40 + mysamples_10[i]
                    val_count40 += 1
                    if mysamples_10[i] < sample_mean + sig_20 and mysamples_10[i] > sample_mean - sig_20:
                        mycurrents20 = mycurrents20 + mysamples_10[i]
                        val_count20 += 1

        current50 = mycurrents50 / val_count50
        current40 = mycurrents40 / val_count40
        current20 = mycurrents20 / val_count20

        print("[%6d][10samples][sig=50]" % count)
        print(repr(current50))
        print("[%6d][10samples][sig=40]" % count)
        print(repr(current40))
        print("[%6d][10samples][sig=20]" % count)
        print(repr(current20))

        ac = datetime.utcnow().strftime('%H:%M:%S.%f')
        print("[%s] " % ac, "[%s]" % bc)
        bc = ac

        print("Get ready for the next measurements...")
        threading.Timer(8.777, self.getsamples).start()
        count += 1

def main():
    mymonsoon = MonsoonDAQ()
    # mymonsoon.getsamples()

    thread1 = threading.Thread(target=mymonsoon.getsamples(), args=())

    sleep(10)

    thread1.start()



if __name__ == "__main__":
    main()
