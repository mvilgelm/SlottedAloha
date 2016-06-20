'''
Basic model: no retransmissions, only mean arrival rate of the poisson distribution as a parameter.
'''

__author__ = 'Mikhail Vilgelm'

import numpy as np
import math, os
import matplotlib.pyplot as plt
import matplotlib


# saloha - throughput (utilization)
def t_aloha(arr):
    return arr*math.exp(-arr)


# saloha - idle probability
def i_aloha(arr):
    return math.exp(-arr)


# saloha - collision probability
def e_aloha(arr):
    return 1.0 - t_aloha(arr) - i_aloha(arr)


# tdma - throughput (utilization)
def t_tdma(arr):
    if arr>1:
        return 1
    return arr


def plot_saloha_vs_tdma(load_range):
    """
    Plot slotted aloha performance vs. tdma
    """

    # configure plot parameters
    matplotlib.rcParams.update({'font.size': 14})
    matplotlib.rcParams.update({'figure.autolayout': True})
    plt.figure(figsize=(7, 4.5))

    load = load_range

    # saloha
    plt.plot(load, [t_aloha(x) for x in load], '-b')

    # tdma
    plt.plot(load, [t_tdma(x) for x in load], '-g')

    # display parameters
    plt.grid(True)
    plt.ylim((0, 1.1))
    plt.xlabel('Normalized load '+r'$\lambda$')
    plt.ylabel('Resource utilization '+r'$T$')

    plt.legend(('C.-based', 'C.-free'), loc=0)


def plot_saloha_performance(load_range):
    """
    Plot slotted aloha performance metrics: collisions, idle slots and throughput
    """

    # configure plot parameters
    matplotlib.rcParams.update({'font.size': 14})
    matplotlib.rcParams.update({'figure.autolayout': True})
    plt.figure(figsize=(7, 4.5))

    load = load_range

    # throughput
    plt.plot(load, [t_aloha(x) for x in load], '-b')

    # collisions
    plt.plot(load, [e_aloha(x) for x in load], '-.r')

    # idle
    plt.plot(load, [i_aloha(x) for x in load], '--g')
    
    plt.grid(True)
    plt.xlabel('Normalized load '+r'$\lambda$')
    plt.ylabel('Probability')

    plt.legend(('success', 'collision', 'idle'), loc=0)
    

if __name__=='__main__':

    load = [0.01+0.01*x for x in range(400)]

    plot_saloha_vs_tdma(load)

    plot_saloha_performance(load)

    plt.show()