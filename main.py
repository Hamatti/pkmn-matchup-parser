import sys
from parser import Parser

if __name__ == '__main__':
    try:
        rk9_id = sys.argv[1]
        limitless_id = sys.argv[2]
        parser = Parser(rk9_id, limitless_id)
    except IndexError as e:
        print(f'Usage: python {__file__} <rk9__id> <limitless_id>')
        sys.exit(1)

    parser.run()
