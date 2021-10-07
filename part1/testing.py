import sys
from antlr.CoolLexer import *
from antlr.CoolParser import *
from antlr.CoolListener import *


from antlr4 import *

def gfiles_from_file(from_file_name: str, in_dir: str) -> list[str] :
    from_file = open(from_file_name, 'r')
    lines = from_file.readlines()
    files = list()
    for line in lines:
        file_name = line.split(';')[0]
        files.append(file_name)
    return list(map(lambda x : in_dir + x, files))

def evaluate_tests(files: list[str]):
    for file in files:
        print(f'in---->{file}')
        parser = CoolParser(CommonTokenStream(CoolLexer(FileStream(file))))
        tree = parser.program()

def main():
    good_files = gfiles_from_file('tests/cases.ok', 'tests/input/')
    # que hacer con .output
    print(good_files)
    evaluate_tests(good_files)

if __name__ == '__main__':
    main()
