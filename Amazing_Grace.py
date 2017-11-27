import math

import numpy as np
import pyaudio

RATE = 44100  # sample rate
CHANNEL_NUM = 1  # チャンネル数 今回はモノラルなので1
NOTE_FREQ = {  # 音の周波数
    "d6": 1174.659,
    "c6": 1046.502,
    "d#5": 622.254,
    "b5": 987.767,
    "a5": 880.000,
    "g5": 783.991,
    "f#5": 739.989,
    "f5": 698.456,
    "e5": 659.255,
    "d5": 587.330,
    "c#5": 554.365,
    "b4": 493.883,
    "a4": 440.000,
    "g4": 391.995,
    "e4": 329.628,
    "d4": 293.665,
    "c4": 261.626,
    "b3": 246.942,
    "a3": 220.000,
}
BPM = 120
VOLUME = 0.1

def tone(scale, length):
    '''generate tone wave

    周波数と長さからsin波を作成する関数
    scale  : frequency [Hz]
    length : length (quater note is 1)
    ''',

    step = (2 * math.pi) * NOTE_FREQ[scale] / 44100  # 2πf*(1/rate)
    wave = np.sin(step * np.arange(length * (60 / BPM) * RATE))  # sin(2πft)
    return wave


def rest(length):  # 休符
    wave = np.zeros(int(length * (60 / BPM) * RATE))
    return wave


def chords(scale1, length1, scale2, length2):   # 二つの音を合成する関数．lengthの短い方に合わせる．
    wave1 = tone(scale1, min(length1, length2))
    wave2 = tone(scale2, min(length1, length2))
    wave = wave1 + wave2
    return wave


def main():
    # pyaudioのストリームを開く
    # streamへ波形を書き込みすると音が出る
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32, channels=CHANNEL_NUM, rate=RATE,
                     output=True)

    # 波形を作成する（Amazing Grace）
    wave = []
    wave.append(chords("d4", 1, "b3", 1))
    wave.append(chords("g4", 2, "b3", 2))
    wave.append(chords("b4", 0.5, "d4", 1)) # ここでd4が二回入力されるのがキモい
    wave.append(chords("g4", 0.5, "d4", 1))
    wave.append(chords("b4", 2, "d4", 2))
    wave.append(chords("a4", 1, "c4", 1))
    wave.append(chords("g4", 2, "b3", 2))
    wave.append(chords("e4", 1, "c4", 1))
    wave.append(chords("d4", 2, "b3", 2))

    # 全部のsin波をつなげる
    wave = np.concatenate(wave, axis=0)
    wave *= VOLUME

    # 鳴らす
    # pyaudioでは波形を量子化ビット数32ビット，
    # 16進数表示でstreamに書き込むことで音を鳴らせる
    stream.write(wave.astype(np.float32).tostring())

if __name__ == '__main__':
    main()
