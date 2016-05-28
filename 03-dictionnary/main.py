import hashlib

def keep_unique_characters(s):
    r = ""
    for c in s:
        if not c in r:
            r += c
    return r


def generate_combinations(alphabet, n):
    import itertools

    res = itertools.product(alphabet,repeat=n)
    for combo in res:
        yield "".join(combo)


def encrypt(str, encryption):
    m =  hashlib.new(encryption)
    m.update(str.encode('utf-8'))
    return m.hexdigest()


encryptions = hashlib.algorithms_guaranteed

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-min", help="min length", type=int, default=4)
    parser.add_argument("-max", help="max length", type=int, default=6)
    parser.add_argument("-a", help="include a-z", action="store_true")
    parser.add_argument("-A", help="include A-Z", action="store_true")
    parser.add_argument("-n", help="include 0-9", action="store_true")
    parser.add_argument("-s", help="Specials chars")
    parser.add_argument("-m", help="encryption", choices=encryptions)
    parser.add_argument("-o","--out" ,  help="file output, if not set, print int console")
    args = parser.parse_args()

    if (args.min > args.max):
        print("Error, min bigger than max !")
        parser.print_help()
        return

    print(args)

    import string
    import sys

    alphabet = ""
    if args.a:
        alphabet += string.ascii_lowercase
    if args.A:
        alphabet += string.ascii_uppercase
    if args.n:
        alphabet += string.digits
    if args.s:
        alphabet += args.s
    if args.out:
        out = open(args.out, "w", encoding="UTF-8")
    else:
        out = sys.stdout

    alphabet = keep_unique_characters(alphabet)
    if (len(alphabet) <= 0):
        print("Error, no letters !")
        parser.print_help()
        return

    print("generating %s [%d, %d] with %s" % (args.m, args.min, args.max, alphabet))

    for i in range(args.min,args.max + 1):
        for mot in generate_combinations(alphabet, i):
            if args.m:
                out.write("%s = %s\n" % (mot, encrypt(mot, args.m)))
            else:
                out.write("%s\n" % mot)


if __name__ == '__main__':
    main()
