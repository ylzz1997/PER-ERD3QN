import random
from collections import deque # 引入双端队列

import numpy as np
import torch

from project_files.model import Model
from project_files.game import Game
from project_files.model import Trainer
from project_files.constants import Direction, Point, MAX_MEMORY, BATCH_SIZE, BLOCK_SIZE, MUTATION_RATE
from project_files.utils_memory import ReplayMemory
class GameAIAgent:
    def __init__(self):
        self.memory =  ReplayMemory(MAX_MEMORY) # 设置存储五元组的存储器
        self.agent = Model(11, 256, 3)
        self.trainer = Trainer(11, 256, 3) # 训练对象

    @staticmethod
    def get_state(game: Game):          # 获取状态
        head = game.snake.head          # head为蛇头
        # 四个状态下将要移动到的点
        point_r = Point(head.x + BLOCK_SIZE, head.y) # 如果方向为右，点应该为蛇头右侧一格
        point_l = Point(head.x - BLOCK_SIZE, head.y) # 如果方向为左，点应该为蛇头左侧一格
        point_u = Point(head.x, head.y - BLOCK_SIZE) # 如果方向为上，点应该为蛇头上侧一格
        point_d = Point(head.x, head.y + BLOCK_SIZE) # 如果方向为下，点应该为蛇头下侧一格

        # 四个bool类型的数据，用来判断方向是否是right，left，up，down
        dir_is_r = game.snake.direction == Direction.RIGHT
        dir_is_l = game.snake.direction == Direction.LEFT
        dir_is_u = game.snake.direction == Direction.UP
        dir_is_d = game.snake.direction == Direction.DOWN

        state = [ # state是一个1*11的数tensor
            # danger straight
            # 向前走是危险的:向前有不同的方向，如果这些将要移动到的点将会导致创死，则认为是危险前移
            (dir_is_r and game.snake.is_collision(point_r))
            or (dir_is_l and game.snake.is_collision(point_l))
            or (dir_is_u and game.snake.is_collision(point_u))
            or (dir_is_d and game.snake.is_collision(point_d)),

            # danger right
            # 向右走是危险的，逻辑同上
            (dir_is_r and game.snake.is_collision(point_d))
            or (dir_is_l and game.snake.is_collision(point_u))
            or (dir_is_u and game.snake.is_collision(point_r))
            or (dir_is_d and game.snake.is_collision(point_l)),

            # danger left
            # 向左走是危险的，逻辑同上
            (dir_is_r and game.snake.is_collision(point_u))
            or (dir_is_l and game.snake.is_collision(point_d))
            or (dir_is_u and game.snake.is_collision(point_l))
            or (dir_is_d and game.snake.is_collision(point_r)),

            # move direction
            # 做出移动
            dir_is_l,
            dir_is_r,
            dir_is_u,
            dir_is_d,

            # food location
            # 寻找食物的位置
            game.food.x < game.snake.head.x,  # food left
            game.food.x > game.snake.head.x,  # food right
            game.food.y < game.snake.head.y,  # food up
            game.food.y > game.snake.head.y  # food down
        ]

        return np.array(state, dtype=np.int32) # 返回当前的状态list

    def remember(self, state, action, reward, next_state, game_over): # 获得一个五元组的数据后，把数据存储到存储器里
        self.memory.push((state, action, reward, next_state, game_over))

    def train_long_memory(self): # 拿多组数据进行训练
        memory_samples,indices,weight = self.memory.sample(BATCH_SIZE)
        # 如果数据量足够多，就随机选取样本训练，否则全部选来训练

        states, actions, rewards, next_states, game_overs = zip(*memory_samples) # 保存到矩阵后转置
        self.trainer.train_step(states, actions, rewards, next_states, game_overs,weight,self.memory,indices) # 用多组数据（矩阵形式）进行训练

    def train_short_memory(self, state, action, reward, next_state, game_over): # 拿一组数据进行训练
        self.trainer.train_step(state, action, reward, next_state, game_over)

