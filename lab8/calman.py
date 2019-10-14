import os
import sys
import numpy as np
from functools import partial

#sys.path.append('')

class Calman():
    def __init__(self, X0, P0, F, Q, H, R):
        """
        Recurrent algorithm of Kalman filter
        X0 - initial estimate of state vector
        P0 - initial filtration error covariance matrix
        H - obseravation matrix
        F - transition matrix
        Q - covariance matrix of state noise
        R - covariance matrix of measurements noise η
        """
        self.X0 = X0
        self.P0 = P0
        # self.z  = z
        self.F  = F
        self.Q  = Q
        self.H = H
        self.R = R
        # self. =

        F7 = np.eye(2)
        for i in range(7):
            F7 = F7.dot(F)

        self.F7 = F7

    @staticmethod
    def predict(F, Q, x_filt, p_filt):

        x_pred = np.dot(F, x_filt)
        p_pred = np.dot(F.dot(p_filt), F.T) + Q
        return x_pred, p_pred

    @staticmethod
    def filter(H, R, x_pred, p_pred, z):
        try:
            x = np.dot(H.dot(p_pred), H.T) + R
            inverse = np.linalg.inv(x)
        except np.linalg.LinAlgError:
            return None
        else:
            ki = np.dot(p_pred, H.T).dot(inverse)
            residual = np.dot(ki, np.subtract(z, H.dot(x_pred)))
            x_filt = x_pred + residual
            p_filt = (np.subtract(np.eye(2), np.dot(ki, H)).dot(p_pred))
            return x_filt, p_filt, ki[0][0]

    def recurrent_calman_filter(self, z):
        self.z = z

        # size = z.shape[0]
        size = len(z)

        # X0, P0, z, F, Q, H, R
        x_filt = self.X0
        p_filt = self.P0

        gain = []
        smoothed = []
        ex7 = []

        predict = partial(Calman.predict, self.F, self.Q)
        filtr = partial(Calman.filter, self.H, self.R)

        diag1 = []
        for i in range(size):
            x_pred, p_pred = predict(x_filt, p_filt)
            # x_pred7 = np.dot(self.F7, x_pred)
            # ex7.append(x_pred7[0][0])

            x_filt, p_filt, k = filtr(x_pred, p_pred, z[i])
            smoothed.append(x_filt)
            gain.append(k)
            diag1.append(np.sqrt(p_filt[0, 0]))
        return smoothed, gain, diag1, ex7


# Plot results including
# true trajectory, measurements,
# filtered estimates of state vector X i .
# smoothed, gain, daig1, ex7 = \
#     recurrent_calman_filter(X0[:2], P00, z, F, q_pred, H, R, True)
def main():
    pass

if __name__ == "__main__":
    main()
