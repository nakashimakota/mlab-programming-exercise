#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import math
import numpy as np
import pyaudio


class Note(object):

    volume = 0.1

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
        wave *= self.__class__.volume
        return wave

class SimpleMusic(object):

    def __init__(self, bpm, rate=44100):
        self.bpm = bpm
        self.rate = rate
        self.notes = []

    def append_note(self, note):
        """Noteオブジェクトを取って音を追加する
        note: Noteオブジェクト
        """
        self.notes.append(note)

    def play(self):
        waves = [note.generate_wave(self.bpm, self.rate)  for note in self.notes]
        wave = np.concatenate(waves, axis=0)
        pa = pyaudio.PyAudio()
        stream = pa.open(format=pyaudio.paFloat32, channels=1, rate=self.rate, output=True)
        stream.write(wave.astype(np.float32).tostring())

    @classmethod
    def abc_music(cls, bpm):   # ドレミファソラシドを鳴らす音楽を作る
        music = cls(bpm=bpm)
        music.append_note(Note("c4"))
        music.append_note(Note("d4"))
        music.append_note(Note("e4"))
        music.append_note(Note("f4"))
        music.append_note(Note("g4"))
        music.append_note(Note("a4"))
        music.append_note(Note("b4"))
        music.append_note(Note("c5"))
        return music

def main():
    music = SimpleMusic.abc_music(120)
    music.play()
    Note.volume = 0.5   # 音量を5倍にする
    music.play()

if __name__ == '__main__':
    main()
