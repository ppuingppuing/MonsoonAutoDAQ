import Monsoon.LVPM as LVPM
import Monsoon.sampleEngine as sampleEngine
import Monsoon.Operations as op

# Monsoon Setup
myMon = LVPM.Monsoon()
myMon.setup_usb()
myMon.setVout(3.9)

# # 매뉴얼에 있던 예제 1 - 콘솔 출력 및 단순 csv에 저장하기
# myEngine = sampleEngine.SampleEngine(myMon)
# myEngine.enableCSVOutput("MainEx.csv")
# myEngine.ConsoleOutput(True)
#
# numSamples = 5000   # the number of samples
#
# myEngine.startSampling(numSamples)
# 시스템에 따라 200 us 샘플링 속도를 못맞출 수도 있다네

#
# # 매뉴얼에 있던 예제 2 - 1초동안 측정하고 값 저장하기
# myEngine = sampleEngine.SampleEngine(myMon)
# myEngine.disableCSVOutput()     # must disable CSV for getSamples()
# myEngine.ConsoleOutput(True)
#
# numSamples = 5000   # the number of samples for one second
# numGranularity = 10     # 10 = 1 out of 10 samples stored
#
# myEngine.startSampling(numSamples)
#
# mySamples = myEngine.getSamples()
#
# Currents = 0
# for i in range(len(mySamples[sampleEngine.channels.timeStamp])):
#     Currents += mySamples[sampleEngine.channels.MainCurrent][i]
#
# myCurrents = Currents/len(mySamples[sampleEngine.channels.timeStamp])
# print(repr(myCurrents))
