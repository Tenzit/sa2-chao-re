#!/usr/bin/env python3

from scipy.optimize import linprog
import numpy as np
import argparse
from itertools import compress

parser = argparse.ArgumentParser()

parser.add_argument('--num-animals', type=int, default=3)
parser.add_argument('--starting-xp', type=int, default=0)
parser.add_argument('--ignore-stat', choices=['swim', 'fly', 'run', 'power'], nargs='*', default=[])
args = parser.parse_args()

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

stat_filter = ['swim' not in args.ignore_stat, 'fly' not in args.ignore_stat,
               'run' not in args.ignore_stat, 'power' not in args.ignore_stat]

num_stats = sum(stat_filter)
print(num_stats)

animals = [(animal[0], list(compress(animal[1],stat_filter))) for animal in animals]

min_animals = np.Infinity
min_animals_animals = []

idx = [0]*args.num_animals
reset_idx = [False]*args.num_animals
needed_stat = 9900-args.starting_xp
stats = [needed_stat]*num_stats

for i in range(1, args.num_animals):
    idx[i] = idx[i-1] + 1
while idx[0] < (len(animals) - (args.num_animals-1)):
    t_mat = np.matrix.transpose(np.array([animals[idx[i]][1] for i in range(args.num_animals)]))
    if ~(~t_mat.any(axis=1)).any():
        res = linprog([1000]*args.num_animals, -t_mat, -np.matrix(stats), method='highs', integrality=1)
        num_animals = res.x
        ceil_na = np.ceil(num_animals)
        if (res.success and np.sum(ceil_na) < min_animals):
            min_animals = np.sum(ceil_na)
            min_animals_animals = [(animals[idx[i]][0], ceil_na[i], animals[idx[i]][1]) for i in range(args.num_animals)]
            ma = [f'{min_animals_animals[i][1]} {min_animals_animals[i][0]}' for i in range(args.num_animals)]
            ma_cat = ', '.join(ma)
            print(f'New minimum number of animals: {min_animals}; {ma_cat}; Sanity check: {np.dot(t_mat, np.matrix.transpose(ceil_na))}')

    for i in range(args.num_animals-1, -1, -1):
        idx[i] = idx[i] + 1
        if idx[i] >= (len(animals) - (args.num_animals-i-1)) and i != 0:
            reset_idx[i] = True
        else:
            break

    for i in range(1, args.num_animals):
        if reset_idx[i]:
            idx[i] = idx[i-1] + 1
            reset_idx[i] = False