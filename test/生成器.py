def range2(n):
    count = 0
    while count < n:
        yield count
        count += 1
        

new_range = range2(2)
len(new_range)
next(new_range)
next(new_range)
next(new_range)
