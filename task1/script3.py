from collections import Counter

from script1 import script1


def script3():
    counter = Counter()
    counter.update(fig.tag for fig in script1())

    print('Кол-во фигур по типам:')
    for fig, count in counter.most_common():
        print(f'{fig}: {count}')


if __name__ == "__main__":
    script3()
