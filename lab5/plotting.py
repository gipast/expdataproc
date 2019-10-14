import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def draw_plots(plots=[], show=False):
    for pi, plabel in plots:
        plt.plot(pi, label=plabel)

    plt.legend()
    if show:
        plt.show()


def new_plot(title, xl, yl, plots=[], show=False):
    figure(num=None, figsize=(10, 5), dpi=100,
           facecolor='w', edgecolor='k')
    plt.title(title)
    plt.ylabel(yl)
    plt.xlabel(xl)

    draw_plots(plots, show)
