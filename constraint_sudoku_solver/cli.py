#! /usr/bin/env python
# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under AGPL v3 or later

from __future__ import print_function

import argparse
import datetime
import sys

from constraint_sudoku_solver.parser import parse_puzzle
from constraint_sudoku_solver.problem import SudokuProblem


_INDENT = '  '


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--echo', action='store_true', help='dump puzzle about to solve')
    parser.add_argument('--duration', dest='max_runtime_seconds', metavar='SECONDS',
            default=0.1, type=float,
            help='seconds to stop searching for additional solutions after (default: %(default)s)')
    parser.add_argument('input_filename', metavar='FILE',
            help='file with puzzle to solve (see examples for puzzle syntax)')
    options = parser.parse_args()

    f = open(options.input_filename, 'r')
    puzzle = f.read()
    f.close()

    if options.echo:
        print('Problem:')
        print('\n'.join((_INDENT + line for line in puzzle.split('\n'))))

    values_of_colum_of_line = parse_puzzle(puzzle)
    problem = SudokuProblem()
    problem.feed_puzzle(values_of_colum_of_line)
    problem.generate_constraints()

    before = datetime.datetime.now()
    print('Trying to solve...')
    solution_index = -1
    solution_dict = None
    after_first = None
    timed_out = False
    for solution_index, solution_dict in enumerate(problem.iterate_solutions()):
        now = datetime.datetime.now()
        if after_first is None:
            after_first = now

        if (now - before).total_seconds() > options.max_runtime_seconds:
            print('Timeout atfer %.3f seconds, %s solutions so far' \
                    % (options.max_runtime_seconds, solution_index + 1))
            timed_out = True
            break

    if solution_dict is None:
        print('There is no solution.', file=sys.stderr)
        sys.exit(1)

    print()
    details = '' \
            if solution_index == 0 \
            else \
                ' (one of %s or more)' % (solution_index + 1) \
                if timed_out \
                else ' (one of %s)' % (solution_index + 1)
    print('Solution%s:' % details)
    print(problem.format_solution(solution_dict, _INDENT))

    print()
    intro = 'First solution took' if solution_index > 0 else 'Took'
    print('%s %.3f seconds to find.' % (intro, (after_first - before).total_seconds()))

    true_sudoku = 'is NOT' \
            if solution_index > 0 \
            else \
                'COULD be' \
                if timed_out \
                else 'IS'
    print('Given problem %s a true Sudoku.' % true_sudoku)


if __name__ == '__main__':
    main()
