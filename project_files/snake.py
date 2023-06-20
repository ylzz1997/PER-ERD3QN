import numpy as np

from project_files.constants import BLOCK_SIZE, Direction, Point, SCREEN_HEIGHT, SCREEN_WIDTH


class Snake:
    def __init__(self, initial_size=3): # 初始化蛇
        if initial_size < 1:
            raise ValueError(f'Cant create snake with initial size = {initial_size}') # 初始长度太小

        self.head = Point(((SCREEN_WIDTH) // 2)+20, SCREEN_HEIGHT // 2) # 初始化蛇头在正中间
        self.direction = Direction.RIGHT # 初始方向向右

        self.blocks = []    # 蛇的身体， point类型
        self.walls = []
        self._place_wall()  #生成障碍物
        # for i in range(initial_size): # 初始化蛇身
        #     self.blocks.append(Point(self.head.x - i*BLOCK_SIZE, self.head.y))
        for i in range(initial_size): # 初始化蛇身
            self.blocks.append(Point(self.head.x - i *BLOCK_SIZE, self.head.y ))
            # print(self.head.x - i*BLOCK_SIZE, self.head.y)
    def move(self, action): # 蛇的移动
        # action = [straight, right, left]，蛇有三种action，不可以反向移动

        directions = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP] # 定义四种方向
        cur_dir_index = directions.index(self.direction) # 定义当前方向在directions中的索引
        # print(cur_dir_index)
        x = self.head.x
        y = self.head.y
        # 定义蛇头的坐标

        new_direction = None # 设置下一state的方向
        if np.array_equal(action, [1, 0, 0]):  # Go straight, no directions change
            # 判断列表是否相等
            new_direction = directions[cur_dir_index] # action是straight，还是原方向

        elif np.array_equal(action, [0, 1, 0]):  # right turn, r -> d -> l -> u
            new_dir_index = (cur_dir_index + 1) % 4 # action是向右，由于direction是按顺时针排列，所以索引+1循环即可
            new_direction = directions[new_dir_index]

        elif np.array_equal(action, [0, 0, 1]):  # left turn, r -> u -> l -> d
            new_dir_index = (cur_dir_index - 1) % 4 # action是向左， 索引-1循环即可
            new_direction = directions[new_dir_index]

        self.direction = new_direction # 更新蛇的下一state的移动方向

        # 根据新的移动方向更新坐标
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y) # 更新蛇头的位置
        self.blocks.insert(0, self.head) # 在整条蛇前插入一个头，代表蛇的移动
        # 在game的step里有蛇的长度变化的逻辑

    def pop(self): # 蛇尾去掉一个格子
        self.blocks.pop()

    def is_collision(self, point=None): # 判断参数point是否发生了碰撞
        if point is None:
            point = self.head # point初设为头（贪吃蛇头碰到自己或墙才会死）

        return point in self.walls or self._hit_boundary(point) or point in self.blocks[1:] # 撞到了边界墙壁或撞到了自己身上的其他部位

    @staticmethod
    def _hit_boundary(point): # 判断是否撞到了边界
        return point.x > SCREEN_WIDTH - BLOCK_SIZE \
               or point.x < 0 \
               or point.y > SCREEN_HEIGHT - BLOCK_SIZE \
               or point.y < 0 \
               # \续行符

    def __contains__(self, item): # 判断item是否在蛇身内
        return item in self.blocks

    def __iter__(self): # 返回蛇身所有点的位置——yield语句
        for point in self.blocks:
            yield point

    def __len__(self): # 获得蛇的长度
        return len(self.blocks)

    def _place_wall(self):
        # 左下角那一块
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
        #     self.walls.append(Point(25 * 20, (7 + i) * 20))
        # for i in range(4):
        #     self.walls.append(Point((13 + i) * 20, 3 * 20))
        #     self.walls.append(Point(16 * 20, (4 + i) * 20))
        #     self.walls.append(Point((28 + i) * 20, 3 * 20))
        #     self.walls.append(Point((28 + i) * 20, 4 * 20))
        #     self.walls.append(Point(27 * 20, (20 + i) * 20))
