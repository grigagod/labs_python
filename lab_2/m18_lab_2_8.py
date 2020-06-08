import argparse
#function_of_power checks if passed is power of two 
function_of_power = lambda n: not(n & (n - 1))
def main(input):
    try:
        n = float(input)
        if n >= 1 and n == int(n):
            print(function_of_power(int(n)), end='\n')
        elif(n > 0 and n < 1 and 1/n == int(1/n)):
            print(function_of_power(int(1/n)), end='\n')
        else:
            print('False', end='\n')
    except:
        raise ValueError('Please enter correct values')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-I", "--input", help="set output file (-O/--output file_name.txt), ", type=float) # !important
    args = parser.parse_args()
    if args.input:
        main(args.input)
    else:
        x = input('Enter integer positive number: ')
        main(x)