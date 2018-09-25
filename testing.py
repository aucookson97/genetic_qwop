from math import sqrt, log
import random


for i in range(10):
    p = [i for i in range(30)]

    percent_top_survive = .3


    pc = p.copy()
    del p[:]

    num_survive = int(len(pc) * percent_top_survive + .5)

    for i in range(num_survive):
        p.append(pc[i])

    for i in range(num_survive, len(pc)):
        
        chance = 1.0/sqrt(2) * log(i, 10)
        if (random.random() >= chance):
            p.append(pc[i])
        #print ('{}, {}'.format(i, chance))

    print ('\nNext Generation:')
    print (p)
    print (len(p))
