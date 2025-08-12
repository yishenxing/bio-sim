#!/usr/bin/env python
#-*- encoding=utf-8 -*-

'''simulate how naive fertility choices affects population gender structure
'''

import random
import matplotlib.pyplot as plt
plt.style.use('ggplot_w')

def boy_born_simulation(num_family, ratio_boy_family=1.0):
    '''Parameters
    -------------
    num_family: int
        number of families to simulate
    ratio_boy_family: float
        ratio of boy born family
    '''
    # 1 boy, 0 girl
    # families
    dict_family = {_:[] for _ in range(num_family)}
    # boy born families
    idx_boy_family = random.sample(range(num_family), int(ratio_boy_family * num_family))
    idx_boy_family = set(idx_boy_family)
    
    # simulate
    for i in range(num_family):
        if i in idx_boy_family:
            lst_child = []
            while not lst_child or lst_child[-1] == 0:
                child = random.randint(0, 1)
                lst_child.append(child)
            dict_family[i] = lst_child
        else:
            dict_family[i].append(random.randint(0, 1))
            
    # summarize
    num_boy, num_girl = 0, 0
    for i, lst_child in dict_family.items():
        num_boy += sum(lst_child)
        num_girl += len(lst_child) - sum(lst_child)
        
    return num_boy, num_girl

def plot(ratio, lst_ratio):
    plt.hist(lst_ratio, bins=100, density=True, alpha=0.5)
    plt.xlabel('boy ratio')
    plt.ylabel('frequency')
    plt.title('ratio = {}'.format(ratio))
    pic_name = 'boy_born_sim_{}.png'.format(ratio)
    plt.savefig(pic_name)
    plt.close()

def main():
    num_family = 1000
    lst_ratio = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    num_sim = 1000
    with open('boy_born_sim.txt', 'w') as fh:
        fh.write('ratio\tboy_ratio\n')
        for ratio in lst_ratio:
            print(ratio)
            lst_sim_result = []
            for _ in range(num_sim):
                num_boy, num_girl = boy_born_simulation(num_family, ratio)
                lst_sim_result.append(num_boy / (num_boy + num_girl))
            plot(ratio, lst_sim_result)
            fh.write('{}\t{:.6f}\n'.format(
                ratio, sum(lst_sim_result) / num_sim
            ))

if __name__ == '__main__':
    main()