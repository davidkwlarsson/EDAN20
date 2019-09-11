"""
Bigram counting
Usage: python count_bigrams.py < corpus.txt
"""
__author__ = "Pierre Nugues"

import sys

import regex as re
import numpy as np


def tokenize(text):
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\,', '', text)
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


if __name__ == '__main__':
    text = open(sys.argv[1],encoding='UTF-8').read()
    words = tokenize(text)
    uni_freq, n = count_unigrams(words)
    bi_freq = count_bigrams(words)

    sentence = tokenize(open(sys.argv[2], encoding='UTF-8').read())

   # print(sentence)

    Prob_bigrams = 1


    bigrams = [tuple(sentence[inx:inx + 2])
               for inx in range(len(words) - 1)]

    print('Bigram model')
    print('==================================')
    print('wi' , 'wi+1', 'Ci,i+1', 'C(i)', 'P(wi+1|wi)')
    print('==================================')

    first_word = True
    for bigram in bigrams:
        if first_word:
            Prob_bigrams *= (uni_freq[bigram[1]] / n)
            first_word = False

        if len(bigram) < 2:
            continue

        if bigram in bi_freq:
            print(bigram[0], bigram[1], '\t', bi_freq[bigram], '\t', uni_freq[bigram[0]], '\t', bi_freq[bigram] / uni_freq[bigram[0]])
            Prob_bigrams *= (bi_freq[bigram] / uni_freq[bigram[0]])
        else:
            laplace = 1 / (uni_freq[bigram[0]] + len(uni_freq))
            print(bigram[0], bigram[1], '\t', 0, '\t', uni_freq[bigram[0]], '\t', 'backoff: ', laplace)
            Prob_bigrams *= laplace


    Geometric_mean_prob = np.power(Prob_bigrams, (1 / len(sentence)))
    Entropy_rate = - np.log2(Prob_bigrams) / len(sentence)
    Perplexity = np.power(2, Entropy_rate)
    print('==================================')
    print('Prob. bigrams: ', Prob_bigrams)
    print('Geometric mean: ',Geometric_mean_prob)
    print('Entropy rate: ',Entropy_rate)
    print('Perplexity: ',Perplexity)

    # Prob.bigrams: 2.292224542392586e-19
    # Geometric mean prob.: 0.013678098151101147
    # Entropy rate: 6.191988542790593
    # Perplexity: 73.10957919390972
