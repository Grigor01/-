import argparse
import re
import sys
import os
import pickle
import glob
from collections import defaultdict

Lang = re.compile(u'[а-яА-Я]+')

def LinesGen(text, reg):
    for line in text:
        if reg:
            yield line.lower()
        else:
            yield line

def TokensGen(lines):
    for line in lines:
        for token in Lang.findall(line):
            yield token

def TrigramsGen(tokens):
    w1, w2 = '7', '7'
    for w3 in tokens:
        yield w1, w2, w3

def train(text, reg):
    model = {}
    MyLines = LinesGen(text, reg)
    MyTokens = TokensGen(lines)
    MyTrigrams = TrigramsGen(tokens)
    bigramm, trigramm = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for w1, w2, w3 in trigrams:
        bigramm[w1, w2] += 1
        trigramm[w1, w2, w3] += 1

    for (w1, w2, w3), frequance in trigramm.items():
        if (w1, w2) in model:
            model[w1, w2].append((w3, freq / bigramm[w1, w2]))
        else:
            model[w1, w2] = [(w3, freq / bigramm[w1, w2])]
    print(model)
    return model


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(description='Директорий, регистр и модель текста.')
    
    parser.add_argument(
        '--input-dir',
        dest='InDir',
        type=str,
        help=' Путь к директории, в которой лежит коллекция документов.\
        Если данный аргумент не задан, считать, что тексты вводятся из stdin.')
    
    parser.add_argument(
        '--lc',
        dest='reg',
        action='store_true',
        help='Приводить тексты к lowercase.')
    
    parser.add_argument(
        '--model',
        dest='data',
        type=argparse.FileType('wb'),  
        help='В заданном директорийе создает файл в котором запишеться модель.',
        required=True)
        
    args = parser.parse_args()
    if not args.InDir:
        args.data.write(pickle.dumps(train(sys.stdin, args.reg)))
    else:
        os.chdir(args.InDir)
        command = 'cat ' + ' '.join(
            glob.glob('*.txt')) + ' > /tmp/generated_text.txt'
        os.system(cmd)
        text = open('/tmp/generated_text.txt', 'r')
        args.data.write(pickle.dumps(train(text, args.reg)))