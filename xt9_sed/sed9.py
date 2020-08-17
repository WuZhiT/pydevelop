import sys
import re

script = sys.argv[1]
files = sys.argv[2:]

def parse_script(script):
    if script[0] == 's':
        return ('s',script.split('/')[1:3])
    elif script[0] == 'r':
        return ('r',script.split(' ')[1:])
    else:
        print("Error, only s suppoted!")
        sys.exit(1)

def do_s(file_name, pattern, replace):
    with open(file_name) as f:
            for line in f.readlines():
                fixed = re.sub(pattern,replace,line)
                print(fixed, end="")

def do_r(file_name,in_file_name):
    content = open(in_file_name).read()
    with open(in_file_name) as f:
        for line in f.readlines():
            print(line,content,end='')

def apply_script(command, file_name, args):
    if command == 's':
        do_s(file_name, *args)
    elif command == 'r':
        print(">>>>>>>",args)
        do_r(file_name, *args)
    else:
        print("Only Support S!")
        sys.exit(1)

command, args = parse_script(script)
for file_name in files:
    apply_script(command, file_name, args)