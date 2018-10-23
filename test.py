#!/usr/bin/env python3

import sys

# if len(sys.argv) != 2:
#     print("there should be exactly 1 argument!")
#     exit(-1)

#print(sys.argv[1])

import parser

print (parser.expression.parse("1 + 2 + d + c + 3"))
