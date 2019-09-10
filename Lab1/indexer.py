
import pickle
import regex as re
import sys
import os
import math
import numpy as np


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
big_idx = {}
N = {}                  # dict with file names as keys

# Making the big dict
for f in files:
    text = open(sys.argv[1] + '/' + f).read()
    wordIter = re.finditer('\p{L}+', text.lower())
    indexes = text_to_idx(wordIter)

    output_path = 'indexes/' + f.split('/')[-1].split('.')[0] + '.idx'
    pickle.dump(indexes, open(output_path, "wb"))
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
        idf = math.log(len(files) / len(big_idx[w].keys()), 10) # not zero since we only have the word that occured at least once
        tf_idf = tf * idf
        tf_idf_list[w] = tf_idf

    N[f].append(tf_idf_list)

# Printing the tf_idf values to compare with results in the assignment
def print_tests():
    print('samlar: ', big_idx['samlar'])
    print('ände: ', big_idx['ände'])

    test_files = ['bannlyst.txt', 'gosta.txt', 'herrgard.txt', 'jerusalem.txt', 'nils.txt']
    test_words = ['känna', 'gås', 'nils', 'et']

    for f in test_files:
        print(f, N[f][0])

        for w in test_words:
            print(w, N[f][1][w])


sim_matrix = np.zeros([len(files), len(files)])

# Only fills sim_matrix under the diagonal since m_i,j = 1 and the matrix is symetric
for i in range(len(files)):
    for j in range(i):
        qd = 0
        q = 0
        d = 0
        for w in big_idx: #big_idx
            if files[i] in big_idx[w] and files[j] in big_idx[w]:
                qd += N[files[i]][1][w] * N[files[j]][1][w]
                q += N[files[i]][1][w] ** 2
                d += N[files[j]][1][w] ** 2

            elif files[i] in big_idx[w]:
                q += N[files[i]][1][w] ** 2
            elif files[j] in big_idx[w]:
                d += N[files[j]][1][w] ** 2

        if qd > 0:
            sim_matrix[i, j] = qd / (math.sqrt(q) * math.sqrt(d))

arg_max = np.argmax(sim_matrix)

max_sim = np.max(sim_matrix)      # sim_matrix[arg_max // len(files), arg_max % len(files)]
most_sim = [files[arg_max // len(files)], files[arg_max % len(files)]]

# print(sim_matrix)
print_tests()
print('the most similar texts are: ', most_sim[0], ' and ', most_sim[1], 'with cosine similarity: ', max_sim)
# kejsaren.txt  and  troll.txt with cosine similarity of ft_idf:  0.08834777884650884
