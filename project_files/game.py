import math
import random
import numpy as np
import pygame

from project_files.constants import Colors, BLOCK_SIZE, Point, SPEED, SCREEN_HEIGHT, SCREEN_WIDTH, K, Direction
from project_files.snake import Snake

pygame.init()
font = pygame.font.SysFont('Arial', 25)  # 设置字体(字体名，大小)


class Game:  # 游戏界面及游戏设置
    def __init__(self, speed=SPEED, Train=True):  # SPEED是蛇的速度，速度作为参数输入
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 设置界面的宽度和高度
        pygame.display.set_caption('Snake')  # 设置界面的标题Snake

        self.Train=Train
        self.index = 0   #随后进行测试时使用
        self.clock = pygame.time.Clock()  # 帮助跟踪时间的对象,也用在网页刷新上
        self.speed = speed  # 设置速度(参数导入)
        self.snake, self.score, self.food, self.frame_iteration = None, None, None, None
        #self.snake是蛇的身体，food是食物，score是得分，frame_iteration是游戏的持续帧
        self.walls = []   #生成的所有障碍物
        #下面的self.food_list_1和self.food_list_2是在最后测试时使用的，为生成固定的是个目标
        self.food_list_1 = [Point(26 * 20, 13 * 20), Point(23 * 20, 7 * 20), Point(17 * 20, 3 * 20), Point(5 * 20, 8 * 20),
                            Point(1*20, 16 * 20), Point(4 * 20, 21 * 20), Point(12 * 20, 18 * 20), Point(19 * 20, 22 * 20),
                            Point(23 * 20, 16 * 20), Point(31 * 20, 23 * 20)]

        self.food_list_2 = [Point(28 * 20, 11 * 20), Point(24 * 20, 6 * 20), Point(17 * 20, 6 * 20), Point(8 * 20, 2 * 20),
                            Point(0, 6 * 20), Point(0, 23 * 20), Point(6 * 20, 20 * 20),
                            Point(16 * 20, 20 * 20),
                            Point(26 * 20, 15 * 20), Point(31 * 20, 23 * 20)]
        self._place_a_wall()
        # 初始的蛇，分数，食物
        self.reset()  # 重置游戏参数
        self._update_screen()

    def reset(self):  # 重置游戏参数的函数，将设置后的路径规划环境，比如障碍物，目标等信息进行更新
        self.snake = Snake(initial_size=3)  # 蛇的长度重置为3，最开始初始化蛇的信息
        # print(self.snake)
        self.score = 0  # 分数重置为0
        self.food = None  # 食物重置为空
        self.index = 0
        self._place_food(train=self.Train)  # 随机出现食物，生成食物的坐标
        self.frame_iteration = 0  # 定义游戏的持续帧


    def _place_food(self, train):  # 设置食物
        if train:
            x = random.randint(0, (self.display.get_width() - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.display.get_height() - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            # 随机生成食物，保证食物在界面内
            # BLOCK_SIZE 常量中设置的一个格子的大小
            self.food = Point(x, y)  # 食物定义为点类
            if self.food in self.snake or self.food in self.walls:
                self._place_food(train=self.Train)
        else:
            self.food = self.food_list_1[self.index] # env1
            self.index += 1
            # self.food = self.food_list_2[self.index] # env2

    def _place_a_wall(self):  #生成路径规划环境中的障碍物
         # env1
         for i in range(3):
             self.walls.append(Point((2 + i) * 20, 16 * 20))
         for i in range(5):
             self.walls.append(Point(4 * 20, (16 + i) * 20))

         # 右下角那一块
         for i in range(4):
             self.walls.append(Point((19 + i) * 20, 16 * 20))
         for i in range(5):
             self.walls.append(Point(19 * 20, (17 + i) * 20))

         # 上面一块
         for i in range(3):
             self.walls.append(Point((5 + i) * BLOCK_SIZE, 9 * BLOCK_SIZE))
             self.walls.append(Point((15 + i) * BLOCK_SIZE, (2 + i) * BLOCK_SIZE))  # 上面斜块
         for i in range(4):
             self.walls.append(Point((18 + i) * 20, 5 * 20))  # 与斜块相连都横块1
             self.walls.append(Point(26 * 20, (9 + i) * 20))  # 竖块2
         for i in range(5):
             self.walls.append(Point((22 + i) * 20, 8 * 20))  # 横块2
         for i in range(3):
             self.walls.append(Point(22 * 20, (5 + i) * 20))  # 竖块1


        # env2

        # self.walls.append(Point(26 * 20, 14 * 20))
        # self.walls.append(Point(28 * 20, 12 * 20))
        # for i in range(3):
        #     self.walls.append(Point(i * 20, 10 * 20))
        #     self.walls.append(Point(3 * 20, (21 + i) * 20))
        #     self.walls.append(Point((6 + i) * 20, 18 * 20))
        #     self.walls.append(Point((6 + i) * 20, 19 * 20))
        #     self.walls.append(Point((17 + i) * 20, 7 * 20))
        #     self.walls.append(Point((16 + i) * 20, 21 * 20))
        #     self.walls.append(Point((13 + i) * 20, (18 + i) * 20))
        #     self.walls.append(Point((19 + i) * 20, (20 - i) * 20))
        #     self.walls.append(Point((26 + i) * 20, (12 + i) * 20))
        #     self.walls.append(Point(3 * 20, (2 + i) * 20))
        # for i in range(4):
        #     self.walls.append(Point(7 * 20, (9 + i) * 20))
        #     self.walls.append(Point((13 + i) * 20, 3 * 20))
        #     self.walls.append(Point(16 * 20, (4 + i) * 20))
        #     self.walls.append(Point((28 + i) * 20, 3 * 20))
        #     self.walls.append(Point((28 + i) * 20, 4 * 20))
        #     self.walls.append(Point(27 * 20, (20 + i) * 20))
        # for i in range(2):
        #     self.walls.append(Point((8 + i) * 20, 12 * 20))
        #     self.walls.append(Point(3 * 20, i * 20))
        #     self.walls.append(Point(4 * 20, i * 20))
        #     self.walls.append(Point((9 + i) * 20, 2 * 20))
        #     self.walls.append(Point((23 + i) * 20, 2 * 20))
        #     self.walls.append(Point(25 * 20, (7 + i) * 20))



        # self.walls.append(Point(26 * 20, 14 * 20))
        # self.walls.append(Point(28 * 20, 12 * 20))
        # for i in range(3):
        #     self.walls.append(Point(i * 20, 10 * 20))
        #     self.walls.append(Point(3 * 20, (21 + i) * 20))
        #     self.walls.append(Point((6 + i) * 20, 18 * 20))
        #     self.walls.append(Point((6 + i) * 20, 19 * 20))
        #     self.walls.append(Point(7 * 20, (9 + i) * 20))
        #     self.walls.append(Point((7 + i) * 20, 12 * 20))
        #     self.walls.append(Point((17 + i) * 20, 7 * 20))
        #     self.walls.append(Point((16 + i) * 20, 21 * 20))
        #     self.walls.append(Point((13 + i) * 20, (18 + i) * 20))
        #     self.walls.append(Point((19 + i) * 20, (20 - i) * 20))
        #     self.walls.append(Point(3 * 20, (2 + i) * 20))
        #     self.walls.append(Point((26 + i) * 20, (12 + i) * 20))
        # for i in range(2):
        #     self.walls.append(Point(3 * 20, i * 20))
        #     self.walls.append(Point(4 * 20, i * 20))
        #     self.walls.append(Point((9 + i) * 20, 2 * 20))
        #     self.walls.append(Point((23 + i) * 20, 2 * 20))
        #     self.walls.append(Point(24 * 20, (7 + i) * 20))
        # for i in range(4):
        #     self.walls.append(Point((13 + i) * 20, 3 * 20))
        #     self.walls.append(Point(16 * 20, (4 + i) * 20))
        #     self.walls.append(Point((28 + i) * 20, 3 * 20))
        #     self.walls.append(Point((28 + i) * 20, 4 * 20))
        #     self.walls.append(Point(27 * 20, (20 + i) * 20))

    def get_other_Reward(self, dir):
        dis = math.sqrt((self.snake.head.x - self.food.x) / 20 * (self.snake.head.x - self.food.x) / 20 +
                        (self.snake.head.y - self.food.y) / 20 * (self.snake.head.y - self.food.y) / 20)
        stra_reward = 0
        left_reward = 0
        right_reward = 0
        if dir == Direction.RIGHT:
            # 向右
            short_dis = self.food.x - self.snake.head.x
            cos_theta = short_dis / dis
            stra_reward = K * cos_theta / dis

            # 向上
            short_dis = self.snake.head.y - self.food.y
            cos_theta = short_dis / dis
            left_reward = K * cos_theta / dis

            # 向下
            short_dis = self.food.y - self.snake.head.y
            cos_theta = short_dis / dis
            right_reward = K * cos_theta / dis

        elif dir == Direction.UP:
            # 向上
            short_dis = self.snake.head.y - self.food.y
            cos_theta = short_dis / dis
            stra_reward = K * cos_theta / dis

            # 向左
            short_dis = self.snake.head.x - self.food.x
            cos_theta = short_dis / dis
            left_reward = K * cos_theta / dis

            # 向右
            short_dis = self.food.x - self.snake.head.x
            cos_theta = short_dis / dis
            right_reward = K * cos_theta / dis

        elif dir == Direction.DOWN:
            # 向下
            short_dis = self.food.y - self.snake.head.y
            cos_theta = short_dis / dis
            stra_reward = K * cos_theta / dis

            # 向右
            short_dis = self.food.x - self.snake.head.x
            cos_theta = short_dis / dis
            left_reward = K * cos_theta / dis

            # 向左
            short_dis = self.snake.head.x - self.food.x
            cos_theta = short_dis / dis
            right_reward = K * cos_theta / dis

        else:
            # 向左
            short_dis = self.snake.head.x - self.food.x
            cos_theta = short_dis / dis
            stra_reward = K * cos_theta / dis

            # 向下
            short_dis = self.food.y - self.snake.head.y
            cos_theta = short_dis / dis
            left_reward = K * cos_theta / dis

            # 向上
            short_dis = self.snake.head.y - self.food.y
            cos_theta = short_dis / dis
            right_reward = K * cos_theta / dis

        return stra_reward, left_reward, right_reward

    def step(self, action):  # 游戏执行一步action
        self.frame_iteration += 1  # 游戏帧数

        for event in pygame.event.get():  # 遍历事件队列（建立的一个队列，用于缓存并派发所有事件原则上先到先处理）
            if event.type == pygame.QUIT:  # 如果碰到结束事件(手动结束)就退出游戏
                pygame.quit()
                quit()

        self.snake.move(action)  # 让蛇执行action

        game_over, reward = False, 0  # 设置game_over变量和reward变量
        self._update_screen()  # 更新游戏界面
        if self.snake.head in self.walls or self.snake.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        # 蛇创死或游戏时间过长，则结束游戏，获得负奖励，返回reward， game_over score

        if self.snake.head == self.food:  # 如果蛇吃到食物，分数就+1，并重新设置食物
            self.score += 1
            if self.index >= 10:
                game_over = True
            else :
                self._place_food(train=self.Train)
            reward = 50
        else:
            self.snake.pop()  # 由于在snake move逻辑里蛇每移动一步长度都+1，所以如果蛇没有吃到食物，应该每一步同时让蛇的长度-1
            stra_reward, left_reward, right_reward = self.get_other_Reward(self.snake.direction)
            if np.array_equal(action, [1, 0, 0]):
                reward = stra_reward
            elif np.array_equal(action, [0, 1, 0]):
                reward = right_reward
            else:
                reward = left_reward

        self.clock.tick(self.speed)  # 这个函数的参数就是每秒调用n次tick函数，一般设置在循环中，限制循环每秒的循环次数。从而达到设置页面刷新率的效果。
        return reward, game_over, self.score  # 返回奖励， 游戏介绍？,分数, 游戏图像

    def _update_screen(self):  # 更新游戏界面
        self.display.fill(Colors.BLACK)  # 将背景填充为黑色

        for pt in self.snake:  # 画蛇的所有部分
            pygame.draw.rect(self.display, Colors.RED, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))  # drawing walls
            pygame.draw.circle(self.display, Colors.YELLOW, (pt.x + (BLOCK_SIZE // 2), pt.y + (BLOCK_SIZE // 2)), 4)
            # 画蛇头和蛇身，红色矩形和黄色圆形搭配
        for pt in self.walls:
            pygame.draw.rect(self.display, Colors.GREEN, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.circle(self.display, Colors.BLUE, (pt.x + (BLOCK_SIZE // 2), pt.y + (BLOCK_SIZE // 2)), 4)
        pygame.draw.rect(self.display, Colors.BLUE, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        # 绘制食物

        text = font.render(f'Score: {self.score}', True, Colors.WHITE)  # 标注分数(标题：分数， 抗锯齿开启， 文字颜色)
        self.display.blit(text, [0, 0])  # 将text放在[0,0]位置
        pygame.display.flip()  # 更新整个对象到屏幕上
