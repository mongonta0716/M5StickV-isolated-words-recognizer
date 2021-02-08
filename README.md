# M5StickV-isolated-words-recognizer
Isolated words recognizer for M5StickV

日本語 | [English](README_en.md)

# 概要(Overview)
　
マイク付きのM5StickVで使用することにより、音声認識を行うことが可能です。

# 開発環境(Develop Environment)
　
Speech Recognizerを使用するため、Sipeedから正式にリリースされているファームウェアでは動きません。importエラーが起きます。
- MaixPy IDE v0.2.5
- firmware 0.6.2（ビルド済みのものを添付しています。）

※ ファームウェアはM5StickV用とMaixシリーズ用の２種類あるので間違えないようにしてください。

## ファームウェアのビルド方法

[M5StickVのファームウェアビルド手順](https://raspberrypi.mongonta.com/howto-build-firmware-of-m5stickv/)を参照してください。（日本語のみ）

# 対応機種
## M5StickV（マイク搭載バージョンのみ）
ファームウェアを書き換えると、M5StickVの電源ボタンの挙動が変わるので注意してください。
- 電源ON：電源ボタンを短く２回押す
- 電源OFF：電源ボタンを２秒以上長押し


## Sipeed MaixM1DockやMaixduino
[boot.py](boot.py)のコメントを参照してBOARD_NAMEをMAIXDUINOかM1DOCKに変更してください。

新しいファームウェアなのでconfig.jsonファイルがflash上に必要です。MaixPyIDEで接続し、対応したスクリプトを実行してください。
[https://github.com/sipeed/MaixPy_scripts/tree/master/board](https://github.com/sipeed/MaixPy_scripts/tree/master/board)

# 使い方(Usage)
firmware_for_M5StickVのフォルダにあるbinをkflash_guiで書き込み、boot.pyをSDカードのルート上に置いてM5StickVを起動してください。

※ firmware_for_MaixはMaixM1Dock,Maixduino用です。

## 初回起動
「Please Speak 1」と表示されます。
録音ファイルが無いので、まずは録音が必要です。１秒以上の言葉を３つ登録してください。（それぞれ1,2,3で登録されます。）

## ２回め以降の起動
録音ファイルがある場合は、音声認識モードで起動します。登録したワードを喋ると対応した1〜3の文字が表示されます。
再度録音したい場合はボタンAを押すと、録音モードになります。

# カスタマイズ
## 単語を増やす
初期は3つになっていますが、増やすことも可能です。多いと登録が大変なので3つにしています。

boot.pyのwordsの配列を増やすと単語数を増やすことが可能です。10個まではテストしましたが、どのくらい増やせるかは分かりません。

## 認識が悪い場合
誤検出を減らすために、パラメータを設定しています。ターミナルに表示される値を元に変更してみてください。
- dtw_threshold : dtwで検出される値
- frame_len_threshold ： msecでこれ以下のワードは検出されないようになっています。

# 参考にしたソース
Sipeed社のMaix_Scriptsにある[isolated_word.py](https://github.com/sipeed/MaixPy_scripts/blob/master/multimedia/speech_recognizer/isolated_word.py)を参考に作成しました。

# LICENSE
[MIT](LICENSE)

# Author
[Takao Akaki](https://github.com/mongonta0716)
