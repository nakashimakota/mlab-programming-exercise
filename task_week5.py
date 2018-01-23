from collections import deque

# import math
import matplotlib.animation as anm
import matplotlib.pyplot as plt
import numpy as np
import pyaudio


#
# 音の取得
#
class AudioInput(object):

    # PyAudioとNumpyのフォーマット．同じデータ型にしておく
    FORMAT_PA = pyaudio.paFloat32
    FORMAT_NP = np.float32

    # CHUNK / RATE が UPDATE_M_SECONDを超えると
    # （他の処理の計算量によっては近づくと）
    # 取得しきれないデータが発生してうまくコンスタレーションが
    # 計算できなくなるので注意
    RATE = 44100  # サンプルレート
    CHUNK = 2048  # 一度の読み込みで入ってくる音のサンプル数
    UPDATE_M_SECOND = 5 # 更新頻度
    CHANNELS = 1

    HISTORY = 5  # 何サンプルデータを保存するか
    LO_FREQUENCY = 1000

    def __init__(self):
        # 音声の読み込み用ストリームを開く
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            format=self.FORMAT_PA, channels=self.CHANNELS, rate=self.RATE,
            input=True, output=False, frames_per_buffer=self.CHUNK)
        self.phase_start_index = 0

    def audioinput(self):
        '''PyAudioのstreamから波形を読み込んでnp.arrayにして返す'''

        data = self.stream.read(self.CHUNK, exception_on_overflow=False)
        wave = np.frombuffer(data, dtype=self.FORMAT_NP)
        return wave

    def show(self):
        fig = plt.figure()
        # 描画データのプレースホルダ
        im, = plt.plot([0] * self.HISTORY, [0] * self.HISTORY, 'bo')

        queue_cos = deque([0] * self.HISTORY, maxlen=self.HISTORY)
        queue_sin = deque([0] * self.HISTORY, maxlen=self.HISTORY)

        def update(frame):
            wave = self.audioinput()
            # sin波との内積によりrealパートを取得する
            lo_wave_sin = [
                np.sin(-2 * np.pi * self.LO_FREQUENCY * x / self.RATE)
                for x in range(self.phase_start_index, self.phase_start_index + self.CHUNK)
            ]
            img_sin = np.dot(lo_wave_sin, wave)
            queue_sin.append(img_sin)

            # cos波との内積によりimgパートを取得する
            lo_wave_cos = [
                np.cos(-2 * np.pi * self.LO_FREQUENCY * x / self.RATE)
                for x in range(self.phase_start_index, self.phase_start_index + self.CHUNK)
            ]
            img_cos = np.dot(lo_wave_cos, wave)
            self.phase_start_index = (self.phase_start_index + self.CHUNK) % self.RATE
            queue_cos.append(img_cos)

            # plotのプレースホルダに値を突っ込む
            im.set_data(queue_cos, queue_sin)

            # プレースホルダを返すことで高速な描画が可能
            return im

        ani = anm.FuncAnimation(fig, update, interval=self.UPDATE_M_SECOND)
        plt.show()


def main():
    ai = AudioInput()
    ai.show()


if __name__ == '__main__':
    main()
