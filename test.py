class Test(object):
    def __init__(self, x):
        self.x = x
x = "Test"
a = eval(f'{x}' + '(10)')
print(a)