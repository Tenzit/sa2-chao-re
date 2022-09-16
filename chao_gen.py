#!/usr/bin/env python3

import argparse
import math

# The following 3 functions yoinked directly from assembly
# while simplifying for a high-level language
# From sonic2App.exe+1506B0 in cheat engine
def method_a(cur_rn):
    dna = [0,1,2,3,4,0,0,0]
    for i in range(10):
        cur_rn = lcg_update(cur_rn)
        idx_a = math.trunc(scale_rn(cur_rn, 5))
        cur_rn = lcg_update(cur_rn)
        idx_b = math.trunc(scale_rn(cur_rn, 5))

        tmp_a = dna[idx_a]
        tmp_b = dna[idx_b]
        dna[idx_a] = tmp_b
        dna[idx_b] = tmp_a

    return (cur_rn, dna)

def method_b(cur_rn):
    dna = [0]*8
    for i in range(8):
        cur_rn = lcg_update(cur_rn)
        scaled_rn = math.trunc(scale_rn(cur_rn, 3))
        dna[i] = 1 + scaled_rn

    return (cur_rn, dna)


def method_c(cur_rn):
    dna = [0]*8
    i = 0
    while i < 14:
        cur_rn = lcg_update(cur_rn)
        scaled_rn = math.trunc(scale_rn(cur_rn, 8))
        if dna[scaled_rn] >= 5:
            continue
        dna[scaled_rn] += 1
        i += 1

    return (cur_rn, dna)

def lcg_update(cur):
    # Courtesy of sonic2App.exe+3A89D8
    return (cur * 0x343FD + 0x269EC3) & 0xFFFFFFFF

def scale_rn(rn, max_range):
    scaled_rn = (rn >> 0x10) & 0x7FFF
    return max_range * scaled_rn/32768

def make_action(val, arrlen):
    class CustomAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if len(values) < arrlen:
                values.extend([val]*(arrlen - len(values)))
            setattr(args, self.dest, values)
    return CustomAction

def min_vals(val):
    return make_action(val, 8)

def max_vals(val):
    return make_action(val, 8)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-seed', dest='seed', type=lambda x: int(x, 0),
                        help='Seed to figure out RNG call offset for')
    parser.add_argument('--min-stats', type=int, nargs="*", action=min_vals(0), default=[0]*8,
                        help='Minimum value for stats to have (up to 8 numbers, 0-5)')
    parser.add_argument('--max-stats', type=int, nargs="*", action=max_vals(5), default=[5]*8,
                        help='Maximum value for stats to have (up to 8 numbers, 0-5)')
    parser.add_argument('--rng-iters', type=int, default=100,
                        help='Number of RNG iterations to check stats for')
    return parser.parse_args()

def main():
    args = parse_args()
    rn = 0x00000000

    if args.seed is None:
        for i in range(1, args.rng_iters):
            rn = lcg_update(rn)
            scaled_rn = scale_rn(rn, 1)

            method = 'A'
            if scaled_rn < 0.33:
                (_, dna) = method_a(rn)
                method = 'A'
            elif scaled_rn < 0.66:
                (_, dna) = method_b(rn)
                method = 'B'
            else:
                (_, dna) = method_c(rn)
                method = 'C'

            if all(x[0] >= x[1] for x in zip(dna, args.min_stats)) and all(x[0] <= x[1] for x in zip(dna, args.max_stats)):
                print(f'RNG Calls: {i} Seed: {hex(rn)} Method {method}: Swim {dna[0]}, Fly {dna[1]}, Run {dna[2]}, Power {dna[3]}, Stam {dna[4]}, Int {dna[5]}, Luck {dna[6]}, Unknown {dna[7]}')
    else:
        i = 0
        while rn != args.seed:
            i += 1
            rn = lcg_update(rn)

        print(f'Found seed {hex(rn)} at RNG call {i}')


if __name__ == '__main__':
    main()
