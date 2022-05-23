from collections import deque
from recognition import Config
import matplotlib.pyplot as plt
from drawnow import drawnow
from time import time
import seaborn as sns
import pandas as pd


class TrustMetric:
    def __init__(self):
        self.x, self.y, self.v, self.data = deque(), deque(), [], []
        self.start = time()
        self.end_time = self.start
        self.confidence = Config.CV_CONFIDENCE

    def append(self, trust, tim):
        self.x.append(tim - self.start)
        self.y.append(trust)
        self.v.append(trust)

    def pop(self):
        self.x.popleft()
        self.y.popleft()

    def make_fig(self):
        plt.title("Коэффициент доверия")
        plt.xlabel("Время")
        plt.ylabel("Значение")
        plt.grid()
        plt.plot(self.x, self.y)
        x = [self.end_time - Config.PLOT_TIME, self.end_time]
        plt.plot(x, [self.confidence, self.confidence], color="magenta")
        plt.xlim(x)
        plt.ylim([40, 160])

    def show(self):
        if len(self.x):
            self.end_time = self.x[-1]
            while self.end_time - self.x[0] > Config.PLOT_TIME:
                self.pop()
        drawnow(self.make_fig)

    def find_value(self, v):
        ln = len(self.v)
        if not ln:
            return 0, 0
        if v <= self.v[0]:
            return 0, 1
        l, r = 0, ln
        while l + 1 < r:
            m = (l + r) // 2
            if self.v[m] < v:
                l = m
            else:
                r = m
        l += 1
        return l / ln, 1 - l / ln

    def get_statistics(self):
        s1 = 'Min: {}'.format(round(self.v[0], 2) if len(self.v) else 'unknown')
        s2 = 'Max: {}'.format(round(self.v[-1], 2) if len(self.v) else 'unknown')
        s3 = 'Average: {}'.format(round(sum(self.v) / len(self.v), 2) if len(self.v) else 'unknown')
        s4 = 'Median: {}'.format(round(self.v[len(self.v) // 2], 2) if len(self.v) else 'unknown')
        s5 = 'A. time: {}'.format(str(round(self.x[-1] * 1000 / len(self.v))) + 'ms' if len(self.v) else 'unknown')
        return [s1, s2, s3, s4, s5]

    def draw_hist(self):
        plt.clf()
        fig = plt.figure(1)
        ax = fig.add_axes([0.13, 0.1, 0.6, 0.72])
        snsplot = sns.kdeplot(self.data['value'], shade=True)
        x_lim = snsplot.axes.get_xlim()
        y_lim = snsplot.axes.get_ylim()
        ar = [-1, -1]
        f0, = ax.plot([self.confidence, self.confidence], y_lim, color="magenta")
        f01, = ax.plot([self.confidence - 5, self.confidence - 5], y_lim, color="magenta")
        f02, = ax.plot([self.confidence - 10, self.confidence - 10], y_lim, color="magenta")
        f03, = ax.plot([self.confidence - 15, self.confidence - 15], y_lim, color="magenta")
        f04, = ax.plot([self.confidence - 20, self.confidence - 20], y_lim, color="magenta")

        f1 = ax.scatter(ar, ar, color="green")
        f2 = ax.scatter(ar, ar, color="red")
        f11 = ax.scatter(ar, ar, color="green")
        f21 = ax.scatter(ar, ar, color="red")
        f12 = ax.scatter(ar, ar, color="green")
        f22 = ax.scatter(ar, ar, color="red")
        f13 = ax.scatter(ar, ar, color="green")
        f23 = ax.scatter(ar, ar, color="red")
        f14 = ax.scatter(ar, ar, color="green")
        f24 = ax.scatter(ar, ar, color="red")

        f3 = ax.scatter(ar, ar, color="blue")
        f4 = ax.scatter(ar, ar, color="blue")
        f5 = ax.scatter(ar, ar, color="blue")
        f6 = ax.scatter(ar, ar, color="blue")
        f7 = ax.scatter(ar, ar, color="blue")
        st = self.get_statistics()
        plt.xlim(x_lim)
        plt.ylim(y_lim)
        plt.title("Коэффициент доверия")
        plt.xlabel("Значение")
        plt.ylabel('Частота')
        pc = self.find_value(self.confidence)
        pc = list(map(lambda x: str(round(x * 100, 2)), pc))
        pc1 = self.find_value(self.confidence - 5)
        pc1 = list(map(lambda x: str(round(x * 100, 2)), pc1))
        pc2 = self.find_value(self.confidence - 10)
        pc2 = list(map(lambda x: str(round(x * 100, 2)), pc2))
        pc3 = self.find_value(self.confidence - 15)
        pc3 = list(map(lambda x: str(round(x * 100, 2)), pc3))
        pc4 = self.find_value(self.confidence - 20)
        pc4 = list(map(lambda x: str(round(x * 100, 2)), pc4))
        val = [str(round(self.confidence, 2)), pc[0] + '%', pc[1] + '%', str(round(self.confidence - 5, 2)), pc1[0] +
               '%', pc1[1] + '%', str(round(self.confidence - 10, 2)), pc2[0] + '%', pc2[1] + '%',
               str(round(self.confidence - 15, 2)), pc3[0] + '%', pc3[1] + '%', str(round(self.confidence - 20, 2)),
               pc4[0] + '%', pc4[1] + '%', *st]
        ax.legend([f0, f1, f2, f01, f11, f21, f02, f12, f22, f03, f13, f23, f04, f14, f24, f3, f4, f5, f6, f7], val,
                  bbox_to_anchor=(1, 0.5), loc='center left')
        return snsplot

    def show_hist(self):
        self.v.sort()
        self.data = pd.DataFrame.from_dict({'value': self.v})
        print('====== Results: =====')
        print('\n'.join(self.get_statistics()))
        print('======   End    =====')
        input('Input something:')

        def onclick(event):
            x, y = event.xdata, event.ydata
            if x is not None:
                self.confidence = x
                self.draw_hist()
                plt.show()

        snsplot = self.draw_hist()
        snsplot.get_figure().canvas.mpl_connect('button_release_event', onclick)
        plt.show()
