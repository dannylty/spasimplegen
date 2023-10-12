with open('generate.in', 'r') as f:
    code = f.read()

lines = code.split('\n')
stmt_num = 0
def edit(s):
    bare = s.replace(' ', '')
    splitted = s.split()
    if not (bare in ['{', '}', '}else{'] or (len(splitted) == 3 and splitted[0] == 'procedure')):
        global stmt_num 
        stmt_num += 1
        return '"' + s + r'\n"' + f' // {stmt_num}'
    return '"' + s + r'\n"'

with open('formatted.in', 'w') as f:
    f.write("\n".join([edit(s) for s in lines][:-1]))