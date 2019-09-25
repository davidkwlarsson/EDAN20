"""
CoNLL-X and CoNLL-U file readers and writers
"""
__author__ = "Pierre Nugues"

import os


def get_files(dir, suffix):
    """
    Returns all the files in a folder ending with suffix
    Recursive version
    :param dir:
    :param suffix:
    :return: the list of file names
    """
    files = []
    for file in os.listdir(dir):
        path = dir + '/' + file
        if os.path.isdir(path):
            files += get_files(path, suffix)
        elif os.path.isfile(path) and file.endswith(suffix):
            files.append(path)
    return files


def read_sentences(file):
    """
    Creates a list of sentences from the corpus
    Each sentence is a string
    :param file:
    :return:
    """
    f = open(file).read().strip()
    sentences = f.split('\n\n')
    return sentences


def split_rows(sentences, column_names):
    """
    Creates a list of sentence where each sentence is a list of lines
    Each line is a dictionary of columns
    :param sentences:
    :param column_names:
    :return:
    """
    new_sentences = []
    root_values = ['0', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', '0', 'ROOT', '0', 'ROOT']
    start = [dict(zip(column_names, root_values))]
    for sentence in sentences:
        rows = sentence.split('\n')
        sentence = [dict(zip(column_names, row.split('\t'))) for row in rows if row[0] != '#']
        sentence = start + sentence
        new_sentences.append(sentence)
    return new_sentences


def save(file, formatted_corpus, column_names):
    f_out = open(file, 'w')
    for sentence in formatted_corpus:
        for row in sentence[1:]:
            # print(row, flush=True)
            for col in column_names[:-1]:
                if col in row:
                    f_out.write(row[col] + '\t')
                else:
                    f_out.write('_\t')
            col = column_names[-1]
            if col in row:
                f_out.write(row[col] + '\n')
            else:
                f_out.write('_\n')
        f_out.write('\n')
    f_out.close()


if __name__ == '__main__':
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']

    train_file = 'swedish_talbanken05_train.conll'
    # train_file = 'test_x'
    test_file = 'swedish_talbanken05_test_blind.conll'

    sentences = read_sentences(train_file)
    formatted_corpus = split_rows(sentences, column_names_2006)
    print(train_file, len(formatted_corpus), len(formatted_corpus[0]))
    #print(formatted_corpus[0])

    print(type(formatted_corpus))
    print(type(formatted_corpus[0]))
    print(type(formatted_corpus[0][0]))


    pairs = {}
    nbr_pairs = 0
    for sentence in formatted_corpus:
        for word in sentence:
            if word['deprel'] == 'SS': #word[column_names_2006[7]
                #print('se här!!!', sentence[int(word['head'])]['form'] )

                w2 = sentence[int(word['head'])]['form'].lower()

                tup = (word['form'].lower(), w2)
                nbr_pairs += 1
                if tup in pairs:
                    pairs[tup] += 1
                # elif (tup[1], tup[0]) in pairs:
                #     pairs[(tup[1], tup[0])] += 1
                else:
                    pairs[tup] = 1


    print('antalet hittade par: ', nbr_pairs)
    sorted_pairs = [(k, pairs[k]) for k in sorted(pairs, key=pairs.get, reverse=True)]
    i = 0
    for sp in sorted_pairs:
        print(sp)
        #print(sp[0])
        #print((sp[0][1], sp[0][0]))
        i += 1
        if i == 5:
            break


    #column_names_u = ['id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc']

    #files = get_files('../../corpus/ud-treebanks-v2.4/', 'train.conllu')
    #for train_file in files:
     #   sentences = read_sentences(train_file)
      #  formatted_corpus = split_rows(sentences, column_names_u)
       # print(train_file, len(formatted_corpus))
        #print(formatted_corpus[0])
