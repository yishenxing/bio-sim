#!/usr/bin/env python
#-*- encoding:utf-8 -*-

'''simulate the probability of multiple molecules in the ont single molecule amplification project
'''

import os
import sys
import random
random.seed(42)
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
plt.style.use('ggplot')

plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.grid'] = False

def barcode_combination_simulation(num_hb, num_tb, num_mol, num_exp):
    '''Paramaters:
    -----------------------
    num_hb: number of head barcodes
    num_tb: number of tail barcodes
    num_mol: number of input molecules
    num_exp: number of experiments
    '''
    lst_result = [] # multi molecule ratio in each experiment
    lst_barcode = [] # number of barcode combination in each experiment
    lst_multi_m = [] # number of multi molecule barcode combination in each experiment
    lst_hb = list(range(num_hb))
    lst_tb = list(range(num_tb))
    for i in range(num_exp):
        lst_mol = [] # all molecule barcode combination in one experiment
        for j in range(num_mol):
            hb = random.choice(lst_hb)
            tb = random.choice(lst_tb)
            lst_mol.append((hb, tb))
        counter = Counter(lst_mol)
        num_multi_m = 0
        num_barcode = 0
        for key, value in counter.items():
            num_barcode += 1
            if value > 1:
                num_multi_m += 1
        lst_result.append(num_multi_m/num_barcode)
        lst_barcode.append(num_barcode)
        lst_multi_m.append(num_multi_m)

    # plot
    plt.hist(lst_result, bins=25)
    plt.xlabel('Experiment times')
    plt.ylabel('Ratio of multi molecule')
    plt.title('barcode:{} {}, molecule:{}, experiment:{}'.format(
        num_hb, num_tb, num_mol, num_exp
    ))
    pic_name = os.path.join('simulation_{}_{}_{}_{}.png'.format(
        num_hb, num_tb, num_mol, num_exp
    ))
    plt.savefig(pic_name, dpi=300)
    plt.close()
    
    return (
        np.array(lst_result).mean(), np.array(lst_result).std(), 
        np.array(lst_barcode).mean(), np.array(lst_barcode).std(), 
        np.array(lst_multi_m).mean(), np.array(lst_multi_m).std()
    )

def main():
    lst_num_mol = list(range(50, 1001, 50))
    num_exp = 1000 # number of repeat time
    num_hb = 30 # number of head barcode
    num_tb = 30 # number of tail barcode

    # collect the simulation result
    lst_mean1 = [] # mean ratio
    lst_mean2 = [] # mean total barcode
    lst_mean3 = [] # mean multi molecule barcode
    
    with open('simulation_summary_{}_{}_{}.txt'.format(num_hb, num_tb, num_exp), 'w') as f:
        f.write('NumberHeadBarcode\tNumberTailBarcode\tNumberMolecule\tNumberExperiment\t'
                'MeanRatio\tStdRatio\tMeanNumberBarcode\tStdNumberBarcode\tMeanNumberMulti\t'
                'StdNumberMulti\n')
        for num_mol in lst_num_mol:
            mean1, std1, mean2, std2, mean3, std3 = barcode_combination_simulation(
                num_hb, num_tb, num_mol, num_exp
            )
            f.write('{}\t{}\t{}\t{}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\n'.format(
                num_hb, num_tb, num_mol, num_exp, mean1, std1, mean2, std2, mean3, std3
            ))
            lst_mean1.append(mean1)
            lst_mean2.append(mean2)
            lst_mean3.append(mean3)
            # print(num_mol, flush=True)
    
    # plot the trend
    fig, ax1 = plt.subplots(figsize=(10, 8))
    ax1.set_ylim(0, num_hb*num_tb)
    line1, = ax1.plot(lst_num_mol, lst_mean2, color='r', linewidth=1, label='total')
    line2, = ax1.plot(lst_num_mol, lst_mean3, color='b', linewidth=1, label='multi')
    ax1.set_xlabel('Number of input molecule')
    ax1.set_ylabel('Number of barcode')
    ax2 = ax1.twinx()
    line3, = ax2.plot(lst_num_mol, lst_mean1, color='g', linewidth=1, linestyle='--', 
                      label='ratio')
    ax2.set_ylim(0, 1.0)
    ax2.set_ylabel('Ratio of multi molecule barcode')
    # add legend
    lines = [line1, line2, line3]
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc='upper left')
    plt.title('barcode:{} {}, experiment:{}'.format(num_hb, num_tb, num_exp))
    plt.savefig('simulation_{}_{}_{}.png'.format(num_hb, num_tb, num_exp), dpi=300)
    plt.close()
    
if __name__ == '__main__':
    main()