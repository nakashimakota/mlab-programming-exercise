import math
import numpy as np
import pyaudio


class Note(object):

    def __init__(self, scale, length=1):
        self.length = length
        """scaleは"d2"などの音階を表す文字列．簡単化のため#,♭はなし"""

        key, octave = scale[0], int(scale[1])

        # 音階の処理
        scale_name = 'cxdxefxgxaxb'  # こそぴょんのパクリ
        key_index = scale_name.find(key)
        factor = key_index - 9

        self.freq = 55 * 2**((octave - 1) + factor / 12)

    def generate_wave(self, bpm, rate):
        step = (2 * math.pi) * self.freq / rate  # 2πf*(1/rate)
        wave = np.sin(
            step * np.arange(int(self.length * (60 / bpm) * rate)))  # sin(2πft)
        return wave


class SimpleMusic(object):

    def __init__(self, bpm, rate):
        self.bpm = bpm
        self.rate = rate
        self.notes = []

    def append_note(self, note):
        """Noteオブジェクトを取って音を追加する
        note: Noteオブジェクト
        """
        self.notes.append(note)

    def play(self):
        """波の生成"""
        for note in self.notes:
            wave = note.generate_wave(self.bpm, self.rate)
            pa = pyaudio.PyAudio()
            stream = pa.open(format=pyaudio.paFloat32, channels=1,
                             rate=self.rate, output=True)
            stream.write(wave.astype(np.float32).tostring())


def main():
    player = SimpleMusic(120, 44100)
    player.append_note(Note("c4"))
    player.append_note(Note("d4"))
    player.append_note(Note("e4"))
    player.append_note(Note("f4"))
    player.append_note(Note("g4"))
    player.append_note(Note("a4"))
    player.append_note(Note("b4"))
    player.append_note(Note("c5"))
    player.play()
    player.bpm = 240  # 速さを2倍にして鳴らす．
    player.play()


if __name__ == '__main__':
    main()
