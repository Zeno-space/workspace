


# def func1(a,op):
#     from functools import reduce
#     def reduce1(op):
#         def outner(func):
#             def inner(op,*args,**kwargs):
#                 func(*args,**kwargs)
#                 op = op[1:]
#             return inner
#         return outner
#     outner = reduce1(op)
#     reduce = outner(reduce)
    
#     def func2(x,y):
#         result = 0
#         if op == '+':
#             result = x + y
#         elif op == '-':
#             result = x - y
#         elif op == '*':
#             result = x * y

#         return result

#     print(reduce(op,func2,a))

# func1([1,2,3,4],['+', '-', '*'])

# def func1(a):
#     index = 0
#     def func2(a):
#         print(a[index])
#         index += 1
        
#     func2(a)

# func1([1,2,3])

def func1(a):
    def func2():
        i = a[0]
        print(i)
    return func2

a = func1('abc')
print(list(a.__closure__))

# a = [1,2,3,4],
# b = ['+','-','*']

# 依次从列表中提取数字和运算符操作，结果是：1 + 2 - 3 * 4

