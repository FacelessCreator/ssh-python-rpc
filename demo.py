from sshrpc import SSHRPC

rpc = SSHRPC('localhost', '22', 'test', '1234')

def func(in_str: str) -> str:
    return "I've got '{}' string".format(in_str)

def func2(in_str: str) -> str:
    return in_str.swapcase()

answer = rpc.exec_func(func, 'hello ♥')
print(answer)

answer = rpc.exec_func(func2, 'It seems nice!')
print(answer)

