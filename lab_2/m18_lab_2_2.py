import string
import random


alphabet = list(string.ascii_letters) # needed for random generation


def fileGenerator(output_filename, limit, quantity_of_words = (10, 100), length_of_word = (3, 10)):
    currentpart = ''
    file = open(output_filename + '.txt', 'w')
    maximum_of_file = round(limit * 1048576)  # from MB to bytes
    maximum_of_row = (length_of_word[1] + 1) * quantity_of_words[1] # this is done to stop main row-genetator and start generating pseudo random row
    maximum_of_word = length_of_word[1] # this is done to stop generating pseudo random row and start generate pseudo random word
    i = 0
    while i < maximum_of_file - maximum_of_row: # main row-generator
        currentpart = rowGenerator(length_of_word, quantity_of_words)
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


fileGenerator('testlow', 0.01)

