#/usr/bin/env python3
from src.lambda_function import lambda_handler
from pprint import pprint

if __name__ == '__main__':
    print(lambda_handler(None, None))
