import sys
import os
import match
import emmet
import warnings

def lexer(lines:list[str]):
    tokens = []
    fintokens = []

    for i in lines:
        line = []
        tok = ''
        for j in i:
            if j.isalnum():
                tok += j
            else:
                if tok:
                    line.append(tok)
                if j != '\n': line.append(j)
                tok = ''
            if j in ">^+":
                warnings.warn("some emmet symbols for parent-child is found. please don't use indentation if you plan to use these symbols")
        tokens.append(line)
    
    indent = [' ' for i in range(4)]
    for line in tokens:
        indmatches = match.match(indent, line)
        while indmatches:
            line = line[:indmatches[0]] + line[indmatches[0]+len(indent):]
            line.insert(indmatches[0], '{tab}')
            indmatches = match.match(indent, line)
        inds = line.count('{tab}')
        fintokens.append([inds, line]) if inds == 0 else fintokens.append([inds, line[inds:]])

    emmet_str = ''
    for pairind in range(len(fintokens)):
        if pairind == 0:
            emmet_str += ''.join(i for i in fintokens[pairind][1])
        else:
            currind = fintokens[pairind][0]
            prevind = fintokens[pairind-1][0]
            content = ''.join(i for i in fintokens[pairind][1])
            if currind > prevind:
                emmet_str += '>' + content
            elif currind == prevind:
                emmet_str += '+' + content
            else:
                emmet_str += '^'*(prevind-currind) + content

    return emmet_str or 1

def emmet_parser(emmetstr): # yes, unnecessary but i want to do it
    return emmet.expand(emmetstr)

def main(args):
    if len(args) < 2: return 1
    file = args[1]
    autodel = input('remove original file? (Y/n) > ') or 'n'
    emmet_str = ''
    with open(file, 'r') as f:
        emmet_str = lexer(f.readlines())
        print(emmet_str)
    
    with open(f"{file.split('.')[0]}.html", 'w') as f:
        f.write(emmet_parser(emmet_str))
    
    ############## vv end vv ####
    if autodel.lower() == 'y':
        os.remove(file)
    return 0

if __name__ == "__main__":
    succ = main(sys.argv)
    print("\nprogram ended, got",succ)