#!/usr/bin/env python3

import sys
import os
from instc import backends, parser, analysis

if len(sys.argv) != 2:
    print("there should be exactly 1 argument!")
    exit(-1)


f = open(sys.argv[1], "r").read()
print(f)

decls = parser.tld.parse(f)
analysis.analize(decls)
prog = backends.llvm_backend(decls)

of = open("out.ll", "w").write(prog)
os.system("llvm-as out.ll -o out.bc")
os.system("lli a.bc")
