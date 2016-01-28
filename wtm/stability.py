__author__ = 'Mikhail Vilgelm'

from mchain import q_a
import math, os
import matplotlib.pyplot as plt
import matplotlib
from scipy import special


def get_G(params, n):
    v = (params['m']-n)*q_a(params['lmb'], params['m']) + n*params['q_r']
    print(v)
    return v


def get_P_succ_appr_n(params, n):
    return get_G(params, n)*math.exp(-get_G(params, n))

def get_P_succ_appr_G(params, G):
    return G*math.exp(-G)

def get_D_n(params, n):
    return (params['m']-n)*q_a(params['lmb'], params['m']) - get_P_succ_appr_n(params, n)


if __name__=='__main__':
    matplotlib.rcParams.update({'font.size': 14})
    matplotlib.rcParams.update({'figure.autolayout': True})
    plt.figure(figsize=(7, 4.5))

    # simulation parameters
    lmb = 0.35
    m = 30
    # q_r_all = [0.1, 0.2, 0.3]
    q_r_all = [0.2]


    for q_r in q_r_all:
        print(q_a(lmb, m))

        params = {'lmb': lmb,
                  'm': m,
                  'q_r': q_r}

        print('##### start #####')

        ns = [n for n in range(params['m']+1)]

        G_ns = [get_G(params, n) for n in ns]
        D_ns = [get_D_n(params,n) for n in ns]

        # plt.plot(G_ns, [get_P_succ_appr_G(params, G) for G in G_ns])

        # plot
        plt.plot(ns, [get_P_succ_appr_n(params, n) for n in ns], '-')

    # plot arrival rate
    plt.plot(ns, [(params['m']-n)*q_a(params['lmb'], params['m'])for n in ns], 'b-.')
    plt.plot(ns, [(params['m']-n)*q_a(0.45, params['m'])for n in ns], 'g-.')
    plt.plot(ns, [params['lmb'] for n in ns], 'r-.')
    plt.grid(True)

    plt.ylim((0, 0.5))
    plt.xlim((0, 35))

    plt.xlabel('Backlog size')

    # plt.legend((r'$q_r=0.1$', \
    #            r'$q_r=0.2$', \
    #            r'$q_r=0.3$', \
    #            r'$(m-n)q_a$'))


    # plt.legend((r'$P_{succ}\approx G(n)e^{-G(n)}$', r'$(m-n)q_a$'+'\t'+r'$\lambda=0.35$', \
    #            r'$(m-n)q_a$'+'\t'+r'$\lambda=0.45$', \
    #            r'$(m-n)q_a$'+'\t'+r'$\lambda=0.15$'))
    plt.legend((r'$P_{succ}\approx G(n)e^{-G(n)}$', r'$(m-n)q_a$'+'\t'+r'$\lambda=0.35$', \
                r'$(m-n)q_a$'+'\t'+r'$\lambda=0.45$', \
                r'$\lambda$'))

    # plt.show()
    plt.savefig(os.getenv("HOME")+'/Dropbox/_lkn/WTM/stability_extended.png', format='png', bbox='tight')
    # plt.savefig(os.getenv("HOME")+'/Dropbox/_lkn/WTM/stability_retx.png', format='png', bbox='tight')