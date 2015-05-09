# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under AGPL v3 or later

import re


_ROUGH_LINE_MATCHER = re.compile('^(?:([0-9_| ]+)|[+-]+|)$')
_FIELD_MATCHER = re.compile('[_0-9]')


def _field_to_csp_values(text):
    if text == '_':
        return range(1, 9 + 1)
    else:
        return [int(text)]


def parse_puzzle(text):
    values_of_colum_of_line = {}
    line_index = 0
    for line in text.split('\n'):
        m = _ROUGH_LINE_MATCHER.match(line)
        if m.group(1):
            if line_index + 1 > 9:
                continue
            for column_index, match in enumerate(re.finditer(_FIELD_MATCHER, m.group(1))):
                if column_index + 1 > 9:
                    continue
                values = _field_to_csp_values(match.group(0))
                values_of_colum_of_line\
                        .setdefault(line_index, {})[column_index] \
                        = values
            line_index += 1

    return values_of_colum_of_line
