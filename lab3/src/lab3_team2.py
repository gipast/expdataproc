
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

from functools import partial

import smoothing as sm
from walking_model import Random_walking_model, rvm_alpha

from noised_signal import Measurements

from plotting import new_plot

def part1():
    sigmasTrue = [28, 97]
    alpha = rvm_alpha(sigmasTrue)

    model = Random_walking_model(10, sigmasTrue[0], 300)
    x = model.x

    Known_vals = Measurements(x, sigmasTrue[1])
    z = Known_vals.z

    RM = sm.RunningMean(z, alpha)
    r300 = RM.run(RM.m)

    Expsmoothing = sm.FB_exp_smoothing(z)
    exp300 = Expsmoothing.run_f(alpha)
    bexp300 = Expsmoothing.run_fb(alpha)

    new_plot('Plot result with backward exponential mean',
             'Measurements', 'Points',
             [[r300, 'Smoothed by running mean'],
             [z, 'Measurements'],
             [x, 'True trajectory']], show=False)
    plt.savefig(fname='FB exp smoothing.png')


    def p1_3():
        #1.3
        indTru = Known_vals.DevVarInd(x)
        print('Indicator tru trajectory:\n', indTru)

        indEx = Known_vals.DevVarInd(exp300)
        print('Indicator forward expotnentially smoothing:\n', indEx)

        indBex = Known_vals.DevVarInd(bexp300)
        print('Indicator backward expotnentially smoothing:\n', indBex)

        indR = Known_vals.DevVarInd(r300)
        print('Indicator running smoothing:\n', indR)

        indZ = Known_vals.DevVarInd(z)
        print('Indicator measurements:\n', indZ)

    p1_3()

#Part II

def part2():
    a = np.random.normal(0, np.sqrt(10), 300)
    sig = np.sqrt(500)

    def Trajectory(size, acc, t):
        vel = Random_walking_model.TrueTrajectory(0, acc * t)
        trajectory = Random_walking_model.TrueTrajectory(
            0, vel[:-1]*t + acc * t * t / 2)

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
    # b = [0.02, 0.08]
    b = [4, 4]
    chvals = np.round(np.linspace(0, z.shape[0] * 0.4, n))[1:]

    eval_params = partial(sm.eval_params, z, Known_vals.DevVarInd, b)

    bestm, resm = eval_params(chvals, RM.run)
    plot_f(z, bestm, RM.run, 'Running mean')
    plt.savefig(fname='Running mean best.png')

    Expsmoothing = sm.FB_exp_smoothing(z)

    probe_alpha = np.linspace(0, 1, n + 2)[1:-1]
    best_alpha, resalpha = eval_params(probe_alpha, Expsmoothing.run_fb)

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
    part1()
    part2()

if __name__ == "__main__":
    main()


