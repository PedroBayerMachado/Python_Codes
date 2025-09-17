# click win, escrever chrome, escrever corvette, abrir site, etc

import pyautogui
import time

pyautogui.PAUSE = 1
pyautogui.press("win")
pyautogui.write("chrome")
pyautogui.press("enter")
time.sleep(4)
pyautogui.click(x=314, y=64)
pyautogui.write("Corvette c8 zr1x")
pyautogui.press("enter")
time.sleep(1)
pyautogui.click(x=306, y=346)
time.sleep(3)
pyautogui.scroll(-20000)
time.sleep(3)
pyautogui.click(x=288, y=16)
time.sleep(1)
pyautogui.write("Bi, isto foi uma automação Basica com Pyton usando pyautogui !!")