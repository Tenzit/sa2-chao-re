#!/usr/bin/env python3

from scipy.optimize import linprog
import numpy as np

# Name, swim, fly, run, power
animals = [
           ('penguin',      [36, 12, 8, 0]),
           ('seal',         [40, 0, 0, 8]),
           ('otter',        [44, 0, 8, 0]),
           ('peacock',      [12, 48, 0, 0]),
           ('parrot',       [0, 48, 0, 4]),
           ('condor',       [20, 60, 0, 16]),
           ('rabbit',       [0, 8, 40, 0]),
           ('cheetah',      [0, 0, 40, 8]),
           ('boar',         [0, 0, 32, 16]),
           ('bear',         [8, 0, 4, 36]),
           ('tiger',        [0, 0, 20, 36]),
           ('gorilla',      [4, 8, 4, 40]),
           ('skunk',        [8, 12, 12, 8]),
           ('sheep',        [8, 12, 20, 20]),
           ('raccoon',      [20, 12, 4, 8]),
           ('dragon',       [20, 4, 8, 32]),
           ('unicorn',      [16, 12, 36, 0]),
           ('phoenix',      [12, 32, 4, 16]),
           ('half fish',    [32, 0, 8, 24]),
           ('skeleton dog', [8, 8, 32, 16]),
           ('bat',          [8, 40, 8, 8])]

min_animals = np.Infinity
min_animals_animals = []

n_to_check = 5

for i in range(31, 41):
    start_xp = i*50

    idx = [0]*n_to_check
    reset_idx = [False]*n_to_check
    needed_stat = 9900-start_xp
    stats = [needed_stat]*4

    for i in range(1, n_to_check):
        idx[i] = idx[i-1] + 1
    while idx[0] < (len(animals) - (n_to_check-1)):
        t_mat = np.matrix.transpose(np.array([animals[idx[i]][1] for i in range(n_to_check)]))
        if ~(~t_mat.any(axis=1)).any():
            res = linprog(np.zeros(n_to_check), -t_mat, -np.matrix(stats))
            num_animals = res.x
            ceil_na = np.ceil(num_animals)
            if (res.success and np.sum(ceil_na) < min_animals):
                min_animals = np.sum(ceil_na)
                min_animals_animals = [(animals[idx[i]][0], ceil_na[i], animals[idx[i]][1]) for i in range(n_to_check)]
                ma = [f'{min_animals_animals[i][1]} {min_animals_animals[i][0]}' for i in range(n_to_check)]
                ma_cat = ', '.join(ma)
                #print(f'New minimum number of animals: {ma_cat}; Sanity check: {np.dot(t_mat, np.matrix.transpose(ceil_na))}')

        for i in range(n_to_check-1, -1, -1):
            idx[i] = idx[i] + 1
            if idx[i] >= (len(animals) - (n_to_check-i-1)) and i != 0:
                reset_idx[i] = True
            else:
                break

        for i in range(1, n_to_check):
            if reset_idx[i]:
                idx[i] = idx[i-1] + 1
                reset_idx[i] = False

    # Minimize the number of animals completely
    delta = 5
    curr_check = needed_stat
    while True:
        curr_check -= delta
        ani_stats = [thing[2] for thing in min_animals_animals]
        nums = [thing[1] for thing in min_animals_animals]

        res = linprog(np.zeros(n_to_check), -np.matrix.transpose(np.matrix(ani_stats)), -np.matrix([curr_check]*4))
        num_animals = np.ceil(res.x)
        if (res.success and np.sum(num_animals) < min_animals):
            test = np.dot(np.matrix.transpose(np.matrix(ani_stats)), np.matrix.transpose(num_animals))
            if (test < needed_stat).any():
                break
            min_animals = np.sum(num_animals)
            for i in range(len(num_animals)):
                min_animals_animals[i] = (min_animals_animals[i][0], num_animals[i], min_animals_animals[i][2])

    ani_stats = [thing[2] for thing in min_animals_animals]
    nums = [thing[1] for thing in min_animals_animals]
    ma = [f'{min_animals_animals[i][1]}' for i in range(n_to_check)]
    ma_cat = ', '.join(ma)
    print(f'{start_xp}, {ma_cat}')
    #print(f'Starting XP: {start_xp}; New minimum number of animals: {ma_cat}; Sanity check: {np.matrix.transpose(np.dot(np.matrix.transpose(np.matrix(ani_stats)), np.matrix.transpose(np.matrix(nums))))}')

# Code for just checking 3
#for h in range(len(animals)):
#    for i in range(h+1, len(animals)):
#        for j in range(i+1, len(animals)):
#            t_mat = np.matrix.transpose(np.array([animals[h][1], animals[i][1], animals[j][1]]))
#            if (~t_mat.any(axis=1)).any():
#                continue
#            res = linprog(np.zeros(3), -t_mat, -np.matrix([9900, 9900, 9900, 9900]))
#            num_animals = res.x
#            ceil_na = np.ceil(num_animals)
#            if (res.success and np.sum(ceil_na) < min_animals):
#                min_animals = np.sum(ceil_na)
#                min_animals_animals = [(animals[h][0], ceil_na[0]), (animals[i][0], ceil_na[1]), (animals[j][0], ceil_na[2])]
#                ma1 = f'{min_animals_animals[0][1]} {min_animals_animals[0][0]}'
#                ma2 = f'{min_animals_animals[1][1]} {min_animals_animals[1][0]}'
#                ma3 = f'{min_animals_animals[2][1]} {min_animals_animals[2][0]}'
#                print(f'New minimum number of animals: {ma1}, {ma2}, {ma3}, {np.dot(t_mat, np.matrix.transpose(ceil_na))}')
