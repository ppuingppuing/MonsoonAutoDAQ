import Monsoon.reflash as reflash

Mon = reflash.bootloaderMonsoon()
Mon.setup_usb()

Header, Hex = Mon.getHeaderFromFWM('/Users/ppuing/Desktop/LVPM_RevE_Prot_1_Ver32.fwm')

if(Mon.verifyHeader(Header)):
    Mon.writeFlash(Hex)


# 구형 디바이스(흰색) LVPM은 Firmware를 Flash 해주는 과정이 필요.
# github의 msoon 계정에서 .fwm 파일을 다운받아올 것
# python 2를 사용해야 정상적으로 동작 (byte와 string 관련)
