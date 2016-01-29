'''
Markov chain model: finite sources, infinite retransmissions, uniform back-off
'''

__author__ = 'Mikhail Vilgelm'

import numpy as np
import math, os
import matplotlib.pyplot as plt
import matplotlib
from scipy import special


class SAlohaModel():

    def __init__(self, params):
        '''
        Parameters: number of nodes, total arrival rate, retransmission probability
        :param params:
        :return:
        '''
        self.m = params['m']
        self.lmb = params['lmb']
        self.q_r = params['q_r']

        # calculate transition matrix
        self.t_matrix = [[]]
        for i in range(self.m+1):
            self.t_matrix.append([])
            for j in range(self.m+1):
                self.t_matrix[i].append(self.get_P_n_nplusi(i, j))

    def q_a(self):
        '''
        Probability of transmission from unbacklogged node
        :return:
        '''
        return 1 - math.exp(-self.lmb/self.m)


    def get_Q_a(self, i, n):
        '''
        Probability of i unbacklogged notes attempt a transmission, given n as a size of a backlog
        :param i:
        :param n:
        :return:
        '''
        return special.binom(self.m-n, i) * ((1-self.q_a()) ** (self.m-n-i)) * (self.q_a() ** i)


    def get_Q_r(self, i, n):
        '''
        Probability of i backlogged notes attempt a transmission, given n as a size of a backlog
        :param i:
        :param n:
        :return:
        '''
        return special.binom(n, i) * ((1-self.q_r) ** (n-i)) * (self.q_r ** i)


    def get_P_n_nplusi(self, n, nplusi):
        '''
        Calculate transition probabilities
        :param n:
        :param nplusi:
        :return:
        '''
        i = nplusi - n
        if (i >= 2) and (i <= (m-n)):
            return self.get_Q_a(i, n)
        elif i == 1:
            return self.get_Q_a(1, n)*(1 - self.get_Q_r(0, n))
        elif i == 0:
            return self.get_Q_a(1, n)*self.get_Q_r(0, n) + \
                   self.get_Q_a(0, n)*(1 - self.get_Q_r(1, n))
        elif i == -1:
            return self.get_Q_a(0, n)*self.get_Q_r(1, n)
        else:
            return 0.0


    def get_p_n(self, n, p_values):
        '''
        :param n: state
        :param p_values: previously computed steady-state probabilities
        :return: current probability
        '''

        assert (len(p_values) == n)  # make we have enough states already computed

        base0 = (1.0/self.get_P_n_nplusi(n, n-1))
        base1 = p_values[n-1] * (1 - self.get_P_n_nplusi(n-1, n-1))

        for j in range(n-1):
            base1 -= p_values[j]*self.get_P_n_nplusi(j, n-1)

        return base0*base1

    def get_p_success(self, n):
        '''
        Probability of a successful transmission given backlog state
        :param n:
        :return:
        '''
        return (self.get_Q_a(1, n)*self.get_Q_r(0, n)) + \
               (self.get_Q_a(0, n)*self.get_Q_r(1, n))

    def get_transition_matrix(self):
        return self.t_matrix

    def print_t_matrix(self):
        for i in range(self.m+1):
            print([('%.2f '%(x,)) for x in self.t_matrix[i]])


    def get_p_values(self):
        # dummy value -> after calculating all we will normalize anyways
        p_0 = 0.1

        # initialize with 0th state
        p_values = [p_0]

        # compute one after another
        for i in range(1, m+1):
            p_values.append(self.get_p_n(i, p_values))

        # get normalized values
        p_values = [v/sum(p_values) for v in p_values]

        # make sure they sum up
        # assert sum(p_values) == 1

        return p_values




if __name__=='__main__':

    # global plotting settings
    matplotlib.rcParams.update({'font.size': 14})
    matplotlib.rcParams.update({'figure.autolayout': True})
    plt.figure(figsize=(7, 4.5))

    # simulation parameters:
    m = 10
    q_r_all = [0.05, 0.2, 0.3]
    lmb_all = [0.01+0.01*x for x in range(200)]

    # plots
    p = []

    # for every q_r
    for q_r in q_r_all:

        # metrics
        delay = []
        expected_ns = []
        throughput = []

        # for all loads
        for lmb in lmb_all:

            # set the parameters dictionary
            params = {'m': m, 'lmb': lmb, 'q_r': q_r}

            # create model instance
            saloha = SAlohaModel(params)

            print('Load ---> ' + str(params['lmb']))

            # transition matrix
            t_matrix = saloha.get_transition_matrix()

            # print matrix nicely
            saloha.print_t_matrix()

            # get steady-state probabilities
            p_values = saloha.get_p_values()

            print(['%.2f'%(i,) for i in p_values])

            # expected number of backlogged nodes
            expected_n = sum([p_values[i]*i for i in range(len(p_values))])
            expected_ns.append(expected_n)
            print('E[n] ---> ' + str(expected_n))

            # expected delay
            delay.append(expected_n/lmb)
            print('Delay --> ' + str(delay[-1]))

            # expected throughput
            T = sum([p_values[i]*saloha.get_p_success(i) for i in range(len(p_values))])
            throughput.append(T)

        # choose the plot you need
        # p.append(plt.plot(lmb_all, delay))
        # p.append(plt.plot(lmb_all, expected_ns, 'x-'))
        p.append(plt.plot(lmb_all, throughput, '-'))


    # plotting parameters

    plt.grid(True)
    plt.xlabel('Total load '+r'$\lambda$')

    # choose the label

    plt.ylabel('Throughput '+r'$T$')
    # plt.ylabel('Delay')
    # plt.ylabel('Probability')

    # pick up the legend
    # plt.legend((r'$q_r$='+str(q_r_all[0]), r'$q_r$='+str(q_r_all[1]), r'$q_r$='+str(q_r_all[2])), loc=0)

    # save or show!
    plt.show()
    # plt.savefig(os.getenv("HOME")+'/Dropbox/_lkn/WTM/mchain_d.png', format='png', bbox='tight')
