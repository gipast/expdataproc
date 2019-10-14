import numpy as np

class Smooth():
    def __init__(self, z):
        self.z = z

class RunningMean(Smooth):
    @staticmethod
    def smooth(z, m):
        x = np.zeros(len(z))
        sumFirst = 0
        sumLast = 0
        step = int((m-1)/2)
        for i in range(0, step):
            sumFirst += z[i]
            sumLast += z[len(z)-i-1]
        for i in range(step, len(z)-step):
            for j in range(i-step, i+step+1):
                x[i] += z[j]
            x[i] /= m
        for i in range(0, step):
            x[i] = sumFirst/step
            x[len(x)-i-1] = sumLast/step
        return x

    @staticmethod
    def window_width(alpha):
        return round((2-alpha)/alpha)

    def __init__(self, z, alpha):
        super().__init__(z)
        self.m = RunningMean.window_width(alpha)

    def run(self, m):
        ret = RunningMean.smooth(self.z, m)
        return ret

class FB_exp_smoothing(Smooth):
    @staticmethod
    def forward(alpfa, z):
        array = np.zeros(len(z))
        array[0] = 10
        for i in range(1, len(z)):
            array[i] = array[i - 1] + alpfa * (z[i] - array[i - 1])
        return array

    @staticmethod
    def backward(alpha, fz):
        array = np.zeros_like(fz)
        array[len(fz)-1] = fz[len(fz)-1]
        for i in range(len(fz)-2, -1, -1):
            array[i] = array[i+1]+alpha*(fz[i]-array[i+1])
        return array

    def run_f(self, alpha):
        res = FB_exp_smoothing.forward(alpha, self.z)
        return res

    def run_b(self, f, alpha):
        res = FB_exp_smoothing.backward(alpha, f)
        return res

    def run_fb(self, alpha):
        forward = FB_exp_smoothing.forward(alpha, self.z)
        res = FB_exp_smoothing.backward(alpha, forward)
        return res


def eval_params(z, idf, b, chvals, run):
        def neigh(vals, i):
            if i > 1:
                return vals[i-2: i+2]
            return(vals[:2])

        krits = []
        for ai in chvals:
            r = run(ai)
            ki = idf(r)
            res = np.sum([ki[i]*b[i] for i in range(2)])
            print('a: {} ki: {} res: {}'.format(
            	ai, [ki[i]*b[i] for i in range(2)], res))
            krits.append(res)
        idmin = np.argmin(krits, 0)
        ret = neigh(chvals, idmin)
        print("best:", ret, idmin, chvals)
        return ret, krits[idmin]
