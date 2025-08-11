#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''simulate the error accumulation with statistic method, simulate the error accumulation in 
different fragment length, enzyme error rate and cycle number
'''

import os
import sys
from decimal import Decimal, getcontext
getcontext().prec = 100

def pcr(error_rate, length, cycle, output):
    # transform the type of error_rate, length, cycle to Decimal
    error_rate = Decimal(str(error_rate))
    length = Decimal(str(length))
    m_error_rate = Decimal(1) - (Decimal(1) - error_rate) ** length
    
    # PCR details each cycle
    # molecule are divided into three types
    # {
    #     (correct_seq, correct_seq): count, 
    #     (wrong_seq, wrong_seq): count, 
    #     (correct_seq, wrong_seq): count
    # }
    dict_seq = {
        ('cor', 'cor'): Decimal(1), 
        ('err', 'err'): Decimal(0), 
        ('cor', 'err'): Decimal(0)
    }
    with open(output, 'w') as f:
        f.write('pcr_cycle\tnum_seq\tnum_error\terror_rate\n')
        f.flush()

        for i in range(cycle):
            # each cycle, the molecule are divided into three types
            # ! errors are not irreversible in default
            dict_seq_cycle = {
                ('cor', 'cor'): Decimal(0), 
                ('err', 'err'): Decimal(0), 
                ('cor', 'err'): Decimal(0)
            }
            # calculate the three types of replication
            # 1. (cor, cor) -> (cor, cor), (cor, err)
            num_cor_err = int(dict_seq[('cor', 'cor')] * 2 * m_error_rate)
            num_cor_cor = dict_seq[('cor', 'cor')] * 2 - num_cor_err
            dict_seq_cycle[('cor', 'cor')] += num_cor_cor
            dict_seq_cycle[('cor', 'err')] += num_cor_err
            # 2. (err, err) -> (err, err)
            num_err_err = dict_seq[('err', 'err')] * 2
            dict_seq_cycle[('err', 'err')] += num_err_err
            # 3. (cor, err) -> (cor, cor), (cor, err), (err, err)
            num_cor_err = int(dict_seq[('cor', 'err')] * m_error_rate)
            num_cor_cor = dict_seq[('cor', 'err')] - num_cor_err
            num_err_err = dict_seq[('cor', 'err')]
            dict_seq_cycle[('cor', 'cor')] += num_cor_cor
            dict_seq_cycle[('cor', 'err')] += num_cor_err
            dict_seq_cycle[('err', 'err')] += num_err_err
            
            # refresh the PCR result
            dict_seq = dict_seq_cycle
            
            num_seq_cycle = sum(dict_seq.values())
            num_err_seq_cycle = dict_seq[('cor', 'err')] + dict_seq[('err', 'err')]
            error_rate_cycle = num_err_seq_cycle / num_seq_cycle * Decimal(100)
            f.write('{}\t{}\t{}\t{:.6f}%\n'.format(
                i+1, num_seq_cycle, num_err_seq_cycle, error_rate_cycle
            ))

def main():
    length = 1500 # the length of the sequence
    cycle = 100 # the number of cycles
    # the error rate of the enzyme
    lst_error_rate = [2e-7, 4e-7, 8e-7, 16e-7, 32e-7, 64e-7, 128e-7]
    lst_error_rate_str = ['2e-7', '4e-7', '8e-7', '16e-7', '32e-7', '64e-7', '128e-7']
    for error_rate, error_rate_str in zip(lst_error_rate, lst_error_rate_str):
        output = 'pcr_simulation_{}_{}.txt'.format(length, error_rate_str)
        pcr(error_rate, length, cycle, output)
    
if __name__ == "__main__":
    main()