# M5StickV-isolated-words-recognizer
Isolated words recognizer for M5StickV

[日本語](README.md) | English

# Overview

If you run it on an M5StickV with a microphone, it will be able to recognize the recorded words.
　
# Develop Environment
It uses Speech Recognizer, so it will not work with the firmware officially released by Sipeed, which will cause an import error.
　
- MaixPy IDE v0.2.5
- firmware 0.6.2

## How to build the firmware

See [M5StickVのファームウェアビルド手順](https://raspberrypi.mongonta.com/howto-build-firmware-of-m5stickv/)（Japanese Only）

# Supported
M5StickV（with Microphone）

If you refer to the comments in the source and change the GPIO pin settings, it will work on the Sipeed MaixDock and Maixduino. (The source referenced is for MaixDock.)

# Usage
Write the bin in the firmware folder with kflash_gui and put boot.py on the root of the SD card and boot it.

## first boot
The message "Please Speak 1" will be displayed. Since there is no recording file, you will need to record three words that are at least one second long. Please register three words that are longer than one second (they will be registered as 1, 2, and 3, respectively).

## after the socond time
If there is a recording file on the SD card, it will start in voice recognition mode. When you speak a registered word, the corresponding letters 1 to 3 will be displayed.
If you want to record again, press button A to enter the recording mode.

# Customize
## increase words
The number of words can be increased by increasing  「words」 array in boot.py.

## when to misrecognize
Refer to the log displayed in the terminal when you record, and adjust the following parameters.
- dtw_threshold
- frame_len_threshold

# Reference
　[isolated_word.py](https://github.com/sipeed/MaixPy_scripts/blob/master/multimedia/speech_recognizer/isolated_word.py)

# LICENSE
[MIT](LICENSE)

# Author
[Takao Akaki](https://github.com/mongonta0716)
