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
        self.confidence, self.precision, self.left, self.right = 0, 0, 0, 0
        self.is_closed_plot, self.fig, self.ax = False, None, None

    def load_from_model(self, model):
        self.confidence, self.precision = model.confidence, model.precision
        self.left, self.right = model.left, model.right

    def open_window(self):
        self.fig = plt.figure(0)

    def save_to_model(self, model):
        model.confidence, model.precision = self.confidence, self.precision
        model.left, model.right = self.left, self.right

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
        plt.ylim([self.left, self.right])

    def show(self):
        if len(self.x) > 1:
            self.end_time = self.x[-1]
            while self.end_time - self.x[1] > Config.PLOT_TIME:
                self.pop()
        if len(self.x) and self.x[-1] > Config.PLAY_TIME or not plt.fignum_exists(0):
            self.is_closed_plot = True
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

    def get_result(self):
        return self.find_value(self.confidence)[0] * 100 >= self.precision

    def get_message(self):
        return 'Свой' if self.get_result() else 'Чужой'

    def get_statistics(self):
        s1 = 'Min: {}'.format(str(round(self.v[0], 2)) if len(self.v) else 'unknown')
        s2 = 'Max: {}'.format(str(round(self.v[-1], 2)) if len(self.v) else 'unknown')
        s3 = 'Average: {}'.format(str(round(sum(self.v) / len(self.v), 2)) if len(self.v) else 'unknown')
        s4 = 'Median: {}'.format(str(round(self.v[len(self.v) // 2], 2)) if len(self.v) else 'unknown')
        s5 = 'A. time: {}'.format(str(round(self.x[-1] * 1000 / len(self.v))) + 'ms' if len(self.v) else 'unknown')
        s6 = self.get_message()
        return [s1, s2, s3, s4, s5, s6]

    def close_plot(self):
        plt.close()
        self.v.sort()
        self.data = pd.DataFrame.from_dict({'value': self.v})

    def draw_hist(self):
        plt.clf()
        fig = plt.figure(1)
        ax = fig.add_axes([0.13, 0.1, 0.6, 0.72])
        snsplot = sns.kdeplot(self.data['value'], shade=True)
        x_lim = snsplot.axes.get_xlim()
        y_lim = snsplot.axes.get_ylim()
        ar = [-1, -1]

        f0, = ax.plot([self.confidence, self.confidence], y_lim, color="magenta")
        f1 = ax.scatter(ar, ar, color="green")
        f2 = ax.scatter(ar, ar, color="red")
        f3 = ax.scatter(ar, ar, color="blue")
        f4 = ax.scatter(ar, ar, color="blue")
        f5 = ax.scatter(ar, ar, color="blue")
        f6 = ax.scatter(ar, ar, color="blue")
        f7 = ax.scatter(ar, ar, color="blue")
        f8 = ax.scatter(ar, ar, color=("green" if self.get_result() else 'red'))

        st = self.get_statistics()
        plt.xlim(x_lim)
        plt.ylim(y_lim)
        plt.title("Коэффициент доверия")
        plt.xlabel("Значение")
        plt.ylabel('Частота')
        pc = self.find_value(self.confidence)
        pc = list(map(lambda x: str(round(x * 100, 2)), pc))
        val = [str(round(self.confidence, 2)), pc[0] + '%', pc[1] + '%', *st]
        ax.legend([f0, f1, f2, f3, f4, f5, f6, f7, f8], val, bbox_to_anchor=(1, 0.5), loc='center left')
        return snsplot, ax

    def show_hist(self, filename=None):
        print('====== Результаты =====')
        print('\n'.join(self.get_statistics()))
        print('======   Конец    =====')
        input('Теперь посмотрим на распределение «коэффициента доверия». ')
        input('Вы можете нажимать на график чтобы узнать процентное распределение «коэффициента доверия». ')
        input('Нажмите что-нибудь, чтобы мы наконец вывели Вам график. ')

        def onclick(event):
            x, y = event.xdata, event.ydata
            if x is not None:
                self.confidence = x
                self.draw_hist()
                plt.show()

        ax, snsplot = self.draw_hist()
        snsplot.get_figure().canvas.mpl_connect('button_release_event', onclick)
        if filename:
            snsplot.figure.savefig(filename, format="png")
        plt.show()
