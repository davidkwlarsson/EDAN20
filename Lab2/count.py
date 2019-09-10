"""
A word counting program
Usage: python count.py < corpus.txt

Write a program to compute a sentence's probability using unigrams. You may find useful the
dictionaries that we saw in the mutual information program
"""
__author__ = "Pierre Nugues"

import sys
import regex as re
import numpy as np


def tokenize(text):
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'(\p{Lu}[^\.]+\. +)', r'<s> \1\n', text)
    text = re.sub(r'\. ', ' </s>', text)
    words = re.findall('\p{L}+|</*s>', text.lower())
    return words


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
    text = sys.stdin.read()
    words = tokenize(text)
    frequency, n = count_unigrams(words)
    sentence = tokenize(open(sys.argv[1]).read())

    # Prob.unigrams: 4.4922846219128876e-27
    # Geometric mean prob.: 0.0023187115559242404
    # Entropy rate: 8.752460922513437
    # Perplexity: 431.2739967353978

    Prob_unigrams = 1
    Geometric_mean_prob = 0
    Entropy_rate = 0
    Perplexity =  0

    for word in sentence:
        if word == '<s>':
            continue

        print(word, '\t', frequency[word], '\t', n, '\t', frequency[word] / n)
        Prob_unigrams *= (frequency[word] / n)

    Geometric_mean_prob = np.power(Prob_unigrams, (1/len(sentence)))
    Entropy_rate = - np.log2(Prob_unigrams) / len(sentence)
    Perplexity = np.power(2, Entropy_rate)


    print(Prob_unigrams)
    print(Geometric_mean_prob)
    print(Entropy_rate)
    print(Perplexity)


