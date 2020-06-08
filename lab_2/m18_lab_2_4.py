def flatten_it(obj):
    if(hasattr(obj, '__iter__') and not isinstance(obj, str)):
        for element in obj:
            if(hasattr(element,'__iter__')):
                yield from flatten_it(element)
            else:
                yield element
    else:
        raise ValueError(obj, 'is not iterable')
    

lis = flatten_it([1, 2, 3, [2, 3, 4,[1,[]]]])
print(list(lis))
