import random
import matplotlib.pyplot as plt


heads_tails = [0, 0]

for _ in range(10000):
    heads_tails[random.randint(0, 1)] += 1
    plt.bar(["Heads", "Tails"], heads_tails, color=["red", "blue"])
    plt.pause(0.08)  # 使用暂停达到一个暂存的效果，下一个图片出来就像是连续出来的动画
