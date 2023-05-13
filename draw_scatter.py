import matplotlib.pyplot as plt


def draw(x, y, title='Title', xlabel='x', ylabel='y', filename='out.png', xlim=None, ylim=None):
    if xlim is None:
        xlim = [min(x), max(x)]
    if ylim is None:
        ylim = [min(y), max(y)]
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.plot(x, y)
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.savefig(filename)
    plt.show()

x = list(range(1, 21))
loss = [0.3464, 0.189, 0.1471, 0.1405, 0.1282, 0.1216, 0.1627, 0.1228, 0.1177, 0.1276, 0.1193, 0.102, 0.1011, 0.1787, 0.1016, 0.1178, 0.1488, 0.1409, 0.1049, 0.1147]
acc = [0.857, 0.9375, 0.9498, 0.9479, 0.9555, 0.9583, 0.9366, 0.9564, 0.9508, 0.9517, 0.9564, 0.9669, 0.9669, 0.9375, 0.9621, 0.9612, 0.9479, 0.9432, 0.9678, 0.965]
acc = [_ * 100 for _ in acc]
draw(x, loss, 'Потери', 'Эпоха', 'Потери', 'tests/eyes/loss.png', ylim=[0, 0.5])
draw(x, acc, 'Точноть', 'Эпоха', 'Точность в %', 'tests/eyes/accuracy.png', ylim=[50, 100])
