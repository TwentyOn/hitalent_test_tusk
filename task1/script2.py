from collections import Counter

from script1 import script1


def script2():
    counter = Counter()
    counter.update(fig.attrib['label'] for fig in script1())

    print('Кол-во фигур по классам:')
    for cls, count in counter.most_common():
        print(f'{cls}: {count}')


if __name__ == '__main__':
    script2()
