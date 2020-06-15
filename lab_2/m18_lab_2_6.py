def from_json(string, flag):
    if flag:
        with open(string, 'r') as content_file:
            s = content_file.read()
    else:
        s = string
    i = skip_leading_whitespace(s, 0)
    assert i < len(s), 'string cannot be emtpy or blank'

    try:
        python_element, i = json_parser(s, i)
        json_validator(s, i, condition=(i == len(s)))
        return python_element
    except IndexError:
        raise_invalid_json_error('Unexpected_token end of string:', s, len(s) - 1)


### Parsing JSON and Translating it to Python
# The following rule is implemented in the parsing functions below:
# Whenever `i` is passed in as an argument to a function or returned from a function, `s[i]` is not whitespace.
# Therefore, we can immediately begin using `s[i]` to inspect the next JSON token we need
# to handle.
# Other conditions on the value of `s[i]` are handled by  
# the `json_validator` function.

def json_parser(s, i):
    first_char = s[i]

    if first_char == '{':
        return object_parser(s, i)
    elif first_char == '[':
        return array_parser(s, i)
    elif first_char == '"':
        return string_parser(s, i)
    elif first_char == 'n':
        return null_parser(s, i)
    elif first_char == 't':
        return true_parser(s, i)
    elif first_char == 'f':
        return false_parser(s, i)
    else:
        return number_parser(s, i)


def object_parser(s, i):

    i = skip_trailing_whitespace(s, i)
    python_dict = {}

    while s[i] != '}':
        key, i = string_parser(s, i)
        json_validator(s, i, expected_token=':')
        value, i = json_parser(s, skip_trailing_whitespace(s, i))

        python_dict[key] = value

        if s[i] == ',':
            i = skip_trailing_whitespace(s, i)
            json_validator(s, i, not_expected_token='}')
        else:
            json_validator(s, i, expected_token='}')

    return python_dict, skip_trailing_whitespace(s, i)


def array_parser(s, i):

    i = skip_trailing_whitespace(s, i)
    python_list = []

    while s[i] != ']':
        python_element, i = json_parser(s, i)
        python_list.append(python_element)

        if s[i] == ',':
            i = skip_trailing_whitespace(s, i)
            json_validator(s, i, not_expected_token=']')
        else:
            json_validator(s, i, expected_token=']')

    return python_list, skip_trailing_whitespace(s, i)


def string_parser(s, i):

    i += 1
    i0 = i

    while s[i] != '"':
        i += 1

    python_string = bytes(s[i0:i], "utf-8").decode("unicode_escape") 
    return python_string, skip_trailing_whitespace(s, i)


def null_parser(s, i):
    json_validator(s, i, condition=(s[i:i+4] == 'null'))
    return None, skip_leading_whitespace(s, i+4)

def true_parser(s, i):
    json_validator(s, i, condition=(s[i:i+4] == 'true'))
    return True, skip_leading_whitespace(s, i+4)


def false_parser(s, i):
    json_validator(s, i, condition=(s[i:i+5] == 'false'))
    return False, skip_leading_whitespace(s, i+5)


def number_parser(s, i):
    json_validator(s, i, condition=(s[i] in '-IN' or '0' <= s[i] <= '9'))

    if s[i] == 'N':
        json_validator(s, i, condition=(s[i:i+3] == 'NaN'))
        return float('nan'), skip_leading_whitespace(s, i+3)
    elif s[i] == 'I':
        json_validator(s, i, condition=(s[i:i+8] == 'Infinity'))
        return float('inf'), skip_leading_whitespace(s, i+8)
    elif s[i] == '-' and s[i+1] == 'I':
        json_validator(s, i, condition=(s[i:i+9] == '-Infinity'))
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

_matcher_pattern = re.compile(r'\s*')
skip_leading_whitespace = lambda s, i: _matcher_pattern.match(s, i).end()
skip_trailing_whitespace = lambda s, i: skip_leading_whitespace(s, i+1)


### Validating Input

def json_validator(s, i, expected_token=None, not_expected_token=None, condition=None):
    assert expected_token is not None or not_expected_token is not None or condition is not None,\
        'expected_token, not_expected_token, or condition must be declared'

    expected_token is not None and s[i] == expected_token or \
    not_expected_token is not None and s[i] != not_expected_token or \
    condition is True or \
    raise_invalid_json_error('Unexpected_token token : ', s, i)


def raise_invalid_json_error(message, s, i):
    err_message = JSON_VALIDATION_ERROR_MESSAGE_TEMPLATE.format(
        message=message,
        json=s[:i+1],
    )
    raise ValueError(err_message)



JSON_VALIDATION_ERROR_MESSAGE_TEMPLATE = """{message}
{json}
"""
