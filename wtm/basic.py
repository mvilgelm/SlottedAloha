__author__ = 'Mikhail Vilgelm'

import numpy as np
import math, os
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams.update({'font.size': 14})
matplotlib.rcParams.update({'figure.autolayout': True})

# saloha - throughput
def t_aloha(arr):
    return arr*math.exp(-arr)

# saloha - idle probability
def i_aloha(arr):
    return math.exp(-arr)

# saloha - collision probability
def e_aloha(arr):
    return 1.0 - t_aloha(arr) - i_aloha(arr)

def t_tdma(arr):
    if arr>1:
        return 1
    return arr

plt.figure(figsize=(7, 4.5))

load = [0.01+0.01*x for x in range(400)]

# throughput
plt.plot(load, [t_aloha(x) for x in load], '-b')

# collisions
plt.plot(load, [i_aloha(x) for x in load], '-.r')

# idle
plt.plot(load, [e_aloha(x) for x in load], '--g')


# plt.ylim((0, 1.1))
plt.grid(True)
plt.xlabel('Normalized load '+r'$\lambda$')
# plt.ylabel('Resource utilization '+r'$T$')
# plt.ylabel('Throughput '+r'$T$')
plt.ylabel('Probability')

plt.legend(('success', 'collision', 'idle'), loc=0)
# plt.legend(('Contention-free' + r'$T = \lambda \exp^{-\lambda}$', r'$T = \lambda$'), loc=0)
# plt.legend(('C.-based', 'C.-free'), loc=0)

# plt.show()
plt.savefig(os.getenv("HOME")+'/Dropbox/_lkn/basic.png', format='png', bbox='tight')
