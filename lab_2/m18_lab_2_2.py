import string
import random
import os
import argparse

alphabet = list(string.ascii_letters) # needed for random generation

def show_progress(output_filename, max_size):
    current_size = os.path.getsize(output_filename)
    print('\r'+ 'Progress is: {}'.format(round(current_size/max_size *100, 1)) + "%", end='')

def fileGenerator(output_filename, limit, quantity_of_words = (10, 100), length_of_word = (3, 10), progressFlag = False):
    if( not (output_filename[:-3] == 'txt' and (quantity_of_words[1]-quantity_of_words[0]) and quantity_of_words[0] and (length_of_word[1]-length_of_word[0]) and length_of_word[0])):
        raise ValueError('Incorrect input')
    currentpart = ''
    file = open(output_filename, 'w')
    maximum_of_file = round(limit * 1048576)  # from MB to bytes
    maximum_of_row = (length_of_word[1] + 1) * quantity_of_words[1] # this is done to stop main row-genetator and start generating pseudo random row
    maximum_of_word = length_of_word[1] # this is done to stop generating pseudo random row and start generate pseudo random word
    i = 0
    if progressFlag:
        while i < maximum_of_file - maximum_of_row: # main row-generator
            currentpart = rowGenerator(quantity_of_words, length_of_word)
            file.write(currentpart)
            show_progress(output_filename, maximum_of_file)
            i += len(currentpart)
        file.write(lastRowGenerator(length_of_word, (maximum_of_file - i), maximum_of_word)) # generating pseudo random (last) row
        file.close()
        show_progress(output_filename, maximum_of_file)
        print('\n')
    else:
        while i < maximum_of_file - maximum_of_row: # main row-generator
            currentpart = rowGenerator(quantity_of_words, length_of_word)
            file.write(currentpart)
            i += len(currentpart)
        file.write(lastRowGenerator(length_of_word, (maximum_of_file - i), maximum_of_word)) # generating pseudo random (last) row
        file.close()

def rowGenerator(quantity, length): 
    Q = random.choice(range(*quantity))
    row = ''
    for i in range(Q - 1):
        row = row + wordGeneranor(length) + ' '
    return row + wordGeneranor(length) + '\n'

def wordGeneranor(length):
    L = random.choice(range(*length))
    return ''.join(random.choice(alphabet) for x in range(L))

def lastRowGenerator(length, difference, maxWordLength):
    result = ''
    currentWord = ''
    i = 0
    while i < (difference - maxWordLength):
         currentWord = wordGeneranor(length)
         i = i + len(currentWord)
         result = result + currentWord
    return result + lastWordGenerator((difference - i))
        

def lastWordGenerator(length):
    return ''.join(random.choice(alphabet) for x in range(length))


if(__name__ == '__main__'):
    # when we don't use fileGenerator as module we can provide extra tips for command line using 
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--progress", help="show progress of generation", action='store_true')
    parser.add_argument("-Q", "--quantity", help="set quantity of words in a row", default=(10, 100), type=int, nargs=2)
    parser.add_argument("-L", "--length", help="set length of words in a row", default=(3, 10), type=int, nargs=2)
    parser.add_argument("-S", "--size", help="set size of output in MB", type=float, required=True) # !important
    parser.add_argument("-O", "--output", help="set output file (-O/--output file_name.txt), ", required=True) # !important
    args = parser.parse_args()
    fileGenerator(args.output, args.size, tuple(args.quantity), tuple(args.length), args.progress)