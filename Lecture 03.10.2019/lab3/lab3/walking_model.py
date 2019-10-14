
import numpy as np

class Random_walking_model():
    @staticmethod
    def TrueTrajectory(initial, diffs):
        array = [initial]
        for di in diffs:
            array.append(array[-1] + di)
        return np.array(array)

    def generate_signal(self, initial, sigma, n):
        diffs = np.random.normal(0, sigma, n-1)
        self.x = Random_walking_model.TrueTrajectory(initial, diffs)

    def __init__(self, initial, sigma, n):
        self.sigma = sigma
        self.generate_signal(initial, sigma, n)

def rvm_alpha(sig):
    '''linear regression koefficient(alpha)
    for random valking model process'''
    psi = sig[0]**2 / sig[1]**2

    alpha = (-psi + np.sqrt(psi**2 + 4 * psi)) / 2
    print('Optimal smoothing coefficient=', alpha)
    return alpha
