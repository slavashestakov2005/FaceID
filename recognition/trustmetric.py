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
        return [s1, s2, s3, s4]

    def draw_hist(self):
        plt.clf()
        fig = plt.figure(1)
        ax = fig.add_axes([0.13, 0.1, 0.6, 0.72])
        snsplot = sns.kdeplot(self.data['value'], shade=True)
        x_lim = snsplot.axes.get_xlim()
        y_lim = snsplot.axes.get_ylim()
        f0, = ax.plot([self.confidence, self.confidence], y_lim, color="magenta")
        ar = [-1, -1]
        f1 = ax.scatter(ar, ar, color="green")
        f2 = ax.scatter(ar, ar, color="red")
        f3 = ax.scatter(ar, ar, color="blue")
        f4 = ax.scatter(ar, ar, color="blue")
        f5 = ax.scatter(ar, ar, color="blue")
        f6 = ax.scatter(ar, ar, color="blue")
        st = self.get_statistics()
        plt.xlim(x_lim)
        plt.ylim(y_lim)
        plt.title("Коэффициент доверия")
        plt.xlabel("Значение")
        plt.ylabel('Частота')
        pc = self.find_value(self.confidence)
        pc = list(map(lambda x: str(round(x * 100, 2)), pc))
        ax.legend([f0, f1, f2, f3, f4, f5, f6], [str(round(self.confidence, 2)), pc[0] + '%', pc[1] + '%', *st],
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
