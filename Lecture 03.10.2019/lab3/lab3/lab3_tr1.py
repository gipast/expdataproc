# Assignment 3
# Determining and removing drawbacks of exponential and running mean.
# Team 2:
#     Ekaterina Karmanova
#     Timur Chikichev
#     Iaroslav Okunevich
#     Nikita Mikhailovskiy
#
# Skoltech, 04.10.2019

import os
try:
	os.chdir(os.path.join(os.getcwd(), 'lab3'))
	print(os.getcwd())
except:
	pass

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

import smoothing as sm
from walking_model import Random_walking_model, rvm_alpha

class Measurements():
    def __init__(self, x, sigma):
        n = len(x)
        noise = np.random.normal(0, sigma, n)
        self.z = x + noise

    def DevVarInd(self, x):
        #find deviation and variability indicators.
        Id = 0
        Iv = 0
        z = self.z
        for i in range(len(z)):
            Id += (z[i]-x[i])**2
        for i in range(0, len(z)-2):
            Iv += (x[i+2] - 2*x[i+1] + x[i])**2
        return Id, Iv


def draw_plots(plots=[], show = False):
    for pi, plabel in plots:
        plt.plot(pi, label=plabel)

    plt.legend()
    if show:
        plt.show()

def new_plot(title, xl, yl, plots = [], show = False):
    figure(num=None, figsize=(10, 5), dpi=100,
           facecolor='w', edgecolor='k')
    plt.title(title)
    plt.ylabel(yl)
    plt.xlabel(xl)

    draw_plots(plots, show)

#Part II
def part2():
    a = np.random.normal(0, np.sqrt(10), 300)
    sig = np.sqrt(500)

    def Trajectory(size, acc, t):
        vel = Random_walking_model.TrueTrajectory(0, acc * t)
        trajectory = Random_walking_model.TrueTrajectory(0, vel * t + acc * t * t / 2)

        new_plot('Plot result', 'Measurement', 'Points',
        [
            [acc, 'Acceleration'],
            [vel, 'Velosity'],
            [trajectory, 'Trajectory']
        ], show = False)
        plt.savefig(fname='Trajectory.png')
        return trajectory

    traject = Trajectory(300, a, 0.1)
    Known_vals = Measurements(traject, sig)
    z = Known_vals.z

    RM = sm.RunningMean(z, 1)

    new_plot('Plot result',
            'Measurements', 'Points', [
                [traject, 'Trajectory'],
                [z, 'Measure']
            ], show = False)
    plt.savefig(fname = 'running mean 1.png')

    def eval_params(z, chvals, b, run):
        krits = []
        for ai in chvals:
            r = run(ai)
            ki = Known_vals.DevVarInd(r)
            res = np.sum([ki[i]*b[i] for i in range(2)])
            print('a: {} ki: {} res: {}'.format(
            	ai, [ki[i]*b[i] for i in range(2)], res))
            krits.append(res)
        idmin = np.argmin(krits, 0)
        ret = chvals[idmin - 1: idmin + 2]
        return ret, krits[idmin]

    def plot_f(z, chvals, run, aname):
        new_plot('Plot result', 'Number', 'Count')
        plt.plot(z, label='Measure', c='lightgrey')
        for ai in chvals:
            r = run(ai)
            ki = Known_vals.DevVarInd(r)
            res = np.sum([ki[i]*b[i] for i in range(2)])
            plt.plot(r, label='{}, val: {}, res: {}'.format(aname, ai, res))
        plt.legend()
        # plt.show()

    n = 10
    b = [0.02, 0.08]
    chvals = np.round(np.linspace(0, z.shape[0] * 0.4, n))[1:]
    bestm, resm = eval_params(z, chvals, b, RM.run)
    plot_f(z, bestm, RM.run, 'Running mean')
    plt.savefig(fname='Running mean best.png')

    Expsmoothing = sm.FB_exp_smoothing(z)

    probe_alpha = np.linspace(0, 1, n + 2)[1:-1]
    best_alpha, resalpha = eval_params(z, probe_alpha, b, Expsmoothing.run_fb)

    print("bestm: {}, best_alpha: {}".format(bestm, best_alpha))
    plot_f(z, best_alpha, Expsmoothing.run_fb, 'exp fb smoothing')

    plt.savefig(fname='exp fb smoothing best.png')

    def proper_choise(m_vals, alpha_vals):
        m = m_vals
        a = alpha_vals

        res = 'exponential' if a < m else 'running mean'
        print("mean:{}, exp:{}".format(m_vals, alpha_vals))
        print(res)

    proper_choise(resm, resalpha)

def main():
    part2()

if __name__ == "__main__":
    main()


