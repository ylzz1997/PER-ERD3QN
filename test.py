import argparse

from project_files.agent import GameAIAgent
from project_files.game import Game
from project_files.plotting import plot,plotsave
import numpy as np
import time
from project_files.model import Model
import torch

def test_snake(file_for_saving, show_plots):
    total_score =  0
    # 记录score， mean_scores, ttal_score, 最好记录
    agent = GameAIAgent() # 初始化网络、经验池等，实例化一个agent对象
    agent.agent.load_state_dict(torch.load("service_env1_model_3/model.pthgood_iter_4042"))
    game = Game(Train=False)         # 实例化一个游戏对象
    while True:           #开始路径规划
        # get the old state
        # time.sleep(0.1)
        old_state = agent.get_state(game) # 根据当前游戏界面获得当前的state

        move = agent.agent.make_action(old_state) # 根据当前state做出action
        agent.trainer.global_step += 1

        # print(agent.trainer.global_step)
        # perform move and get new state
        reward, game_over, score = game.step(move) # 执行action后，获取本次执行所得到的reward, game_over, score

        if game_over: # 游戏结束
            # train long memory, plotting
            game.reset() # 重新设置游戏
            total_score += score # 每玩一次总分数加上当前分数

            print(f'Game: {agent.trainer.n_iterations}, Score: {score}, 路径长度:{agent.trainer.global_step}')
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train your snake') #创建argparse对象
    parser.add_argument('-f', '--filename', type=str, help='Path to the file where to save model after training',
                        required=False, default='./model/model.pth')  #设置filename参数，应用是当参数进行传参
    parser.add_argument('-s', '--short_form', action='store_false',
                        help='Dont show plotting of scores and mean score while training')#设置short_form参数，应用是当参数进行传参

    args = parser.parse_args()  #创建parser

    test_snake(args.filename, args.short_form)
