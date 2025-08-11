#!/usr/bin/env python
#-*- encoding: utf-8 -*-

'''plot pcr simulation results
'''

import os
import sys
import matplotlib.pyplot as plt
plt.style.use('ggplot')

length = 1500
lst_error_rate = [2e-7, 4e-7, 8e-7, 16e-7, 32e-7, 64e-7, 128e-7]
lst_error_rate_str = ['2e-7', '4e-7', '8e-7', '16e-7', '32e-7', '64e-7', '128e-7']
lst_error_num = [int(1/_) for _ in lst_error_rate]

def read_data(file_name):
    x, y = [0], [0]
    with open(file_name, 'r') as f:
        f.readline()
        for line in f:
            arr = line.strip().split('\t')
            cycle = int(arr[0])
            error_rate = float(arr[3][:-1])
            x.append(cycle)
            y.append(error_rate)
    return x, y

def plot(pic_name):
    fig = plt.figure(figsize=(10, 6))
    for error_rate, error_rate_str, error_num in zip(
        lst_error_rate, lst_error_rate_str, lst_error_num
    ):
        file_name = "pcr_simulation_{}_{}.txt".format(length, error_rate_str)
        x, y = read_data(file_name)
        plt.plot(x, y, label='Base error rate: {}, One error per {} bases'.format(
            error_rate_str, error_num
        ))
    plt.xlabel("Cycle")
    plt.ylabel("Error molecule (%)")
    plt.title('PCR simulation with {}bp sequence'.format(length))
    plt.legend(fontsize='x-small')
    plt.savefig(pic_name, dpi=300)

def main():
    plot("pcr_simulation_statistic.png")

if __name__ == "__main__":
    main()