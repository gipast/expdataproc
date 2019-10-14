import numpy as np
from functools import partial

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

import smoothing as sm
from walking_model import Random_walking_model, rvm_alpha


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
                    ], show=False)
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
                ], show= False)
plt.savefig(fname='running mean 1.png')
