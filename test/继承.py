class A(object):
    def test(self):
        print('from A')

class B(A):
    def test(self):
        print('from B')

class C(B):
    def test(self):
        print('from C')

class I(A):
    def test(self):
        print('from I')
class D(C):
    # def test(self):
    #     print('from D')
    pass
class G(I):
    def test(self):
        print('from G')

class E(G):
    def test(self):
        print('from E')





class F(D,E):
    # def test(self):
    #     print('from F')
    pass
f1=F()
f1.test()
print(F.__mro__) #只有新式才有这个属性可以查看线性列表，经典类没有这个属性