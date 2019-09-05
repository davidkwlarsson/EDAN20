# Input: Selma novels.
# Output: An index of all the words with their positions.
# Execution (in terminal):  python indexer.py folder_name

import pickle
import re
import sys
import os
import math
import numpy as np
import collections as Counter

# WORDS = Counter(re.findall(r'\w+', text.lower()))

#def P(word, N=sum(WORDS.values())):
 #   "Probability of `word`."
  #  return WORDS[word] / N


def get_files(dir, suffix):
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files


def text_to_idx(wordIter):
    word_idx = {}
    for word in wordIter:
        try:
            word_idx[word.group()].append(word.start())
        except:
            word_idx[word.group()] = [word.start()]

    return word_idx


files = get_files(sys.argv[1], 'txt')
# text = open(sys.argv[1]).read()

big_idx = {}

# N = [0] * len(files)    # number of word in each file
N = {}                  # dict with file names as keys

# Making the big dict
for f in files:
    # print(sys.argv[1] + '/' + f)
    text = open(sys.argv[1] + '/' + f).read()
    # text = open('Selma/nils.txt').read()
    # WORDS = re.findall(r'\w+', text.lower())
    wordIter = re.finditer(r'\w+', text.lower())
    indexes = text_to_idx(wordIter)

    N[f] = [0]
    for word in indexes:
        N[f][0] += len(indexes[word])
        # each item as a tuple with key in the first place
        try:
            big_idx[word][f] = indexes[word]
        except:
            big_idx[word] = {f: indexes[word]}


# Saving all the tf_idf values
for f in files:
    tf_idf_list = {}
    for w in big_idx:
        try:
            num = len(big_idx[w][f])

        except:
            num = 0

        tf = num / N[f][0]
        idf = math.log(len(files) / len(big_idx[w].keys()), 10)
        tf_idf = tf * idf
        tf_idf_list[w] = tf_idf

    N[f].append(tf_idf_list)

# Printing the tf_idf values to compare with results in the assignment
test_files = ['bannlyst.txt', 'gosta.txt', 'herrgard.txt', 'jerusalem.txt', 'nils.txt']
test_words = ['känna', 'gås', 'nils', 'et']
for f in test_files:
    print(f)
    for w in test_words:
        print(w, N[f][1][w])

# Getting the cosine similarity to compare all documents
# sim_matrix = [[0]*len(files)]*len(files)
# sim_matrix = [[0 for x in range(s)] for y in range(s)]
sim_matrix = np.zeros([len(files), len(files)])

for i in range(len(files)): #files
    for j in range(len(files)):
        qd = 0
        q = 0
        d = 0
        for w in big_idx: #big_idx
            if files[i] in big_idx[w] and files[j] in big_idx[w]:
                qd += len(big_idx[w][files[i]]) * len(big_idx[w][files[j]])
                q += len(big_idx[w][files[i]]) ** 2
                d += len(big_idx[w][files[j]]) ** 2
            elif files[i] in big_idx[w]:
                q += len(big_idx[w][files[i]]) ** 2
            elif files[j] in big_idx[w]:
                d += len(big_idx[w][files[j]]) ** 2

        if qd > 0:
            sim_matrix[i][j] = qd / (math.sqrt(q) * math.sqrt(d))


    print(files[i], sim_matrix[i])


#print(sim_matrix)

#print(sim_matrix)

# print(big_idx['som'])
#print(big_idx['uppklarnande'])

#print(big_idx['barndomsdrömmars'])
#print(big_idx['avskedets'])
#print(big_idx['undergång'])


#tf_i,j * log(N/n_i).

# som var varandra mycket olika

# pickle.dump(WORDS, open('save.p', "wb"))
# print(WORDS)

# where you will get the matches and the positions with the group() and start() methods.

# You will use the pickle package to write your dictionary in an file, see https://wiki.python.org/moin/UsingPickle

# Save a dictionary into a pickle file.
# import pickle
# favorite_color = {"lion": "yellow", "kitty": "red"}
# pickle.dump(favorite_color, open("save.p", "wb"))





