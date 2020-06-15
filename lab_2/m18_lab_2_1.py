import re
# pre-calculated array blocks
def subsums(lst, lgth):
    subsum = 0
    total = []
    for i in range(len(lst)):
        subsum += lst[i]
        if (i + 1) % lgth == 0 and not i == 0:
            total.append(subsum)
            subsum = 0
    if subsum != 0:
        total.append(subsum)
    return total


# sum to the right end
def rsum(lst, lgth, r):
    total = 0
    i = 0
    while i + lgth <= r and i % lgth == 0:
        total += subsums(lst, lgth)[i // lgth]
        i += lgth
    for i in range(i, r + 1):
        total += lst[i]
    return total


# sum on the segment from left end to the right
def segsum(lst, lgth, l, r):
    if l == 0:
        return rsum(lst, lgth, r)
    else:
        return rsum(lst, lgth, r) - rsum(lst, lgth, l-1)

def main():
    string = input('Please enter data or filewithdata.txt : ')
    if string[-4:] == '.txt':
        file = open(string, 'r+')
        array = file.readline().split(' ')
        settings = file.readline().split(' ')
    else:
        array = string.split(' ')
        settings = input('Please enter l and r : ')
        settings = settings.split(' ')
    try:
        for i,item in enumerate(array):
            array[i] = int(item)
        for i,item in enumerate(settings):
            settings[i] = int(item)
    except ValueError:
        raise ValueError("Enter correct data, please")
    print('Sum of chosen segment is {}'.format(segsum(array, int(len(array)**0.5), settings[0], settings[1])))

main()