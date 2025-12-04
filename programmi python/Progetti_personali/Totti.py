import pyautogui
from time import sleep
from random import randint

sleep(10)
with open("C:/Users/Dell/Desktop/Totti.txt","r") as file:
    for n, line in enumerate(file):
        pyautogui.typewrite(line)
        sleep(randint(1,100)/10)
