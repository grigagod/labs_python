import argparse
#leonardo_numbers() is a infinite generator of Leonardo numbers, I use it for more efficiency
def leonardo_numbers():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b + 1

def main(input):
    try:
        n = int(input)
        if(n >= 0):
            gen = leonardo_numbers() #initialize generator
            for i in range(n): # set endpoint of infinite generator
                next(gen)
            print(next(gen), end='\n')
        else:
            raise ValueError('Please enter correct values')
    except:
        raise ValueError('Please enter correct values')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-I", "--input", help="set output file (-O/--output file_name.txt), ", type=int) # !important
    args = parser.parse_args()
    if args.input:
        main(args.input)
    else:
        x = input('Enter integer not-negative number: ')
        main(x)