import re
import fileinput
import sys


pattern_list = [
    "Program name",
    "Turn in files",
    "Makefile",
    "Arguments",
    "External functs.",
    "Libft authorized",
    "Description"
]
mypattern = '^(' + "|".join(pattern_list) + ')'


def mdMaker(txtPath, mdPath):
    with open(txtPath) as txt, open(mdPath, 'w') as md:
        cnt = 0
        h3flg = False
        lmode = False

        for t in txt:
            t = t.strip()

            if t.isdigit():
                pass

            elif cnt == 1:
                print(f"\n# {t}", end='\n', file=md)

            elif t == "Contents":
                t = t.replace('Contents', '## Contents')
                print(f"{t}", end='\n', file=md)
            elif re.search(r'\d+$', t):
                print(f"- {t}", end='\n', file=md)

            elif re.search(r'^Chapter', t):
                print(f"\n## {t}", end='\n', file=md)
                h3flg = True
            elif h3flg:
                print(f"### {t}", end='\n', file=md)
                h3flg = False
                lmode = False

            elif re.search(mypattern, t):
                t = re.sub(mypattern, r'\1 :', t)
                print(f"\n{t}", end='\n', file=md)
                lmode = False

            elif re.search('^•', t) or lmode:
                t = t.replace('•', '-')
                if re.search(r':$', t):
                    print(f"\n{t}", end='\n', file=md)
                elif re.search('^-', t):
                    print(f"\n{t} ", end='', file=md)
                else:
                    print(f"{t} ", end='', file=md)
                lmode = True

            elif re.search(r'(\.|\!|:)$', t) is None:
                t = t.replace('. ', '.\n')
                print(f"{t} ", end='', file=md)
            else:
                print(t, file=md)
            cnt += 1


def mdFormatter(mdPath):
    with fileinput.FileInput(mdPath, inplace=True) as f:
        lmode = False
        nflg = False
        for t in f:
            t = t.strip()
            if not t:
                pass
            elif re.search(r'^#', t):
                if not nflg:
                    print()
                print(f"{t}\n")
                nflg = True
                lmode = False

            elif re.search(mypattern, t):
                if not nflg:
                    print()
                print(f"{t}\n")
                nflg = True

            elif re.search(r'^-', t):
                if not nflg and not lmode:
                    print()
                print(t)
                lmode = True
                nflg = False

            else:
                if lmode and not nflg:
                    print()
                    lmode = False
                print(t)
                nflg = False


def main():
    args = sys.argv
    if len(args) == 3:
        try:
            mdMaker(args[1], args[2])
            mdFormatter(args[2])
        except:
            print('error')


if __name__ == '__main__':
    main()
