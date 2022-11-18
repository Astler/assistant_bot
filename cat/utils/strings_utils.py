import random


def shuffle(string):
    temp = list(string)
    random.shuffle(temp)
    return ''.join(temp)
