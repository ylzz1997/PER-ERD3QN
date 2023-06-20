import matplotlib.pyplot as plt
from IPython import display


plt.ion()
# matplotlib.pyplot.ion()函数用于开启交互模式


def plot(scores, mean_scores):
    plt.clf()   # Clear figure清除所有轴，但是窗口打开，这样它可以被重复使用。
    plt.title('Training...') # 设置标题
    plt.xlabel('Number of games') # 设置x轴label
    plt.ylabel('Score')     # 设置y轴label
    plt.plot(scores, label='scores') # plot()方法一般是用来绘制线条的，包括直线、折线等
                                     # 绘制分数，并设置线条label
    plt.plot(mean_scores, label='mean score') # 绘制得分均值， 设置label
    plt.ylim(ymin=0) # ylim()函数用于获取或设置当前轴的y限制， y轴最小值为0

    plt.legend() # 设置图例添加对函数的描述

    try:
        plt.text(len(scores) - 1, scores[-1], str(scores[-1])) # text() 添加注释说明 参数：x, y, 内容
                                        # 在线条变换的最前面标注出数据
        plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
    except IndexError:
        pass

    plt.show(block=False) # show()函数用于显示所有图形。
    plt.pause(0.000001)

def plotsave(index):
    plt.savefig(f"图_{index}.png")
    # matplotlib.pyplot.pause(interval)
    # pause函数会检测当前是否有活动的图形对象，如果有，则会检测figure.stale（它代表图形已发生变化，需要重绘），
    # 如果为True则会重绘图形，并采用非阻塞形式显示图形，然后运行事件循环interval秒。如果没有活动图形，直接运行time.sleep函数，休眠interval秒。

