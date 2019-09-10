"""
Bigram counting
Usage: python count_bigrams.py < corpus.txt
"""
__author__ = "Pierre Nugues"

import sys

import regex


def tokenize(text):
    words = regex.findall("\p{L}+", text)
    return words


def count_bigrams(words):
    bigrams = [tuple(words[inx:inx + 2])
               for inx in range(len(words) - 1)]
    frequencies = {}
    for bigram in bigrams:
        if bigram in frequencies:
            frequencies[bigram] += 1
        else:
            frequencies[bigram] = 1
    return frequencies

def count_unigrams(words):
    frequency = {}
    n = 0
    for word in words:
        n += 1
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency, n

if __name__ == '__main__':
    text = open(sys.argv[1], encoding='UTF-8').read().lower()
    sentence = open(sys.argv[2], encoding='UTF-8').read().lower()
    words = tokenize(text)
    frequency_bigrams = count_bigrams(words)
    frequency_words, tot_words = count_unigrams(words)
    for bigram in frequency_bigrams:
        print(frequency_bigrams[bigram], "\t", bigram)
