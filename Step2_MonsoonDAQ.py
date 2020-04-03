import Monsoon.LVPM as LVPM
import Monsoon.sampleEngine as sampleEngine
import Monsoon.Operations as op

import subprocess
import threading
from time import sleep

# Monsoon Setup
myMon = LVPM.Monsoon()
myMon.setup_usb()
myMon.setVout(4.0)

# 매뉴얼에 있던 예제 1 - 콘솔 출력 및 단순 csv에 저장하기
myEngine = sampleEngine.SampleEngine(myMon)
myEngine.enableCSVOutput("MainEx.csv")
myEngine.ConsoleOutput(True)

numSamples = 5000
myEngine.startSampling(numSamples)


# 시스템에 따라 200 us 샘플링 속도를 못맞출 수도 있다네

# myEngine = sampleEngine.SampleEngine(myMon)
# myEngine.disableCSVOutput()
#
# myEngine.startSampling(5000)
# samples = myEngine.getSamples()
