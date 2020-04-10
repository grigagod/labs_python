import os
import argparse
import tracemalloc

def next_letter_from_file(index, depth): 
    # This function is used for getting code of next letters(if the first letters are the same)
    file = open('file_{}.txt'.format(index), 'r+')
    file.seek(depth)
    letter_code = ord(file.read(1))
    file.close()
    return letter_code


def sorting(array, *flag):   
    array_code = map(lambda element: ord(element[0]), array)
    array_index = range(len(array))
    dictionary = list(zip(array_code, array_index)) # use such 'tuple' for sorting it by the first element (code)
                                                    # and in the same time connect code of each element with its posinion(index)
                                                    # to obtain needed result easily
    def deep_comparing(L, R, i, j, *flag):
        # L/R in this case is a pair (code of first letter, index of element)
        # This function is used in merge_sort and has two cases:
        # 1) To compare first letters of rows (flag == True)
        # 2) To compare first letters of words in a row (First step in merge_sort_main)
        # Differences:
        # While sorting words in a row, we pass to the sorting function 
        # a array of words (full words) and we have them in memory, 
        # so we can get next code of letters from array (e.g array[index][letter_number])
        # When it's time to sort rows(each are located in separate file) 
        # and we have to get code of next letters for comparing, 
        # we get them using next_letter_from_file 
        if(flag == True):
            depth = 0
            left = L[0]
            right = R[0]
            while(left == right):
                depth+=1
                if(right != 32  and left != 32): # break point when the first word in row is ended (32 is char code of Space)
                    left = next_letter_from_file(L[1], depth)
                    right = next_letter_from_file(R[1], depth)
                    continue
                elif(right == 32 and left != 32):
                    return (L, i+1, j)
                else:
                    return(R, i, j+1)
            else:
                if(left < right):
                    return (L, i+1, j)
                else:
                    return(R, i, j+1)
        else:
            depth = 0
            length_L = len(array[L[1]]) # would be one of the breakpoints
            length_R = len(array[R[1]]) # would be one of the breakpoints
            left = L[0]
            right = R[0]
            while(left == right):
                depth+=1
                if(depth < length_L and depth < length_R):
                    left = ord(array[L[1]][depth])
                    right = ord(array[R[1]][depth])
                    continue
                elif(depth >= length_R and depth < length_L):
                    return (L, i+1, j)
                else:
                    return (R, i, j+1)
            else:
                if(left < right):
                    return (L, i+1, j)
                else:
                    return(R, i, j+1)

    def merge_sort(arr): 
        if len(arr) >1: 
            mid = len(arr)//2 #Finding the mid of the array 
            L = arr[:mid] # Dividing the array elements  
            R = arr[mid:] # into 2 halves 
            merge_sort(L) # Sorting the first half 
            merge_sort(R) # Sorting the second half 
    
            i = j = k = 0
            
            # Copy data to temp arrays L[] and R[] 
            while i < len(L) and j < len(R):
                if(L[i][0] == R[j][0]): # if the codes of first letters are the same we need to compare them deeper
                    (arr[k], i , j) = deep_comparing(L[i], R[j], i, j, flag)
                else:
                    if L[i][0] < R[j][0]: 
                        arr[k] = L[i] 
                        i+=1
                    else: 
                        arr[k] = R[j] 
                        j+=1
                k+=1
            
            # Checking if any element was left 
            while i < len(L): 
                arr[k] = L[i] 
                i+=1
                k+=1
            
            while j < len(R): 
                arr[k] = R[j] 
                j+=1
                k+=1

    merge_sort(dictionary)
    if(flag):
        return (i[1] for i in dictionary) # we obtain in what order we need to merge our buffer_files in a result_file
    else:
        return tuple(map(lambda element: array[element[1]], dictionary)) # more efficient for future joining list of words in a row

def show_progress(input_filename, current_size, comments):
    max_size = os.path.getsize(input_filename)
    print('\r'+ comments + '{}'.format(round(current_size/max_size *100, 1)) + "%", end='')


def merge_sort_main(input_filename, output_filename = 'sorted.txt', status_flag = False, memory_flag = False):
    # This is main function which consists of two main loops:
    # 1) We sort words in each row (by the way preparing for the row sorting)
    # after the first loop we sort rows and obtain sequence
    # 2) Row merging from buffer_files in result_file in a correct sequence also delering buffer_files
    first_letters = [] # to get list of letters to sort rows after word sorting
    current_size = 0
    if(memory_flag):
        tracemalloc.start()
    with open(str(input_filename), 'r+') as file: # word sorting 
        for i, sorted_row in enumerate(file):
            sorted_row = ' '.join(sorting(sorted_row.rstrip().split(' ')))
            buffer_file = open("file_{}.txt".format(i),'w+') # generation of indexed file
            print(sorted_row, end='\n', file=buffer_file)
            buffer_file.close()
            first_letters.append(sorted_row[0])
            if(status_flag):
                current_size+= len(sorted_row) +1
                show_progress(str(input_filename), current_size, 'Progress (in sorting words) is: ')
            sorted_row = None
    print('\n')
    sequence = sorting(first_letters, True)
    result_file = open(str(output_filename), 'w+')
    for i in sequence:
        buffer_file = open("file_{}.txt".format(i),'r+')
        print((buffer_file.readline()), end='', file=result_file)
        if(status_flag):
            show_progress(str(input_filename), os.path.getsize(str(output_filename)), 'Progress (in sorting rows) is: ')
        buffer_file.close()
        os.remove("file_{}.txt".format(i))
    if(memory_flag):
        current, peak = tracemalloc.get_traced_memory()
        print('\nInput file size is: {}'.format(os.path.getsize(input_filename)//1048576) + ' MB')
        print(f"Current memory usage is: {current // 1048576} MB;\nPeak was: {peak // 1048576} MB")
        tracemalloc.stop()
        




if(__name__ == '__main__'):
    # when we don't use merge_sort_main as module we can provide extra tips for command line using 
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--progress", help="show progress of sorting", action="store_true") # extra tip: progress bar
    parser.add_argument("-M", "--memory", help="show usage of memory", action="store_true") # extra tip: memory usage
    parser.add_argument("-I", "--input", help="set input file (-I/--input file_name.txt)") # !important
    parser.add_argument("-O", "--output", help="set output file (-O/--output file_name.txt)", action="store_true")
    args = parser.parse_args()
    merge_sort_main(args.input, args.output, args.progress, args.memory)

