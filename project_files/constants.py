# 游戏内一些常量的设置
from collections import namedtuple # 使用了collections中的namedtuple作为坐标
from enum import Enum # 导入枚举类型
K = 1
GAMMA2 = 0.6
BLOCK_SIZE = 20     # 游戏界面的方块大小
SPEED = 10000     # 速度设置
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480 # 游戏屏幕的宽度和高度
MUTATION_RATE = 4000   # 保证随机性 # the higher this rate the more likely snake will "mutate" (make random moves not based on NN)
# 设置突变率
# 突变(Mutation)：使用该算子是为了避免群体中的一致性。突变随机改变基因型的一个值，随机更改现有解决方案，以避免搜索空间中的局部最小值。

MAX_MEMORY = 100_000    # 保存记录的最大记录个数
BATCH_SIZE = 1000       # 批次数
LEARNING_RATE = 0.001   # 学习率
GAMMA = 0.9             # 奖励的折扣参数

Point = namedtuple('Point', 'x y') # (类型名，具有的属性名)
# namedtuple是继承自tuple的子类。namedtuple创建一个和tuple类似的对象，而且对象拥有可访问的属性


class Colors:   # 设置颜色常量
    BLACK = (20, 20, 20)
    WHITE = (255, 255, 255)
    RED = (200, 30, 30)
    BLUE = (30, 30, 200)
    YELLOW = (200, 200, 50)
    GREEN = (30, 200, 30)


class Direction(Enum): # 定义方向的枚举类，用来表示方向
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'
    UP = 'UP'
    DOWN = 'DOWN'
