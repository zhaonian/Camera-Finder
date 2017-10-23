import math as m
import numpy as np
import lmfit as lf

NUM_POINT_REFERENCE = 5


class ProjectionEstimator:

        def __init__(self):
                return

        def __t_rot(self, rx, ry, rz):
                m_rx = np.matrix([[1, 0,         0],
                                  [0, m.cos(rx), -m.sin(rx)],
                                  [0, m.sin(rx), m.cos(rx)]])
                m_ry = np.matrix([[m.cos(ry),   0, m.sin(ry)],
                                  [0,           1, 0],
                                  [-m.sin(ry),  0, m.cos(ry)]])
                m_rz = np.matrix([[m.cos(rz),     -m.sin(rz),   0],
                                  [m.sin(rz),     m.cos(rz),    0],
                                  [0,               0,          1]])
                return m_rz * m_ry * m_rx

        def __reproj_error(self, params, real_p, screen_p):
                f = params['f']
                rx = params['rx']
                ry = params['ry']
                rz = params['rz']
                px = params['px']
                py = params['py']
                pz = params['pz']

                t_rot = self.__t_rot(-rx, -ry, -rz)
                t_trans = np.array([-px, -py, -pz])
                model_p = -f * t_rot * (real_p + t_trans[:, None])
                model_pw = model_p[2, :]
                model_p = model_p / model_pw

                diff = screen_p - model_p
                delta = np.sum(np.multiply(diff, diff), axis=0)
                return np.sqrt(delta)

        def compute_extrinsic(self, h, s, f, pattern_size):
                pattern_h_scale = 0.5 * pattern_size / 1000
                delta = 2 * pattern_h_scale / NUM_POINT_REFERENCE
                delta2 = 1 / NUM_POINT_REFERENCE
                real_p = np.mgrid[
                    -pattern_h_scale:pattern_h_scale:delta,
                    -pattern_h_scale:pattern_h_scale:delta,
                    0:1:1].reshape(3, -1)
                pattern_p = np.mgrid[
                    -0.5:0.5:delta2,
                        -0.5:0.5:delta2,
                        1:2:1].reshape(3, -1)

                screen_p = np.dot(h, pattern_p)
                screen_pw = screen_p[2, :]
                screen_p = screen_p / screen_pw
                screen_p[0:2, :] /= s
                # print(screen_p)

                rx_c = 0.0
                ry_c = 0.0
                rz_c = 0.0
                px_c = 0.0
                py_c = 0.0
                pz_c = 1.0

                min_cost = m.inf

                for i in range(0, 50):
                        params = lf.Parameters()
                        params.add('f', value=f / 1000, vary=False)
                        params.add('rx', value=np.random.normal(
                                   loc=rx_c, scale=m.pi / 4), min=0, max=m.pi / 2)
                        params.add('ry', value=0.0, vary=False)
                        params.add('rz', value=np.random.normal(
                                   loc=rz_c, scale=m.pi), min=0, max=2 * m.pi)
                        params.add('px', value=np.random.normal(
                                   loc=px_c, scale=5), min=-10, max=10)
                        params.add('py', value=np.random.normal(
                                   loc=py_c, scale=5), min=-10, max=10)
                        params.add('pz', value=np.random.normal(
                                   loc=pz_c, scale=2.5), min=0.01, max=5)

                        out = lf.minimize(
                            self.__reproj_error, params, args=(real_p, screen_p))

                        if out.chisqr < min_cost:
                                min_cost = out.chisqr
                                rx_c = out.params['rx'].value
                                rz_c = out.params['rz'].value
                                px_c = out.params['px'].value
                                py_c = out.params['py'].value
                                pz_c = out.params['pz'].value

                return rx_c, ry_c, rz_c, px_c, py_c, pz_c, min_cost

'''
pe = ProjectionEstimator()
h = np.matrix([[2.23422791e-02, -1.31393626e+00,   2.02942265e+03],
               [1.18337483e+00,   5.10424114e-02, -1.21915018e+03],
               [-2.35530371e-05,   1.81555398e-04,   1.00000000e+00]])
# h = np.matrix([[1, 0, 0],
#               [0, 1, 0],
#               [0, 0, 1]])
result = pe.compute_extrinsic(h, 3000, 32, 88)
print(result)
'''
