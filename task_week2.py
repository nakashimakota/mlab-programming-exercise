import math
import functools
import operator
import re
import numpy as np
import pyaudio

RATE = 44100  # sample rate
CHANNEL_NUM = 1  # チャンネル数 今回はモノラルなので1

NOTE_POWER = {     #音の乗数
    "c": -9,
    "c#": -8,
    "d": -7,
    "d#": -6,
    "e": -5,
    "f": -4,
    "f#": -3,
    "g": -2,
    "g#": -1,
    "a": 0,
    "a#": 1,
    "b": 2,
}

VOLUME = 0.1


def tone(scale, length):
    '''generate tone wave

    周波数と長さからsin波を作成する関数
    scale  : 音階
    length : length (quater note is 1)
    ''',

    pattern1 = r'([a-g]+\#?)'
    pattern2 = r'(\d)'
    key = re.search(pattern1, scale)
    octabe = re.search(pattern2, scale)
    standard = 55 * 2**(float(octabe.group(0)) - 1)  #基準となるラの周波数を決める

    step = (2 * math.pi) * standard * 2**(
        NOTE_POWER[key.group(0)] / 12) / 44100  # 2πf*(1/rate)
    wave = np.sin(step * np.arange(length * (60 / BPM) * RATE))  # sin(2πft)
    wave *= np.linspace(1.5, 0.3, len(wave))
    return wave


def rest(length):  # 休符
    wave = np.zeros(int(length * (60 / BPM) * RATE))
    return wave


def notes(tones):
    '''generate multiple notes wave
    連符のような異なる音階を時間的につなぐ関数
    tones : list of tone (wave)
    '''

    return np.concatenate(tones, axis=0)


def chord(tones):
    '''generate chord wave
    waveのリストから和音を作成する関数
    tones : list of tone (wave)
    '''

    return functools.reduce(operator.add, tones)


def main():

    class Amazing_grace:
        global BPM
        BPM = 120
        # pyaudioのストリームを開く
        # streamへ波形を書き込みすると音が出る
        pa = pyaudio.PyAudio()
        stream = pa.open(format=pyaudio.paFloat32, channels=CHANNEL_NUM,
                         rate=RATE, output=True)

        # 波形を作成する（Amazing Grace）
        wave = []
        wave.append(chord([tone("b3", 1), tone("d4", 1)]))
        wave.append(chord([tone("b3", 2), tone("g4", 2)]))
        wave.append(
            chord([tone("d4", 1),
                   notes([tone("b4", 0.5), tone("g4", 0.5)])]))
        wave.append(chord([tone("d4", 2), tone("b4", 2)]))
        wave.append(chord([tone("c4", 1), tone("a4", 1)]))
        wave.append(chord([tone("b3", 2), tone("g4", 2)]))
        wave.append(chord([tone("c4", 1), tone("e4", 1)]))
        wave.append(chord([tone("b3", 2), tone("d4", 2)]))

        # 全部のsin波をつなげる
        wave = np.concatenate(wave, axis=0)
        wave *= VOLUME

        # 鳴らす
        # pyaudioでは波形を量子化ビット数32ビット，
        # 16進数表示でstreamに書き込むことで音を鳴らせる
        stream.write(wave.astype(np.float32).tostring())

    class Canon:
        global BPM
        BPM = 90
        # pyaudioのストリームを開く
        # streamへ波形を書き込みすると音が出る
        pa = pyaudio.PyAudio()
        stream = pa.open(format=pyaudio.paFloat32, channels=CHANNEL_NUM,
                         rate=RATE, output=True)

        # 波形を作成する（Amazing Grace）
        wave = []
        wave.append(
            chord([
                tone("d5", 2),
                tone("f#4", 2),
                notes([tone("d3", 1), tone("f#3", 1)])
            ]))
        wave.append(
            chord([
                tone("c#5", 2),
                tone("a4", 2),
                notes([tone("a3", 1), tone("g3", 1)])
            ]))
        wave.append(
            chord([
                tone("b4", 2),
                tone("d4", 2),
                notes([tone("f#3", 1), tone("d3", 1)])
            ]))
        wave.append(
            chord([
                tone("a4", 2),
                tone("f#4", 2),
                notes([tone("f#3", 1), tone("e3", 1)])
            ]))
        wave.append(
            chord([
                tone("g4", 2),
                tone("b3", 2),
                notes([tone("d3", 1), tone("b2", 1)])
            ]))
        wave.append(
            chord([
                tone("f#4", 2),
                tone("d4", 2),
                notes([tone("d3", 1), tone("a2", 1)])
            ]))
        wave.append(
            chord([
                tone("g4", 2),
                tone("b3", 2),
                notes([tone("g2", 1), tone("b2", 1)])
            ]))
        wave.append(
            chord([
                tone("a4", 2),
                tone("c#4", 2),
                notes([tone("c#3", 1), tone("a2", 1)])
            ]))

        # 全部のsin波をつなげる
        wave = np.concatenate(wave, axis=0)
        wave *= VOLUME

        # 鳴らす
        # pyaudioでは波形を量子化ビット数32ビット，
        # 16進数表示でstreamに書き込むことで音を鳴らせる
        stream.write(wave.astype(np.float32).tostring())


if __name__ == '__main__':
    main()
