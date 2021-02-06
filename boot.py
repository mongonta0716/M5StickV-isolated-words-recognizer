import time
from Maix import GPIO, I2S
from fpioa_manager import *
from board import board_info
import os, Maix, lcd, image

sample_rate   = 16000
words = ["1", "2", "3"]

#####################################################################
# If the word recognition rate is low, look at the values of
# dtw_value and current_frame_len in the terminal and adjust them.
dtw_threshold = 400
frame_len_threshold = 60
#####################################################################

#####################################################################
# Settings for M5StickV. Maix series should fix the following lines.
lcd.init(type=3)
fm.register(board_info.MIC_DAT,fm.fpioa.I2S0_IN_D0, force=True)
fm.register(board_info.MIC_LRCLK,fm.fpioa.I2S0_WS, force=True)
fm.register(board_info.MIC_CLK,fm.fpioa.I2S0_SCLK, force=True)
fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1, force=True)
button_a = GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)
#####################################################################

lcd.rotation(0)
lcd_w = lcd.width()
lcd_h = lcd.height()
img = image.Image(size=(lcd_w, lcd_h))
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

def save_file(number, data):
    filename0 = "/sd/" + "rec0_" + str(number) + ".sr"
    filename1 = "/sd/" + "rec1_" + str(number) + ".sr"
    print(filename0)
    print(filename1)
    print(len(data))
    print(type(data))
    t0 = data[0]
    t1 = data[1]
    print(type(t0))
    print(type(t1))
    with open(filename0, 'w') as f:
        f.write(str(t0))
    with open(filename1, 'wb') as f:
        f.write(bytearray(t1))

def load_data(number):
    for i in range(number):
        print("load_data:" + str(i))
        filename0 = "/sd/" + "rec0_" + str(i) + ".sr"
        filename1 = "/sd/" + "rec1_" + str(i) + ".sr"
        with open(filename0, 'r') as f:
            data0 = f.read()
        with open(filename1, 'rb') as f:
            data1 = f.read()
        print(data0)
        print(data1)
        tupledata = [int(data0), data1]
        sr.set(i*2, tupledata)

## record and get & set
def record_voice():
    for i in range(len(words)):
        while True:
            time.sleep_ms(100)
            print(sr.state())
            if sr.Done == sr.record(i*2):
                data = sr.get(i*2)
                print(len(data))
                print(type(data))
                save_file(i, data)
                print(data)
                break
            if sr.Speak == sr.state():
                print('speak ' + words[i])
                img.draw_rectangle((0, 0, lcd_w, lcd_h), fill=True, color=(255, 255, 255))
                img.draw_string(10, 10, "Please speak " + words[i], color=(255, 0, 0), scale=2, mono_space=0)
                lcd.display(img)
        sr.set(i*2, data)
        img.draw_rectangle((0, 0, lcd_w, lcd_h), fill=True, color=(255, 255, 255))
        img.draw_string(10, 10, "get !", color=(255, 0, 0), scale=4, mono_space=0)
        lcd.display(img)
        time.sleep_ms(500)


## recognizer
try:
    load_data(len(words))
except Exception as e:
    record_voice()

print('recognizer')
img.draw_rectangle((0, 0, lcd_w, lcd_h), fill=True, color=(255, 255, 255))
img.draw_string(10, 10, "Recognition begin", color=(255, 0, 0), scale=2, mono_space=0)
lcd.display(img)
time.sleep_ms(1000)

while True:
    time.sleep_ms(200)
    img.draw_rectangle((0, 0, lcd_w, lcd_h), fill=True, color=(255, 255, 255))
    img.draw_string(10, 10, "Please speak words", color=(255, 0, 0), scale=2, mono_space=0)
    img.draw_string(10, 50, "BtnA: Record Voice", color=(0, 0, 255), scale=2, mono_space=0)
    lcd.display(img)
    if (button_a.value() == 0):
        record_voice()
    if sr.Done == sr.recognize():
        res = sr.result()
        print("(Number,dtw_value,currnt_frame_len,matched_frame_len)=" + str(res))
        if (res != None) and (res[1] < dtw_threshold) and (res[2] > frame_len_threshold):
            print(str(res[0]))
            for i in range(len(words)):
                if res[0] == (i * 2):
                    img.draw_rectangle((10, 10, lcd_w, lcd_h), fill=True, color=(255, 255, 255))
                    img.draw_string(int(lcd_w / 2), 30, words[i], color=(255, 0, 0), scale=5, mono_space=0)
                    lcd.display(img)
                    time.sleep_ms(200)

