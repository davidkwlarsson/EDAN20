import pickle
import re
import sys
import os

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

    print(word_idx)
    return word_idx

#files = get_files(sys.argv[1], 'txt')
#text = open(sys.argv[1]).read()

text = open('Selma/nils.txt').read()
WORDS = re.findall(r'\w+', text.lower())
wordIter = re.finditer(r'\w+', text.lower())
indexes = text_to_idx(wordIter)


    
    
#pickle.dump(WORDS, open('save.p', "wb"))
print(WORDS)

