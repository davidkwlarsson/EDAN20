"""
dependency parser
"""

import transition
import conll
import features

import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn import linear_model
from sklearn import metrics
import pickle


def reference(stack, queue, graph):
    """
    Gold standard parsing
    Produces a sequence of transitions from a manually-annotated corpus:
    sh, re, ra.deprel, la.deprel
    :param stack: The stack
    :param queue: The input list
    :param graph: The set of relations already parsed
    :return: the transition and the grammatical function (deprel) in the
    form of transition.deprel
    """
    # Right arc
    if stack and stack[0]['id'] == queue[0]['head']:
        # print('ra', queue[0]['deprel'], stack[0]['cpostag'], queue[0]['cpostag'])
        deprel = '.' + queue[0]['deprel']
        stack, queue, graph = transition.right_arc(stack, queue, graph)
        return stack, queue, graph, 'ra' + deprel
    # Left arc
    if stack and queue[0]['id'] == stack[0]['head']:
        # print('la', stack[0]['deprel'], stack[0]['cpostag'], queue[0]['cpostag'])
        deprel = '.' + stack[0]['deprel']
        stack, queue, graph = transition.left_arc(stack, queue, graph)
        return stack, queue, graph, 'la' + deprel
    # Reduce
    if stack and transition.can_reduce(stack, graph):
        for word in stack:
            if (word['id'] == queue[0]['head'] or
                    word['head'] == queue[0]['id']):
                # print('re', stack[0]['cpostag'], queue[0]['cpostag'])
                stack, queue, graph = transition.reduce(stack, queue, graph)
                return stack, queue, graph, 're'
    # Shift
    stack, queue, graph = transition.shift(stack, queue, graph)
    return stack, queue, graph, 'sh'


def train(file, column_names_2006, feature_names):

    sentences = conll.read_sentences(file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006)

    X_dict = list()
    y = list()
    for sentence in formatted_corpus:
        stack = []
        queue = list(sentence)
        graph = {}
        graph['heads'] = {}
        graph['heads']['0'] = '0'
        graph['deprels'] = {}
        graph['deprels']['0'] = 'ROOT'

        while queue:
            X = features.extract(stack, queue, graph, feature_names, sentence)
            stack, queue, graph, trans = reference(stack, queue, graph)
            X_dict.extend(X)
            y.extend([trans])

        stack, graph = transition.empty_stack(stack, graph)

        # does this do anything??
        for word in sentence:
            word['head'] = graph['heads'][word['id']]

    vec = DictVectorizer(sparse=True)
    X_mat = vec.fit_transform(X_dict)
    return X_mat, y, vec


def test(file, vec, classifier, column_names, feature_names, idx):

    sentences = conll.read_sentences(file)
    formatted_corpus = conll.split_rows(sentences, column_names)

    for sentence in formatted_corpus:
        stack = []
        queue = list(sentence)
        graph = {}
        graph['heads'] = {}
        graph['heads']['0'] = '0'
        graph['deprels'] = {}
        graph['deprels']['0'] = 'ROOT'

        while queue:
            X = features.extract(stack, queue, graph, feature_names, sentence)
            X_trans = vec.transform(X)
            trans = classifier.predict(X_trans)
            stack, queue, graph, trans = parse_ml(stack, queue, graph, trans[0])

        stack, graph = transition.empty_stack(stack, graph)

        for word in sentence:
            if not 'head' in word:
                word['head'] = '0'
            if not 'deprel' in word:
                word['deprel'] = 'ROOT'
            if not 'phead' in word:
                word['phead'] = '_'
            if not 'pdeprel' in word:
                word['pdeprel'] = '_'

        # Does this anything
        for word in sentence:
            word['head'] = graph['heads'][word['id']]

    out = open('system_output' + str(idx) + '.txt', 'w')
    skipp = True
    for sentence in formatted_corpus:
        for word in sentence:
            # word['head'] = graph['heads'][word['id']]
            # word['deprel'] = graph['deprels'][word['id']]
            if word['id'] == '0':
                if skipp:
                    skipp = False
                else:
                    out.write('\n')

            else:
                out.write(word['id'] + '\t' + word['form'] + '\t' + word['lemma'] + '\t' + word['cpostag']
                          + '\t' + word['postag'] + '\t' + word['feats'] + '\t' + word['head'] + '\t' +
                          word['deprel'] + '\t_\t_' + '\n')
            skipp = False

    out.close()

    return 0


def parse_ml(stack, queue, graph, trans):
    if stack and trans[:2] == 'ra':     #if stack == if can_rightarc
        queue[0]['head'] = stack[0]['id']
        queue[0]['deprel'] = trans[3:]

        stack, queue, graph = transition.right_arc(stack, queue, graph, trans[3:])
        return stack, queue, graph, 'ra'
    elif transition.can_leftarc(stack, graph) and trans[:2] == 'la':
        stack[0]['head'] = queue[0]['id']
        stack[0]['deprel'] = trans[3:]
        stack, queue, graph = transition.left_arc(stack, queue, graph, trans[3:])
        return stack, queue, graph, 'la'
    elif transition.can_reduce(stack, graph) and trans == 're':
        stack, queue, graph = transition.reduce(stack, queue, graph)
        return stack, queue, graph, 're'
    else:   # shift if shift or fail
        stack, queue, graph = transition.shift(stack, queue, graph)
        return stack, queue, graph, 'sh'


if __name__ == '__main__':
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']
    feature_names = [[], [], []]
    feature_names[0] = ['stack0_POS', 'stack0_word', 'queue0_POS', 'queue0_word', 'can-re', 'can-la']
    feature_names[1] = ['stack0_POS', 'stack1_POS', 'stack0_word', 'stack1_word', 'queue0_POS', 'queue1_POS',
                        'queue0_word', 'queue1_word', 'can-re', 'can-la']
    feature_names[2] = ['stack0_POS', 'stack1_POS', 'stack0_word', 'stack1_word', 'queue0_POS', 'queue1_POS',
                        'queue0_word', 'queue1_word', '1_POS', '1_word', '2_POS', '2_word', 'can-re', 'can-la']

    train_file = 'train.conll.txt'
    test_file = 'test_blind.conll.txt'
    # train_file = 'mini.conll.txt'
    # test_file = 'miniB.conll.txt'

    print('Now we start to build and train our classifiers')
    for i in range(3):
        classifier = linear_model.LogisticRegression(penalty='l2', dual=False, solver='lbfgs', max_iter=100,
                                                     multi_class='auto')

        X_train, y_train, vec = train(train_file, column_names_2006, feature_names[i])
        model = classifier.fit(X_train, y_train)

        pathM = "lbfgs_model" + str(i) + ".p"
        with open(pathM, "wb") as handle:
            pickle.dump(classifier, handle, protocol=pickle.HIGHEST_PROTOCOL)

        pathV = "vec" + str(i) + ".p"
        with open(pathV, "wb") as handle:
            vec = pickle.dump(vec, handle, protocol=pickle.HIGHEST_PROTOCOL)

        print('Model ', i, ' has been trained and saved')


    print('models done, lets evaluate them')
    for i in range(3):
        # Extracting saved models and vectorizers
        pathM = "lbfgs_model" + str(i) + ".p"
        with open(pathM, "rb") as handle:
            clf2 = pickle.load(handle)
        pathV = "vec" + str(i) + ".p"
        with open(pathV, "rb") as handle:
            vec = pickle.load(handle)

        test(test_file, vec, clf2, column_names_2006_test, feature_names[i], i)
        print('model ' + str(i) + ' completed')


    print('terminated succesfully')
