__author__ = 'Mikhail Vilgelm'

import numpy as np
import math, os
import matplotlib.pyplot as plt
import matplotlib
from scipy import special


def q_a(lmb, m):
    return 1 - math.exp(-lmb/m)


def get_Q_a(m, lmb, i, n):
    return special.binom(m-n, i) * ((1-q_a(lmb, m)) ** (m-n-i)) * (q_a(lmb, m) ** i)


def get_Q_r(q_r, i, n):
    return special.binom(n, i) * ((1-q_r) ** (n-i)) * (q_r ** i)


def get_P_n_nplusi(params, n, nplusi):
    i = nplusi - n
    if (i >= 2) and (i <= (m-n)):
        return get_Q_a(params['m'], params['lmb'], i, n)
    elif i == 1:
        return get_Q_a(params['m'], params['lmb'], 1, n)*(1 - get_Q_r(params['q_r'], 0, n))
    elif i == 0:
        return get_Q_a(params['m'], params['lmb'], 1, n)*get_Q_r(params['q_r'], 0, n) + \
               get_Q_a(params['m'], params['lmb'], 0, n)*(1 - get_Q_r(params['q_r'], 1, n))
    elif i == -1:
        return get_Q_a(m, params['lmb'], 0, n)*get_Q_r(params['q_r'], 1, n)
    else:
        return 0.0


def get_p_n(params, n, p_values):
    assert (len(p_values) == n)

    base0 = (1.0/get_P_n_nplusi(params, n, n-1))
    base1 = p_values[n-1] * (1 - get_P_n_nplusi(params, n-1, n-1))

    for j in range(n-1):
        base1 -= p_values[j]*get_P_n_nplusi(params, j, n-1)

    return base0*base1

def get_p_success(params, n):
    return (get_Q_a(params['m'], params['lmb'], 1, n)*get_Q_r(params['q_r'], 0, n)) + \
           (get_Q_a(params['m'], params['lmb'], 0, n)*get_Q_r(params['q_r'], 1, n))



if __name__=='__main__':

    matplotlib.rcParams.update({'font.size': 14})
    matplotlib.rcParams.update({'figure.autolayout': True})

    plt.figure(figsize=(7, 4.5))

    # simulation body

    m = 10
    q_r_all = [0.05, 0.2, 0.3]
    lmb_all = [0.01+0.01*x for x in range(200)]

    # plots
    p = []

    for q_r in q_r_all:

        delay = []
        expected_ns = []
        throughput = []

        for lmb in lmb_all:

            params = {'m': m, 'lmb': lmb, 'q_r': q_r}

            print('Load ---> ' + str(params['lmb']))
            # transition matrix
            t_matrix = [[]]
            for i in range(m+1):
                t_matrix.append([])
                for j in range(m+1):
                    t_matrix[i].append(get_P_n_nplusi(params, i, j))
                # print(t_matrix[i])

            for i in range(m+1):
                # print(t_matrix[i])
                print([('%.2f '%(x,)) for x in t_matrix[i]])

            p_0 = 0.1  # dummy value
            p_values = [p_0]

            for i in range(1, m+1):
                p_values.append(get_p_n(params, i, p_values))

            p_values = [v/sum(p_values) for v in p_values]
            print(['%.2f'%(p,) for p in p_values])

            # expected number of backlogged nodes
            expected_n = sum([p_values[i]*i for i in range(len(p_values))])
            expected_ns.append(expected_n)
            print('E[n] ---> ' + str(expected_n))

            # expected delay
            delay.append(expected_n/lmb)
            print('Delay --> ' + str(delay[-1]))

            # expected throughput
            T = sum([p_values[i]*get_p_success(params, i) for i in range(len(p_values))])
            throughput.append(T)

        p.append(plt.plot(lmb_all, delay))
        # p.append(plt.plot(lmb_all, expected_ns, 'x-'))
        # p.append(plt.plot(lmb_all, throughput, '-'))


    plt.figure(figsize=(7, 4.5))

    # plt.ylim((0, 0.7))
    plt.grid(True)
    plt.xlabel('Total load '+r'$\lambda$')
    # plt.ylabel('Resource utilization '+r'$T$')
    # plt.ylabel('Throughput '+r'$T$')
    plt.ylabel('Delay')
    # plt.ylabel('Probability')

    plt.legend((r'$q_r$='+str(q_r_all[0]), r'$q_r$='+str(q_r_all[1]), r'$q_r$='+str(q_r_all[2])), loc=0)
    # plt.legend(('Contention-free' + r'$T = \lambda \exp^{-\lambda}$', r'$T = \lambda$'), loc=0)
    # plt.legend(('C.-based', 'C.-free'), loc=0)

    # plt.show()
    plt.savefig(os.getenv("HOME")+'/Dropbox/_lkn/WTM/mchain_d.png', format='png', bbox='tight')
