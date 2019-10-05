"""
CoNLL-X and CoNLL-U file readers and writers
"""
__author__ = "Pierre Nugues"

import os
import operator
import collections

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
    f = open(file, encoding='UTF-8').read().strip()
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
    f_out = open(file, 'w', encoding='UTF-8')
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

# def extract_subverb(formatted_corpus):
#     subverbs = {}
#     total_subvers = 0
#     for sentence in formatted_corpus:
#         for word in sentence:
#             if word['deprel'] == 'SS':
#                 head_id = word['head']
#                 for heads in sentence:
#                     if head_id == heads['id']:
#                         head = heads['form'].lower()
#                 if (word['form'].lower(), head) in subverbs:
#                     subverbs[(word['form'].lower(), head)] += 1
#                 else:
#                     subverbs[(word['form'].lower(), head)] = 1
#                 #subvers[(word)]
#                 total_subvers += 1
#     return subverbs, total_subvers

def extract_subverb(formatted_corpus):
    subverbs = {}
    total_subvers = 0
    for sentences in formatted_corpus:
        sentence = { w['id'] : w for w in sentences}
        for word in sentences:
            if word['deprel'] == 'SS':
                head_id = word['head']
                tpl = (word['form'].lower(), sentence[head_id]['form'].lower())
                if tpl in subverbs:
                    subverbs[tpl] += 1
                else:
                    subverbs[tpl] = 1
                total_subvers += 1
    return subverbs, total_subvers

def extract_subverb_U(formatted_corpus):
    subverbs = {}
    total_subvers = 0
    for sentences in formatted_corpus:
        sentence = { w['id'] : w for w in sentences}
        for word in sentences:
            if word['deprel'] == 'nsubj':
                head_id = word['head']
                tpl = (word['form'].lower(), sentence[head_id]['form'].lower())
                if tpl in subverbs:
                    subverbs[tpl] += 1
                else:
                    subverbs[tpl] = 1
                total_subvers += 1
    return subverbs, total_subvers


# def extract_subverbobj(formatted_corpus):
#     subverbobj = {}
#     total = 0
#     for sentence in formatted_corpus:
#         for word in sentence:
#             if word['deprel'] == 'SS':
#                 verb_id = int(word['head'])
#                 verb = sentence[verb_id]
#                 if verb['deprel'] == 'OO':
#                     obj_id = int(verb['head'])
#                     obj = sentence[obj_id]
#                     tpl = (word['form'].lower(), verb['form'].lower(), obj['form'].lower())
#                     if tpl in subverbobj:
#                         subverbobj[tpl] += 1
#                     else:
#                         subverbobj[tpl] = 1
#                     total += 1
#
#
#
#
#     return subverbobj, total

def extract_subverbobj(formatted_corpus):
    subverbobj = {}
    total = 0
    for sentences in formatted_corpus:
        sentence = { w['id'] : w for w in sentences}
        found_ss = False
        found_oo = False
        for word in sentences:
            if word['deprel'] == 'SS':
                verb_id = word['head']
                verb = sentence[verb_id]
                subj = word
                found_ss = True
                for new_word in sentences:
                    if new_word['deprel'] == 'OO':
                        verb2_id = new_word['head']
                        verb2 = sentence[verb2_id]
                        obj = new_word
                        found_oo = True
                    if found_oo and found_ss and verb['id'] == verb2['id']:
                        tpl = (subj['form'].lower(), verb['form'].lower(), obj['form'].lower())
                        if tpl in subverbobj:
                            subverbobj[tpl] += 1
                        else:
                            subverbobj[tpl] = 1
                        total += 1
                        found_oo = False
                        found_ss = False




    return subverbobj, total

def extract_subverbobj_U(formatted_corpus):
    subverbobj = {}
    total = 0
    for sentences in formatted_corpus:
        sentence = { w['id'] : w for w in sentences}
        found_ss = False
        found_oo = False
        for word in sentences:

            if word['deprel'] == 'nsubj':
                verb_id = word['head']
                verb = sentence[verb_id]
                subj = word
                found_ss = True
                for new_word in sentences:
                    if new_word['deprel'] == 'obj':
                        verb2_id = new_word['head']
                        verb2 = sentence[verb2_id]
                        obj = new_word
                        found_oo = True
                    if found_oo and found_ss and verb['id'] == verb2['id']:
                        tpl = (subj['form'].lower(), verb['form'].lower(), obj['form'].lower())
                        total += 1
                        if tpl in subverbobj:
                            subverbobj[tpl] += 1
                        else:
                            subverbobj[tpl] = 1

                        found_oo = False
                        found_ss = False




    return subverbobj, total

def sort_dictvals(dict):
    sorted_rep = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
    return collections.OrderedDict(sorted_rep)


if __name__ == '__main__':
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']

    train_file = 'swedish_talbanken05_train.conll'
    # train_file = 'test_x'
    test_file = 'swedish_talbanken05_test.conll'

    sentences = read_sentences(train_file)
    formatted_corpus = split_rows(sentences, column_names_2006)
    #print(train_file, len(formatted_corpus))
    #print(formatted_corpus[0])

    sub_verbs, tot1 = extract_subverb(formatted_corpus)
    # print(tot1)
    sorted_subverb = sort_dictvals(sub_verbs)
    i = 0
    for pair in sorted_subverb:
        print(pair, ": ", sorted_subverb[pair])
        if i > 10:
            break
        i += 1

    sub_verbs_obj, tot2 = extract_subverbobj(formatted_corpus)
    print("total subverbsobjs: ", tot2)

    sorted_subverbobj = sort_dictvals(sub_verbs_obj)
    i = 0
    for trip in sorted_subverbobj:
        print(trip, ": ", sorted_subverbobj[trip])
        if i > 6:
            break
        i += 1

    column_names_u = ['id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc']

    files = get_files('ud-treebanks-v2.4/', 'train.conllu')
    for train_file in files:
        sentences = read_sentences(train_file)
        formatted_corpus = split_rows(sentences, column_names_u)
        print(train_file, len(formatted_corpus))
        sub_verbs_U, tot_U = extract_subverb_U(formatted_corpus)
        print("total from U : ", tot_U)
        sorted_subverb_U = sort_dictvals(sub_verbs_U)
        i = 0
        for pair in sorted_subverb_U:
            print(pair, ": ", sorted_subverb_U[pair])
            if i >= 5:
                break
            i += 1

        sub_verbs_obj_U, tot2_U = extract_subverbobj_U(formatted_corpus)
        print("total from U : ", tot2_U)
        sorted_subverbobj_U = sort_dictvals(sub_verbs_obj_U)
        i = 0
        for trip in sorted_subverbobj_U:
            print(trip, ": ", sorted_subverbobj_U[trip])
            if i >= 5:
                break
            i += 1

        # print(formatted_corpus[0])
