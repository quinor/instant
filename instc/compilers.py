from . import backends, parser, analysis, resources
import uuid
import os

def compile_llvm(filename, outname=None):
    assert filename[-4:] == ".ins"
    filename = os.path.expanduser(filename)
    basename = filename[:-4]
    asfile = "{}.ll".format(basename)
    outfile = outname or "{}.bc".format(basename)

    code = open(filename, "r").read()
    decls = parser.tld.parse(code) # no error handling
    analysis.analize(decls) # no error handling
    prog = backends.llvm_backend(decls)
    open(asfile, "w").write(prog)
    os.system("llvm-as {} -o {}".format(asfile, outfile))


def compile_jvm(filename, outname=None):
    assert filename[-4:] == ".ins"
    filename = os.path.expanduser(filename)
    basename = filename[:-4]
    asfile = "{}.j".format(basename)
    dname, cname = basename.rsplit("/", 1)
    outdir = outname or dname

    code = open(filename, "r").read()
    decls = parser.tld.parse(code) # no error handling
    analysis.analize(decls) # no error handling
    prog = backends.jvm_backend(decls, cname)
    open(asfile, "w").write(prog)
    os.system("java -jar {} {} -d {}".format(resources.JASMIN_PATH, asfile, outdir))
