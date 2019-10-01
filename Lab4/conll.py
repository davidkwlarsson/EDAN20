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


def get_pairs(pairs, corpus, subj):
    nbr_pairs = 0
    for sentence in corpus:
        for word in sentence:
            if word['deprel'] == subj:
                w2 = sentence[int(word['head'])]['form']
                tup = (word['form'].lower(), w2.lower())
                nbr_pairs += 1
                if tup in pairs:
                    pairs[tup] += 1
                else:
                    pairs[tup] = 1


    return pairs, nbr_pairs

def get_triples(triples, corpus, subj, obj):
    nbr_triples = 0
    for sentence in corpus:
        for word in sentence:
            # Find verb to subject
            if word['deprel'] == subj:
                w2 = sentence[int(word['head'])]
                # Find same verb again but from object
                for w3 in sentence:
                    if w3['deprel'] == obj and w3['head'] == w2['id']:
                        tup = (word['form'].lower(), w2['form'].lower(), w3['form'].lower())
                        nbr_triples += 1
                        if tup in triples:
                            triples[tup] += 1
                        else:
                            triples[tup] = 1

    return triples, nbr_triples

def remove_lines(corpus):
    new_corpus = []
    for sentence in corpus:
        new_sentence = []
        for word in sentence:
            if len(word['id']) == 1:
                # Adds word without range in index to new sentence
                new_sentence.append(word)
        # Adds the new sentence to the new corpus
        new_corpus.append(new_sentence)

    return new_corpus

if __name__ == '__main__':
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']

    train_file = 'swedish_talbanken05_train.conll'
    # train_file = 'test_x'
    test_file = 'swedish_talbanken05_test_blind.conll'

    sentences = read_sentences(train_file)
    formatted_corpus = split_rows(sentences, column_names_2006)
    print(train_file, len(formatted_corpus), len(formatted_corpus[0]))

    pairs = {}
    pairs, nbr_pairs = get_pairs(pairs, formatted_corpus, 'SS')
    print('antalet hittade par: ', nbr_pairs)
    sorted_pairs = [(k, pairs[k]) for k in sorted(pairs, key=pairs.get, reverse=True)]
    i = 0
    for sp in sorted_pairs:
        print(sp)
        i += 1
        if i == 5:
            break

    triples = {}
    triples, nbr_triples = get_triples(triples, formatted_corpus, 'SS', 'OO')
    print('antalet hittade triplar: ', nbr_triples)
    sorted_triples = [(k, triples[k]) for k in sorted(triples, key=triples.get, reverse=True)]
    i = 0
    for st in sorted_triples:
        print(st)
        i += 1
        if i == 5:
            break

    column_names_u = ['id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc']

    # EN: SS -> nsubj OO ->nobj
    #files = get_files('ud-treebanks-v2.4/UD_Swedish-Talbanken', 'train.conllu')
    file = 'en_esl-ud-train.conllu'

    sentences = read_sentences(file)
    formatted_corpus = split_rows(sentences, column_names_2006)
    #formatted_corpus = split_rows(sentences, column_names_u)
    # Remove all lines that include range in id field
    formatted_corpus = remove_lines(formatted_corpus)

    pairs = {}
    pairs, nbr_pairs = get_pairs(pairs, formatted_corpus, 'nsubj')
    print('antalet hittade par: ', nbr_pairs)
    sorted_pairs = [(k, pairs[k]) for k in sorted(pairs, key=pairs.get, reverse=True)]
    i = 0
    for sp in sorted_pairs:
        print(sp)
        i += 1
        if i == 5:
            break

    triples = {}
    triples, nbr_triples = get_triples(triples, formatted_corpus, 'nsubj', 'obj')

    print('antalet hittade triplar: ', nbr_triples)
    sorted_triples = [(k, triples[k]) for k in sorted(triples, key=triples.get, reverse=True)]
    i = 0
    for st in sorted_triples:
        print(st)
        i += 1
        if i == 5:
            break

def unused():
    files_EN = get_files('English', 'train.conllu')
    files_FR = get_files('French', 'train.conllu')
    files_SP = get_files('Spanish', 'train.conllu')

    F = [files_EN, files_FR, files_SP]
    languages = ['English', 'French', 'Spanish']

    pairs = [{}, {}, {}]
    triples = [{}, {}, {}]
    for i in range(len(F)):
        files = F[i]
        lan = languages[i]
        print('Here commes the result from the ', lan, ' corpuses:')

        for train_file in files:
            sentences = read_sentences(train_file)
            formatted_corpus = split_rows(sentences, column_names_u)
            # print(train_file, len(formatted_corpus))
            # print(formatted_corpus[0])

            # Remove all lines that include range in id field
            formatted_corpus = remove_lines(formatted_corpus)
            get_pairs(pairs[i], formatted_corpus, 'nsubj')
            get_triples(triples[i], formatted_corpus, 'nsubj', 'obj')

        print('antalet hittade par: ', nbr_pairs)
        sorted_pairs = [(k, pairs[i][k]) for k in sorted(pairs[i], key=pairs[i].get, reverse=True)]
        i = 0
        for sp in sorted_pairs:
            print(sp)
            i += 1
            if i == 5:
                break
