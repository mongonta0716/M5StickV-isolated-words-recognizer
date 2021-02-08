#####################################################################
# Copyright (c) 2021 Takao Akaki. All rights reserved.
#####################################################################

# Notice:
# If you want to use it with Sipeed Maix series, you need config.json in flash.
# Run the script in the link below.
# https://github.com/sipeed/MaixPy_scripts/tree/master/board

# BOARD_NAME == M5STICKV or M1DOCK or MAIXDUINO
BOARD_NAME = "M5STICKV"

import time
from Maix import GPIO, I2S
from fpioa_manager import *
from board import board_info
import os, Maix, lcd, image
from machine import I2C

if (BOARD_NAME == "M5STICKV"):
    from pmu import axp192
    pmu = axp192()
    pmu.enablePMICSleepMode(True)

sample_rate   = 16000

#####################################################################
# Initial values
#####################################################################

# If you increase the words array, the number of registered words
# will also increase.
words = ["1", "2", "3"]

# If the word recognition rate is low, look at the values of
# dtw_value and current_frame_len in the terminal and adjust them.
dtw_threshold = 400
frame_len_threshold = 70

# Settings for M5StickV. Maix series should fix the following lines.
if (BOARD_NAME == "M5STICKV"):
    lcd.init(type=3)
    fm.register(board_info.MIC_DAT,fm.fpioa.I2S0_IN_D0, force=True)
    fm.register(board_info.MIC_LRCLK,fm.fpioa.I2S0_WS, force=True)
    fm.register(board_info.MIC_CLK,fm.fpioa.I2S0_SCLK, force=True)
    fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1, force=True)
    button_a = GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)
    button_a_label = "BtnA"
elif ((BOARD_NAME == "MAIXDUINO") or (BOARD_NAME == "M1DOCK")):
    lcd.init()
    fm.register(board_info.MIC0_DATA, fm.fpioa.I2S0_IN_D0, force=True)
    fm.register(board_info.MIC0_WS, fm.fpioa.I2S0_WS, force=True)
    fm.register(board_info.MIC0_BCK, fm.fpioa.I2S0_SCLK, force=True)
    fm.register(board_info.BOOT_KEY, fm.fpioa.GPIO1, force=True)
    button_a = GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)
    button_a_label = "BtnBoot"

# data storage "/sd/" or "/flash/"
storage = "/flash/"


#####################################################################
# Functions
#####################################################################
def print_lcd(str1, str2=None, str3=None, serial_out=True, bgcolor=(0, 0, 0)):
    img.draw_rectangle((0, 0, lcd_w, lcd_h), fill=True, color=bgcolor)
    if (str1 != None):
        img.draw_string(10, 10, str1, color=(255, 0, 0), scale=2, mono_space=0)
        if (serial_out):
            print(str1)
    if (str2 != None):
        img.draw_string(10, 45, str2, color=(0, 0, 255), scale=2, mono_space=0)
        if (serial_out):
            print(str2)
    if (str3 != None):
        img.draw_string(10, 70, str3, color=(0, 0, 255), scale=3, mono_space=0)
        if (serial_out):
            print(str3)
    lcd.display(img)


def save_file(number, data):
    print_lcd("Data Saving...")
    lcd.display(img)
    filename0 = storage + "rec0_" + str(number) + ".sr"
    filename1 = storage + "rec1_" + str(number) + ".sr"
    t0 = data[0]
    t1 = data[1]
    print(type(t0))
    print(type(t1))
    with open(filename0, 'w') as f:
        f.write(str(t0))
    with open(filename1, 'wb') as f:
        f.write(bytearray(t1))

def load_data(number):
    print_lcd("Data Loading...")
    for i in range(number):
        print("load_data:" + str(i))
        filename0 = storage + "rec0_" + str(i) + ".sr"
        filename1 = storage + "rec1_" + str(i) + ".sr"
        with open(filename0, 'r') as f:
            data0 = f.read()
        with open(filename1, 'rb') as f:
            data1 = f.read()
        print(data0)
        print(data1)
        tupledata = [int(data0), data1]
        sr.set(i*2, tupledata)
        print(b'0x0d0x0a')

def record_voice():
    for i in range(len(words)):
        while True:
            time.sleep_ms(100)
            print(sr.state())
            if sr.Done == sr.record(i*2):
                print_lcd("get !")
                data = sr.get(i*2)
                save_file(i, data)
                print(data)
                break
            if sr.Speak == sr.state():
                print_lcd("Please speak " + words[i])
        sr.set(i*2, data)
        time.sleep_ms(500)

##############################################################################
# Main
##############################################################################
lcd.rotation(0)

if (BOARD_NAME == "M5STICKV"):
    # set lcd backlight for M5StickV
    i2c = I2C(I2C.I2C0, freq=400000, scl=28, sda=29)
    i2c.writeto_mem(0x34, 0x91, b'\xa0')
elif ((BOARD_NAME == "MAIXDUINO") or (BOARD_NAME == "M1DOCK")):
    lcd.set_backlight(50)

lcd_w = lcd.width()
lcd_h = lcd.height()
img = image.Image(size=(lcd_w, lcd_h))
print_lcd("MaixPy", "Isolated words Recognizer")
rx = I2S(I2S.DEVICE_0)
rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode=I2S.STANDARD_MODE)
rx.set_sample_rate(sample_rate)
print(rx)
from speech_recognizer import isolated_word
# model
sr = isolated_word(dmac=2, i2s=I2S.DEVICE_0, size=50)
print(sr.size())
print(sr)
## threshold
sr.set_threshold(0, 0, 10000)



# data set
try:
    load_data(len(words))
except Exception as e:
    record_voice()

# recognition
print_lcd("Recognition begin")
time.sleep_ms(1000)

while True:
    time.sleep_ms(200)
    print_lcd("Please speak word!", button_a_label + ":Record Voice", serial_out=False)
    if (button_a.value() == 0):
        record_voice()
    if sr.Done == sr.recognize():
        res = sr.result()
        print("(Number,dtw_value,currnt_frame_len,matched_frame_len)=" + str(res))
        if (res != None) and (res[1] < dtw_threshold) and (res[2] > frame_len_threshold):
            print(str(res[0]))
            for i in range(len(words)):
                if res[0] == (i * 2):
                    print_lcd("Recognize",str3=words[i], bgcolor=(255, 255, 255))
                    time.sleep_ms(200)

