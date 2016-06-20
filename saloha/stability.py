"""
Additions to the markov chain model of slotted aloha: stability plots.
"""
__author__ = 'Mikhail Vilgelm'

from mchain import SAlohaModel, create_figure_with_params
import math, os
import matplotlib.pyplot as plt
import matplotlib
from scipy import special


def plot_stability():

    create_figure_with_params()
    # simulation parameters
    lmb = 0.35
    m = 30
    # q_r_all = [0.1, 0.2, 0.3]
    q_r_all = [0.2]


    for q_r in q_r_all:
        # print(q_a(lmb, m))

        mchain_model = SAlohaModel(lmb=lmb,
                  m=m,
                  q_r=q_r)

        print('##### start #####')

        ns = [n for n in range(m+1)]

        G_ns = [mchain_model.get_G(n) for n in ns]
        D_ns = [mchain_model.get_D_n(n) for n in ns]

        # plot
        plt.plot(ns, [mchain_model.get_P_succ_appr_n(n) for n in ns], '-')

    # plot arrival rate
    plt.plot(ns, [(m-n)*mchain_model.q_a() for n in ns], 'b-.')
    plt.plot(ns, [(m-n)*SAlohaModel(lmb=0.45, m=m, q_r=q_r).q_a() for n in ns], 'g-.')
    plt.plot(ns, [lmb for n in ns], 'r-.')
    plt.grid(True)

    plt.ylim((0, 0.5))
    plt.xlim((0, 35))

    plt.xlabel('Backlog size')

    plt.legend((r'$P_{succ}\approx G(n)e^{-G(n)}$', r'$(m-n)q_a$'+'\t'+r'$\lambda=0.35$', \
                r'$(m-n)q_a$'+'\t'+r'$\lambda=0.45$', \
                r'$\lambda$'))


if __name__=='__main__':
    
    plot_stability()
    plt.show()
