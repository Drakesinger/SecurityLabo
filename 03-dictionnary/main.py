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
    import itertools

    res = itertools.product(lettres,repeat=n)
    for combo in res:
        yield "".join(combo)


def crypte(str, methode):
    m =  hashlib.new(methode)
    m.update(str.encode('utf-8'))
    return m.hexdigest()


methodes = hashlib.algorithms_guaranteed

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-min", help="min length", type=int, default=4)
    parser.add_argument("-max", help="max length", type=int, default=6)
    parser.add_argument("-a", help="include a-z", action="store_true")
    parser.add_argument("-A", help="include A-Z", action="store_true")
    parser.add_argument("-n", help="include 0-9", action="store_true")
    parser.add_argument("-s", help="Specials chars")
    parser.add_argument("-m", help="methode", choices=methodes)
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

    for i in range(args.min,args.max + 1):
        for mot in mygen(lettres, i):
            if args.m:
                out.write("%s = %s\n" % (mot, crypte(mot, args.m)))
            else:
                out.write("%s\n" % mot)


if __name__ == '__main__':
    main()
