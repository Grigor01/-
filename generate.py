import random
import argparse
import sys
import random
import pickle

def SentenceGenerator(data, origin, l):
    if l == 0:
        l = random.randint(1, 25)
    space = ''
    w1, w2 = '7', '7'
    if origin != "":
        ComboKeys = list(data.keys())
        random.shuffle(ComboKeys)
        for key in ComboKeys:
            if key[0] == origin:
                w1, w2 = key
                break
        if (w1, w2) == ('7', '7'):
            print("Invalid origin.\n")
            sys.exit(0)
        space += w1 + ' ' + w2
    for _ in range(l):
        w1, w2 = w2, unirand(data[w1, w2])
        if w2 == '7': break
    return space + '\n'


def RandNextWord(sequence):
    sum, frequence = 0, 0
    for pair, freq in sequence:
        sum += freq
    rand = random.uniform(0, sum)
    for token, freq in seq:
        frequence += freq
        if rand < frequence:
            return token


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Генерирует текст из модели')
    
    parser.add_argument(
        '--seed',
        dest='origin',
        type=str,
        default="7",
        help='Начальное слово. Если не указано,\
        выбираем слово случайно из всех слов.')
    
    parser.add_argument(
        '--length',
        dest='l',
        type=int,
        help='Длина генерируемой последовательности.',
        required=True)

    parser.add_argument(
        '--model',
        dest='data',
        type=argparse.FileType('rb'),
        help='Полученная модель',
        required=True)

    parser.add_argument(
        '--output',
        dest='output',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='output model (default: stdout)')
   
    args = parser.parse_args()
    args.output.write(generate_sentence
                      (pickle.load(args.data), args.origin, args.l))