from typing import (
    Tuple,
)

import torch
import numpy as np


class ReplayMemory(object): # 用于存储游戏的中间样本（经验池）

    def __init__(
            self,
            capacity: int, # 1e5
    ) -> None:
        self.__capacity = capacity # 1e5
        self.__pos = 0 # 存储位置
        self.buffer = [] # 缓存区，存储五元组
        # 存储优先级
        self.__m_priority = np.zeros((capacity, ), dtype=np.float32) # 优先级

    # 加入memory
    def push(
            self,
            state
    ): # 保存一次交互：状态、动作、收益、是否完成

        # 当buffer为空时，将max_prio初始化为0，否则为最大值
        # 这是为了防止第一次进行sample时，memory为空，导致程序卡死
        max_prio = self.__m_priority.max() if self.buffer else 1.0

        # buffer未满则append，否则覆盖
        if len(self.buffer) < self.__capacity:
            self.buffer.append(state)
        else:
            self.buffer[self.__pos] = state
        # 更新优先极和pos
        self.__m_priority[self.__pos] = max_prio
        self.__pos = (self.__pos + 1) % self.__capacity # 位置+1

    # 采样
    def sample(self, batch_size: int):
        # 若buffer满了，则直接取整个数组，否则取当前存在的pos个
        if len(self.buffer) == self.__capacity:
            prios = self.__m_priority
        else:
            prios = self.__m_priority[:self.__pos]
        # 计算每个优先级的概率
        probs  = prios ** 0.6
        probs /= probs.sum()
        # 抽取indices
        indices = np.random.choice(len(self.buffer), batch_size, p=probs)
        # 计算权重用于计算loss
        total    = len(self.buffer)
        weights  = (total * probs[indices]) ** (-0.4)
        weights /= weights.max()
        weights  = np.array(weights, dtype=np.float32)
        state = np.array(self.buffer)[indices]

        return state,indices,weights
    
    # 更新优先级
    def update_priorities(self, batch_indices, batch_priorities):
        for idx, prio in zip(batch_indices, batch_priorities):
            self.__m_priority[idx] = prio
    
    # 返回长度
    def __len__(self) -> int:
        return len(self.buffer)