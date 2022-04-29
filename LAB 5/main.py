from SimpleParser import SimpleParser


# function for scanning the .txt file
def scan_file(string):
    grammar = open(string)
    grammar = grammar.readlines()
    prog = []
    for line in grammar:
        newline = line.strip()
        prog.append(newline)
    return prog


# scanning the txt file
program = scan_file('grammar.txt')

# building the parser
x = SimpleParser(program)
x.build_parser()

# printing the first and last matrix and the simple precedence table
print("FIRST")
print(x.first)
print()
print("LAST")
print(x.last)
print()
print("PRECEDENCE TABLE")
print(x.simple_pr_table)
print()

# parsing the word
word = 'adbbdb'
x.parse(word)
