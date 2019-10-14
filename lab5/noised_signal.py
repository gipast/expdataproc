import numpy as np

class Measurements():
    def __init__(self, x, sigma):
        n = len(x)
        noise = np.random.normal(0, sigma, n)
        self.z = x + noise

    def DevVarInd(self, x):
        #find deviation and variability indicators.
        # Id = 0
        # Iv = 0
        z = self.z
        # for i in range(len(z)):
        #     Id += (z[i]-x[i])**2
        Id = np.sum((z - x)**2)
        Iv = np.sum((x[2:] + x[:-2] - 2 * x[1:-1])**2)
        # for i in range(len(z)-2):
        #     Iv += (x[i+2] - 2*x[i+1] + x[i])**2
        return Id, Iv

    def ms_error(self, x):
        '''mean-squared error of estimation'''
        return np.sum((self.z - x)**2)
