# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under AGPL v3 or later

from constraint import Problem, AllDifferentConstraint


class SudokuProblem(object):
    def __init__(self):
        self._problem = Problem()

    def _each_once_per_line(self):
        for line_index in range(9):
            variable_names = [self._variable_name(line_index, column_index) for column_index in range(9)]
            self._problem.addConstraint(AllDifferentConstraint(), variable_names)

    def _each_once_per_column(self):
        for column_index in range(9):
            variable_names = [self._variable_name(line_index, column_index) for line_index in range(9)]
            self._problem.addConstraint(AllDifferentConstraint(), variable_names)

    def _each_once_per_square(self):
        for line_square_index in range(3):
            for column_square_index in range(3):
                variable_names = []
                line_index_start = line_square_index * 3
                for line_index in range(line_index_start, line_index_start + 3):
                    column_index_start = column_square_index * 3
                    for column_index in range(column_index_start, column_index_start + 3):
                        variable_names.append(self._variable_name(line_index, column_index))
                self._problem.addConstraint(AllDifferentConstraint(), variable_names)

    def generate_constraints(self):
        self._each_once_per_line()
        self._each_once_per_column()
        self._each_once_per_square()

    def _variable_name(self, line_index, column_index):
        return '(l%d,c%d)' % (line_index, column_index)

    def feed_puzzle(self, values_of_colum_of_line):
        for line_index, values_of_column in values_of_colum_of_line.items():
            for column_index, values in values_of_column.items():
                variable_name = self._variable_name(line_index, column_index)
                self._problem.addVariable(variable_name, values)

    def iterate_solutions(self):
        return self._problem.getSolutionIter()

    def format_solution(self, solution_dict, indent_text):
        chunks = []
        for line_index in range(9):
            values = []
            for column_index in range(9):
                value = solution_dict[self._variable_name(line_index, column_index)]
                values.append(value)
            chunks.append(indent_text + '%d %d %d | %d %d %d | %d %d %d' % tuple(values))

            if line_index % 3 == 2 and line_index < 8:
                chunks.append(indent_text + '------+-------+------')

        return '\n'.join(chunks)
