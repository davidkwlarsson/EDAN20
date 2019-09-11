"""
A word counting program
Usage: python count.py < corpus.txt
"""
__author__ = "Pierre Nugues"

import sys
import regex as re
import numpy as np


def tokenize(text):
    words = re.findall('\p{L}+', text)
    return words

def tokenize5(text):
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\,', r'', text)
    text = re.sub(r'(\p{Lu}[^\.]+[\.\!\?] +)', r'<s> \1\n', text)
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
    # cutoff = 0.01
    # if (len(sys.argv) > 2):
    #     cutoff = float(sys.argv[2])
    text = open(sys.argv[1], encoding='UTF-8').read().lower()
    words = tokenize5(text)
    frequency, n = count_unigrams(words)
    # prob = frequency
    # for word in frequency.keys():
    #     prob[word] = frequency[word]/n

    sentence = open(sys.argv[2], encoding='UTF-8').read().lower()
    prob_words = tokenize5(sentence)
    prob_uni = 1
    for word in prob_words:
        prob_uni *= frequency[word]/n
        print(word, frequency[word], n,frequency[word]/n)

    geo_mean = np.power(prob_uni, 1/len(prob_words))
    entropy = -1/len(prob_words)*np.log2(prob_uni)
    perplexity = np.power(2, entropy)
    print('===================================')
    print('prob unigram', prob_uni)
    print('geometric mean', geo_mean)
    print('entropy', entropy)
    print('perplexity', perplexity)

    # for word in sorted(frequency.keys(), key=frequency.get, reverse=True):
    #     if (frequency[word]/n < cutoff): break
    #     print(word, '\t', frequency[word]/n)
