import hashlib

def asUnique(s):
    r = ""
    for c in s:
        if not c in r:
            r += c
    return r

class genletter:
    def __init__(self, lettres):
        self.__lettres = lettres
        self.__i = 0
        self.__len = len(lettres) -1
    def hasNext(self):
        return self.__i < self.__len
    def next(self):
        self.__i += 1
        return self.current
    def current(self):
        return self.__lettres[self.__i]
    def reset(self):
        self.__i = 0


def mygen(lettres, n):
    tab = [genletter(lettres) for i in range(n)]
    tabInv = reversed(tab)
    tabInv = tab
    hasNext = True
    while hasNext:
        yield "".join([g.current() for g in tabInv])[::-1]
        hasNext = False
        for g in tab:
            if g.hasNext():
                g.next()
                hasNext = True
                break
            else:
                g.reset()
def md5(str):
    m =  hashlib.md5()
    m.update(str.encode('utf-8'))
    return m.hexdigest()
methodes = {
    "md5" : md5,
    "sha1" : md5,
    "sha512" : md5
}

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-min", help="min length", type=int, default=4)
    parser.add_argument("-max", help="max length", type=int, default=6)
    parser.add_argument("-a", help="include a-z", action="store_true")
    parser.add_argument("-A", help="include A-Z", action="store_true")
    parser.add_argument("-n", help="include 0-9", action="store_true")
    parser.add_argument("-s", help="Specials chars")
    parser.add_argument("-m", help="methode", choices=methodes.keys())
    parser.add_argument("-o","--out" ,  help="file output, if not set, print int console")
    args = parser.parse_args()
    if (args.min > args.max):
        print("Error, min bigger than max !")
        parser.print_help()
        return
    print(args)
    import string
    import sys
    lettres = ""
    if args.a:
        lettres += string.ascii_lowercase
    if args.A:
        lettres += string.ascii_uppercase
    if args.n:
        lettres += string.digits
    if args.s:
        lettres += args.s
    if args.out:
        out = open(args.out, "w", encoding="UTF-8")
    else:
        out = sys.stdout
    lettres = asUnique(lettres)
    if (len(lettres) <= 0):
        print("Error, no letters !")
        parser.print_help()
        return
    print("generating %s [%d, %d] with %s" % (args.m, args.min, args.max, lettres))

    crypt = None
    if args.m:
        crypt = methodes[args.m]
    for i in range(args.min,args.max + 1):
        for mot in mygen(lettres, i):
            if crypt:
                out.write("%s = %s\n" % (mot, crypt(mot)))
            else:
                out.write("%s\n" % mot)

if __name__ == '__main__':
    main()