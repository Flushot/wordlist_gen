#!/usr/bin/env python
"""
Generate a wordlist.
"""
from __future__ import print_function, unicode_literals, with_statement

import itertools
import math
import sys

import argparse
import tqdm


def all_subsets(ss):
    return itertools.chain(*map(lambda x: itertools.combinations(ss, x), 
                                range(0, len(ss) + 1)))


def load_charset(charset_file):
    charset_file.seek(0)
    for line in charset_file:
        char_or_word = line.rstrip('\r\n')
        if char_or_word:
            yield char_or_word


def get_total_permutations(charset):
    total_words = 0
    for subset in all_subsets(charset):
        total_words += math.factorial(len(subset))

    return total_words


def iterate_permutations(charset):
    for subset in all_subsets(charset):
        for perm in itertools.permutations(subset):
            yield ''.join(perm)


def generate_wordlist(wordlist_file, charset_file, using_stdout):
    charset = list(load_charset(charset_file))
    gen = iterate_permutations(charset)
    if not using_stdout:
        gen = tqdm.tqdm(gen, 
                        total=get_total_permutations(charset),
                        unit='word')

    for perm in gen:
        print(perm, file=wordlist_file)


def main():
    argp = argparse.ArgumentParser(description='Generate wordlist')
    argp.add_argument('--charset', '-c', 
                      metavar='CHARSET_FILE', 
                      help='Characters or words to permute (default: stdin)')
    argp.add_argument('--output', '-o', 
                      metavar='OUTPUT_FILE', 
                      help='Wordlist output file (default: stdout)')
    # TODO: add options for min/max password length to generate
    args = argp.parse_args()

    try:
        # Open charset file
        if args.charset:
            charset_file = open(args.charset, 'r')
        else:
            charset_file = sys.stdin

        # Open output file
        if args.output:
            out_file = open(args.output, 'w+', buffering=int(1e5))
        else:
            out_file = sys.stdout
    except IOError as ex:
        log.error(ex)
        return 1

    using_stdout = (out_file == sys.stdout)

    try:
        generate_wordlist(out_file, charset_file, using_stdout)
        return 0
    except KeyboardInterrupt:
        print('User interrupted with ^C', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
