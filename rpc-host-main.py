import sys
from rpcfunc import func

def get_input():
    return sys.stdin.read()

def put_output(output_str: str):
    sys.stdout.write(output_str)
    sys.stdout.write('\0')

if __name__ == '__main__':
    input_str = get_input()
    output_str = func(input_str)
    put_output(output_str)
