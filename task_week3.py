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
        # self.lengths = []
        # self.freqs = []
        self.notes = []
        self.bpms = []

    def append_note(self, note):
        """Noteオブジェクトを取って音を追加する
        note: Noteオブジェクト
        """
        # self.lengths.append(note.length)
        # self.freqs.append(note.freq)
        self.notes.append(note)
        self.bpms.append(self.bpm)

    def play(self):
        for (note, bpm) in zip(self.notes, self.bpms):
            # Note.length = self.lengths[i]
            # Note.freq = self.freqs[i]
            wave = note.generate_wave(bpm, self.rate)
            pa = pyaudio.PyAudio()
            stream = pa.open(format=pyaudio.paFloat32, channels=1,
                             rate=self.rate, output=True)
            stream.write(wave.astype(np.float32).tostring())


def main():
    player = SimpleMusic(120, 44100)
    player.append_note(Note("c4"))
    player.append_note(Note("d4"))
    player.append_note(Note("e4"))
    player.bpm = 60  # 途中で遅くする
    player.append_note(Note("f4"))
    player.append_note(Note("g4"))
    player.append_note(Note("a4"))
    player.append_note(Note("b4"))
    player.append_note(Note("c5"))
    player.play()


if __name__ == '__main__':
    main()
