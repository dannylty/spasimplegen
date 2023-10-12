with open('generate.in', 'r') as f:
    code = f.read()

lines = code.split('\n')

def edit(s):
    return '"' + s + r'\n"'

with open('formatted.in', 'w') as f:
    f.write("\n".join([edit(s) for s in lines][:-1]))