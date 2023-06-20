import argparse

from project_files.agent import GameAIAgent
from project_files.game import Game
from project_files.plotting import plot,plotsave
import numpy as np
import time
def train_snake(file_for_saving, show_plots):
    plot_scores, plot_mean_scores, total_score, record = [], [], 0, 0
    # 记录score， mean_scores, ttal_score, 最好记录
    agent = GameAIAgent() # 初始化网络、经验池等，实例化一个agent对象
    game = Game(Train=True)         # 实例化一个游戏对象
    reward_list = []               #保存一轮的所有得分
    rewards_list = []              #对每轮的得分求平均并保存
    while True:           #开始路径规划
        # get the old state
        # time.sleep(0.1)
        old_state = agent.get_state(game) # 根据当前游戏界面获得当前的state

        move = agent.trainer.make_action(old_state) # 根据当前state做出action
        agent.trainer.global_step += 1

        # perform move and get new state
        reward, game_over, score = game.step(move) # 执行action后，获取本次执行所得到的reward, game_over, score
        reward_list.append(reward)
        # get new state
        new_state = agent.get_state(game) # 在获取新的state

        agent.train_short_memory(old_state, move, reward, new_state, game_over) # 拿这一组数据训练一次
        agent.remember(old_state, move, reward, new_state, game_over) # 把这个四元组保存在memory里

        if game_over: # 游戏结束
            # train long memory, plotting
            game.reset() # 重新设置游戏
            reward_mean = np.mean(reward_list)
            rewards_list.append(reward_mean)
            agent.trainer.n_iterations += 1 # 迭代次数+1
            agent.train_long_memory() # 拿获得的多组数据进行训练

            if score > record: # 如果分数比最高纪录还好
                record = score # 更新一下最高纪录
                agent.trainer.q_eval.save(file_for_saving + f"good_iter_{agent.trainer.n_iterations}") # 保存一下模型

            total_score += score # 每玩一次总分数加上当前分数

            mean_score = total_score / agent.trainer.n_iterations # 计算平均分
            reward_list = []
            if show_plots:  # 展示图像
                plot_scores.append(score)
                plot_mean_scores.append(mean_score)

                plot(plot_scores, plot_mean_scores)

            print(f'Game: {agent.trainer.n_iterations}, Score: {score}, Mean Score: {mean_score}, Record: {record}')
        if agent.trainer.n_iterations % 1000 == 0:
            plotsave(agent.trainer.n_iterations)
            #np.save(f"平均奖励_{agent.trainer.n_iterations}.pth",np.array(rewards_list))
            #np.save(f"平均得分_{agent.trainer.n_iterations}.pth",np.array(plot_mean_scores))
        if agent.trainer.n_iterations == 6001:break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train your snake') #创建argparse对象
    parser.add_argument('-f', '--filename', type=str, help='Path to the file where to save model after training',
                        required=False, default='model/model.pth')  #设置filename参数，应用是当参数进行传参
    parser.add_argument('-s', '--short_form', action='store_false',
                        help='Dont show plotting of scores and mean score while training')#设置short_form参数，应用是当参数进行传参

    args = parser.parse_args()  #创建parser
    # import os
    # for i in range(1):
    #     train_snake(os.path.join(str(i),args.filename), args.short_form)
    train_snake(args.filename, args.short_form)