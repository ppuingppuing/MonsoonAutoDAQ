import Monsoon.LVPM as LVPM
import Monsoon.sampleEngine as sampleEngine
import Monsoon.Operations as op

import csv

from datetime import datetime
from time import sleep

import threading
import subprocess


count = 0
f = open('data.csv', 'w', newline='')
wr = csv.writer(f)


class MonsoonDAQ:

    print("Monsoon Set up...")  # 이거 뭐지..왜 돌지
    mymon = LVPM.Monsoon()
    mymon.setup_usb()
    # mymon.setVout(4)

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
        mysamples = self.myengine.getSamples()

        currents = 0
        for i in range(len(mysamples[sampleEngine.channels.timeStamp])):
            currents += mysamples[sampleEngine.channels.MainCurrent][i]

        mycurrents1 = currents/len(mysamples[sampleEngine.channels.timeStamp])

        self.myengine.startSampling(5000)
        mysamples = self.myengine.getSamples()

        currents = 0
        for i in range(len(mysamples[sampleEngine.channels.timeStamp])):
            currents += mysamples[sampleEngine.channels.MainCurrent][i]

        mycurrents2 = currents/len(mysamples[sampleEngine.channels.timeStamp])

        self.myengine.startSampling(5000)
        mysamples = self.myengine.getSamples()

        currents = 0
        for i in range(len(mysamples[sampleEngine.channels.timeStamp])):
            currents += mysamples[sampleEngine.channels.MainCurrent][i]

        mycurrents3 = currents/len(mysamples[sampleEngine.channels.timeStamp])

        self.myengine.startSampling(5000)
        mysamples = self.myengine.getSamples()

        currents = 0
        for i in range(len(mysamples[sampleEngine.channels.timeStamp])):
            currents += mysamples[sampleEngine.channels.MainCurrent][i]

        print("getSamples() end...")
        mycurrents4 = currents/len(mysamples[sampleEngine.channels.timeStamp])

        mycurrents = (mycurrents1+mycurrents2+mycurrents3+mycurrents4)/4

        print("[", datetime.utcnow().strftime('%H:%M:%S.%f'), "] [%6d]" % count)
        print(repr(mycurrents))
        wr.writerow([count, mycurrents])

        threading.Timer(5.54, self.getsamples).start()
        count += 1

    def setimages(self):
        # subprocess.call("adb devices", shell=True)
        print("[", datetime.utcnow().strftime('%H:%M:%S.%f'), "] Daemon started... Unplug the phone!!!")


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
