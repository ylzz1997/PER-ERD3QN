import copy
import random

import torch
import torch.nn as nn
from torch.nn.functional import relu

from project_files.constants import GAMMA, LEARNING_RATE, GAMMA2,MUTATION_RATE

class Model(nn.Module):             # 搭建深度学习网络模型
    def __init__(self, input_size, hidden_size, output_size):   # 初始化
        super().__init__()

        self.layer1 = nn.Linear(input_size, hidden_size)    # layer1是从input_size->hidden_size的线性层
        self.A = nn.Linear(hidden_size, output_size)   # layer2是从input_size->hidden_size的线性层
        self.V = nn.Linear(hidden_size, 1)  # layer2是从input_size->hidden_size的线性层
        self.optimizer = torch.optim.Adam(self.parameters(), lr=LEARNING_RATE) # 使用Adam优化器进行优化(模型参数，学习率)

    def forward(self, x):            # 前向传播
        x = relu(self.layer1(x))     # 先经过线性层1, in_feature从input_size->hidden_size
        a = self.A(x)           # 在经过relu激活函数
        v = self.V(x)           # 在经过线性层2，infeature从hidden_size->out_size
        return v,a

    def getQ(self,x):
        a,v = self.forward(x)
        return a+v-torch.mean(a,dim=-1,keepdim=True)

    def save(self, filename='model.pth'):   # 保存模型
        print(filename)
        torch.save(self.state_dict(), filename) # 用把参数保存成字典的方式保存模型中的参数

    def make_action(self, state): # 执行action
        final_move = [0, 0, 0] # action_list
        _,a = self.forward(torch.tensor(state, dtype=torch.float)) # 网络输出是三个动作的价值期望
        move = torch.argmax(a).item() # 获取三个动作中值最大的一个的下标
        final_move[move] = 1    # 做出第move个动作

        return final_move # 返回最终的action列表

class Trainer:
    def __init__(self, input_size, hidden_size, output_size):
        self.q_eval = Model(input_size, hidden_size, output_size)
        self.q_target = Model(input_size, hidden_size, output_size)
        self.criterion = nn.MSELoss()       # 设置损失函数Loss
        self.max_idx = 0                    # 获取action的最大值
        self.get_action = []                # 获取DQN输出的三维action tensor
        self.dict = {}
        self.global_step = 0                #路径规划总步数
        self.n_iterations = 0               #路径规划轮数
        self.a = MUTATION_RATE

    def update_target(self):
        self.q_target = copy.deepcopy(self.q_eval)

    def make_action(self, state): # 执行action
        final_move = [0, 0, 0] # action_list
        if self.n_iterations == 2596:
            self.a = 0
        if random.randint(0, 10000) < self.a - self.n_iterations:
            # 再(0, 200)之间随机生成一个数，则随机做出axtion
            # 这种做法保证了蛇探索的随机如果小于<MUTATION_RATE-n_iterations性，防止收敛于局部最小值
            # 其中MUTATION_RATE - self.n_iterations会越来越小，那么采取随机动作的概率也会逐渐减小到0
            move = random.randint(0, 2) # 随机选择一个action
            final_move[move] = 1 # 做出第move个动作
        else:# 如果大于条件，则按照网络模型训练的玩法选择action
            _,a = self.q_eval(torch.tensor(state, dtype=torch.float)) # 网络输出是三个动作的价值期望
            move = torch.argmax(a).item() # 获取三个动作中值最大的一个的下标
            final_move[move] = 1    # 做出第move个动作

        return final_move # 返回最终的action列表


    def train_step(self, state, action, reward, next_state, game_over,weight=None,mem=None,ind=None): # 进行学习
        state = torch.tensor(state, dtype=torch.float) # 将state转成tensor
        action = torch.tensor(action, dtype=torch.float)# 将action转成tensor
        reward = torch.tensor(reward, dtype=torch.float) # 将reward转成tensor
        next_state = torch.tensor(next_state, dtype=torch.float) # 将next_state转成tensor
        if weight is not None:
            weight = torch.tensor(weight, dtype=torch.float)

        # 如果是训练一组数据，shape是n，此时state是标量，则要将tensor的shape增加一个维度
        # 多组数据不需要，因为shape是 1xn的
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            next_state = torch.unsqueeze(next_state, 0)
            game_over = (game_over, ) # 元组只有一个元素需要加,
            # 全部增加一个维度


        # newQ = Reward + y * max(next_predicted) # 折扣价值 y是折扣率
        target = self.q_target.getQ(state)
        for idx in range(len(game_over)):
            q_new = reward[idx]
            if not game_over[idx]:  # 如果idx步游戏还没结束，就要按照q_learning的公式计算Q(s, a)
                q_1 = self.q_eval.getQ(next_state[idx])
                q_2 = self.q_target.getQ(next_state[idx])
                q_1 = torch.max(q_1,0)[1]
                self.max_idx = q_1.item()
                q_ = q_2.gather(0,q_1)
                ste = str(state[idx].tolist())
                if ste not in self.dict:
                    self.dict[ste] = [0, 0, 0]
                self.dict[ste] += action[idx]
                q_new = reward[idx] + GAMMA * q_
                q_new = q_new * GAMMA2 + (1 - GAMMA2) * q_new * (1 / (1 + self.dict[ste][self.max_idx]))
            else:
                self.dict = {}
            target[idx][torch.argmax(action).item()] = q_new
        pred = self.q_eval.getQ(state)  # 获得主网络预测的action tensor
        self.q_eval.optimizer.zero_grad()  # 梯度清空
        if mem != None:
            td_error = target - pred  # 计算损失函数
            p = torch.abs(td_error.sum(-1)+1e-6)
            loss = torch.mean(td_error*weight[:,None])
            mem.update_priorities(ind, p.detach().cpu().numpy())
        else:
            loss = self.criterion(target,pred)
        loss.backward()  # 反向传播求梯度

        self.q_eval.optimizer.step()  # 更新权重参数

        if self.global_step % 200 == 0:
            self.update_target()
