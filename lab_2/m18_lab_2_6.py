"""
The parser below is a predictive, recursive-descent parser. The use of a predictive parser
is possible because JSON has an LL(k) grammar. Specifically, JSON has an LL(1) grammar,
a fact that is hinted at in the `parse_json` function: `parse_json` looks ahead by only
one character (not even a whole JSON token) in order to decide how to parse the string.
"""

### Top-level Function

def from_json(string, flag):
    if flag:
        with open(string, 'r') as content_file:
            s = content_file.read()
    else:
        s = string
    i = skip_leading_whitespace(s, 0)
    assert i < len(s), 'string cannot be emtpy or blank'

    try:
        python_element, i = parse_json(s, i)
        validate_json(s, i, condition=(i == len(s)))
        return python_element
    except IndexError:
        raise_invalid_json_error('Unexpected end of string:', s, len(s))


### Parsing JSON and Translating it to Python
# In the parsing functions below, two invariants are implicitly enforced for values
# at the index `i`:
#   1. When `i` is passed in as an argument to a function, `s[i]` is not whitespace.
#   2. When `i` is returned from a function, `s[i]` is not whitespace.
# Therefore, whenever a function is called or the value returned from a function is
# handled, we can immediately begin using `s[i]` to inspect the next JSON token we need
# to handle.
# Other conditions on the value of `s[i]` are more explicitly enforced below, using
# the `validate_json` function.

def parse_json(s, i):
    first_char = s[i]

    if first_char == '{':
        return parse_object(s, i)
    elif first_char == '[':
        return parse_array(s, i)
    elif first_char == '"':
        return parse_string(s, i)
    elif first_char == 'n':
        return parse_null(s, i)
    elif first_char == 't':
        return parse_true(s, i)
    elif first_char == 'f':
        return parse_false(s, i)
    else:
        return parse_number(s, i)


def parse_object(s, i):
    validate_json(s, i, expected='{')

    i = skip_trailing_whitespace(s, i)
    python_dict = {}

    while s[i] != '}':
        key, i = parse_string(s, i)
        validate_json(s, i, expected=':')
        value, i = parse_json(s, skip_trailing_whitespace(s, i))

        python_dict[key] = value

        if s[i] == ',':
            i = skip_trailing_whitespace(s, i)
            validate_json(s, i, not_expected='}')
        else:
            validate_json(s, i, expected='}')

    return python_dict, skip_trailing_whitespace(s, i)


def parse_array(s, i):
    validate_json(s, i, expected='[')

    i = skip_trailing_whitespace(s, i)
    python_list = []

    while s[i] != ']':
        python_element, i = parse_json(s, i)
        python_list.append(python_element)

        if s[i] == ',':
            i = skip_trailing_whitespace(s, i)
            validate_json(s, i, not_expected=']')
        else:
            validate_json(s, i, expected=']')

    return python_list, skip_trailing_whitespace(s, i)


def parse_string(s, i):
    validate_json(s, i, expected='"')

    i += 1
    i0 = i

    while s[i] != '"':
        i += 1

    python_string = bytes(s[i0:i], "utf-8").decode("unicode_escape") 
    return python_string, skip_trailing_whitespace(s, i)


def parse_null(s, i):
    validate_json(s, i, condition=(s[i:i+4] == 'null'))
    return None, skip_leading_whitespace(s, i+4)

def parse_true(s, i):
    validate_json(s, i, condition=(s[i:i+4] == 'true'))
    return True, skip_leading_whitespace(s, i+4)


def parse_false(s, i):
    validate_json(s, i, condition=(s[i:i+5] == 'false'))
    return False, skip_leading_whitespace(s, i+5)


def parse_number(s, i):
    validate_json(s, i, condition=(s[i] in '-IN' or '0' <= s[i] <= '9'))

    if s[i] == 'N':
        validate_json(s, i, condition=(s[i:i+3] == 'NaN'))
        return float('nan'), skip_leading_whitespace(s, i+3)
    elif s[i] == 'I':
        validate_json(s, i, condition=(s[i:i+8] == 'Infinity'))
        return float('inf'), skip_leading_whitespace(s, i+8)
    elif s[i] == '-' and s[i+1] == 'I':
        validate_json(s, i, condition=(s[i:i+9] == '-Infinity'))
        return float('-inf'), skip_leading_whitespace(s, i+9)

    is_number_char = lambda char: '0' <= char <= '9' or char in '+-Ee.'
    j = next((j for j in range(i, len(s)) if not is_number_char(s[j])), len(s))
    use_float = any(s[i] in 'Ee.' for i in range(i, j))
    python_converter = float if use_float else int

    try:
        return python_converter(s[i:j]), skip_leading_whitespace(s, j)
    except ValueError:
        raise_invalid_json_error('Invalid JSON number:', s, i)


### Skipping over Whitespace between JSON Tokens

import re

_whitespace_matcher = re.compile(r'\s*')
skip_leading_whitespace = lambda s, i: _whitespace_matcher.match(s, i).end()
skip_trailing_whitespace = lambda s, i: skip_leading_whitespace(s, i+1)


### Validating Input

def validate_json(s, i, expected=None, not_expected=None, condition=None):
    assert expected is not None or not_expected is not None or condition is not None,\
        'expected, not_expected, or condition must be declared'

    expected is not None and s[i] == expected or \
    not_expected is not None and s[i] != not_expected or \
    condition is True or \
    raise_invalid_json_error('Unexpected token:', s, i)


def raise_invalid_json_error(message, s, i):
    err_message = JSON_VALIDATION_ERROR_MESSAGE_TEMPLATE.format(
        message=message,
        json=s,
        caret=caret(i)
    )
    raise ValueError(err_message)


def caret(i):
    return ' ' * i + '^'



JSON_VALIDATION_ERROR_MESSAGE_TEMPLATE = """{message}
{json}
{caret}"""
