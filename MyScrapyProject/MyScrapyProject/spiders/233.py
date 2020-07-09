import sys
import os
from sys import path
path.append(os.path.abspath(os.path.dirname(__file__)).split('MyScrapyProject')[0])


for p in path:
    print(p)