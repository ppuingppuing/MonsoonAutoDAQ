import Monsoon.LVPM as LVPM
import Monsoon.sampleEngine as sampleEngine
import Monsoon.Operations as op

from datetime import datetime
import threading


count = 0

class MonsoonDAQ:

    print("Monsoon Set up...")
    mymon = LVPM.Monsoon()
    mymon.setup_usb()
    mymon.setVout(3.9)

    myengine = sampleEngine.SampleEngine(mymon)
    myengine.disableCSVOutput()
    myengine.ConsoleOutput(False)
    print("Monsoon Setting Finished...")

    def __init__(self):
        pass

    def getsamples(self):
        global count
        print("Get Samples! [%6d] [" % count, datetime.utcnow().strftime('%H:%M:%S.%f'),"]")

        self.myengine.startSampling(5000)
        mysamples = self.myengine.getSamples()

        currents = 0
        for i in range(len(mysamples[sampleEngine.channels.timeStamp])):
            currents += mysamples[sampleEngine.channels.MainCurrent][i]

        mycurrents = currents/len(mysamples[sampleEngine.channels.timeStamp])

        print(repr(mycurrents))

        threading.Timer(3.88, self.getsamples).start()
        count += 1


def main():
    mymonsoon = MonsoonDAQ()
    mymonsoon.getsamples()


if __name__ == "__main__":
    main()
