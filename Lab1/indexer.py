import pickle
import re
import sys
import os
import numpy as np
import collections as Counter

def get_files(dir,suffix):
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

# for f in files:
#     text = open(sys.argv[1] + '/' + f).read()
#     #WORDS = re.findall(r'\wåäö+', text.lower())
#     wordIter = re.finditer('\p{L}+', text.lower())
#     indexes = text_to_idx(wordIter)

master_indexer = {}
#WORDS = Counter(re.findall(r'\w+', open('textfile.txt').read().lower()))
word_counter = {}
tot_words = {}
for f in files:
    text = open(sys.argv[1] + '/' + f).read()
    count = 0
    wordIter = re.finditer(r'\w+', text.lower())
    indexes = text_to_idx(wordIter)
    for word in indexes:
        if word in master_indexer:
            master_indexer[word][f] = indexes[word]
            word_counter[word] += len(indexes[word])
            count += len(indexes[word])
        else:
            master_indexer[word] = {}
            word_counter[word] = 0
            master_indexer[word][f] = indexes[word]
            word_counter[word] += len(indexes[word])
            count += len(indexes[word])
    tot_words[f] = count
    
    
# pickle.dump(WORDS, open('save.p', "wb"))
# for keys,values in word_counter.items():
#     print(keys)
#     print(values)

 #
 # for keys,values in master_indexer.items():
 #     print(keys)

tf_idf = {}
for f in files:
    text = open(sys.argv[1] + '/' + f).read()
    wordIter = re.finditer(r'\w+', text.lower())
    indexes = text_to_idx(wordIter)
    for word in indexes:
        tf_idf[word] = (len(indexes[word])/tot_words[f])*np.log(len(files)/len(master_indexer[word]))
#
# for keys,items in tf_idf.items():
#     print(keys)
#     print(items)

with open("save.p", "wb") as handle:
    pickle.dump(tf_idf, handle, protocol=pickle.HIGHEST_PROTOCOL)
