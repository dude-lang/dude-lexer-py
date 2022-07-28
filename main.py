from argparse import ArgumentParser, FileType
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dude_lexer import tokenize


def create_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('--file', '-f', type=FileType('r', encoding='utf-8'), required=True)
    parser.add_argument('--export', '-e', action='store_true')
    parser.add_argument('--print', '-p', action='store_true')
    parser.add_argument('--time', '-t', action='store_true')

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    t1 = datetime.now()
    tokens = tokenize(args.file.read())
    t2 = datetime.now()

    if args.time:
        d = relativedelta(t2, t1).normalized()
        print(f'Tokenizing took {d.seconds}s {d.microseconds // 1000}ms')

    if args.print:
        print(' '.join(map(lambda x: f"'{x}'", tokens)))

    if args.export:
        with open(args.file.name + '.tok', 'w') as file:
            file.write(' '.join(tokens))


if __name__ == '__main__':
    main()
