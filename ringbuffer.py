#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import math

class RingBuffer(object):

    def __init__(self, capacity):
        """capacity:最大の容量"""
        self.capacity = capacity
        self.buff = [0] * self.capacity # 最大容量の大きさの空配列を作成
        self.begin = 0  # 始点
        self.end = 0    # 終点
        self.count = 0  # 要素数

    def append_front(self, item):
        """先頭にitemを追加"""
        if self.count == self.capacity: # リングバッファが一杯ならばbegin,end両方移動させる．
            self.end = (self.end - 1) % self.capacity
        else:
            self.count += 1
        self.begin = (self.begin - 1) % self.capacity   # beginを前に移動
        self.buff[self.begin] = item
        self.get_list()

    def append_back(self, item):
        """最後尾にitemを追加"""
        if self.count == self.capacity:
            self.begin = (self.begin + 1) % self.capacity
        else:
            self.count += 1
        self.buff[self.end] = item
        self.end = (self.end + 1) % self.capacity   # endを後ろに移動
        self.get_list()
        # print("begin = ",self.begin)
        # print("end = ",self.end)

    def pop_front(self):
        """先頭のitemをreturnし削除"""
        self.count -= 1
        item = self.buff[self.begin]
        self.begin = (self.begin + 1) % self.capacity   # beginを後ろに移動
        self.get_list()
        return item

    def pop_back(self):
        """最後尾のitemをreturnし削除"""
        self.count -= 1
        self.end = (self.end - 1) % self.capacity   # endを前に移動
        item = self.buff[self.end]
        self.get_list()
        return item

    def get_list(self):
        """beginからendまでの値を配列として返す"""
        if self.end > self.begin:
            list = self.buff[self.begin:self.end]
        else:
            list = self.buff[self.begin:] + self.buff[:self.end]    # 配列をリングバッファっぽく並び替える．
        print(list)


def main():
    ringbuffer = RingBuffer(5)
    ringbuffer.append_front(1)
    ringbuffer.append_front(2)
    ringbuffer.append_front(3)
    ringbuffer.append_back(4)
    ringbuffer.append_back(5)
    ringbuffer.append_back(6)
    ringbuffer.append_back(7)
    ringbuffer.pop_front()
    ringbuffer.pop_front()
    ringbuffer.pop_back()
    ringbuffer.append_front(8)

if __name__ == '__main__':
    main()
