"""
Gold standard parser
"""
__author__ = "Pierre Nugues"

import transition
import conll
import features

import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn import linear_model
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV


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
    # print('sh', [], queue[0]['cpostag'])
    stack, queue, graph = transition.shift(stack, queue, graph)
    return stack, queue, graph, 'sh'



def get_Xy(test_file, column_names_2006, feature_names):

    sentences = conll.read_sentences(test_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006)

    X_dict = list()
    y = list()
    p = 0
    for sentence in formatted_corpus:
        stack = []
        queue = list(sentence)
        graph = {}
        graph['heads'] = {}
        graph['heads']['0'] = '0'
        graph['deprels'] = {}
        graph['deprels']['0'] = 'ROOT'
        transitions = []

        while queue:
            X = features.extract(stack, queue, graph, feature_names, sentence)
            stack, queue, graph, trans = reference(stack, queue, graph)
            transitions.append(trans)
            X_dict.extend(X)
            y.extend([trans])

        stack, graph = transition.empty_stack(stack, graph)

        for word in sentence:
            word['head'] = graph['heads'][word['id']]

    # print(type(X_dict[0]), X_dict[0])
    vec = DictVectorizer(sparse=True)
    X_mat = vec.fit_transform(X_dict)
    # print(np.shape(X_mat))

    return X_mat, y


if __name__ == '__main__':
    train_file = 'mini.conll.txt'
    # test_file = 'test_blind.conll.txt'
    test_file = 'mini_test.conll.txt'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']

    # feature_names = ['stack0_POS', 'stack0_word', 'queue0_POS', 'queue0_word', 'can-re', 'can-la']
    feature_names = ['stack0_POS', 'stack1_POS', 'stack0_word', 'stack1_word', 'queue0_POS', 'queue1_POS',
                       'queue0_word', 'queue1_word', 'can-re', 'can-la']
    # feature_names = ['stack0_POS', 'stack1_POS', 'stack0_word', 'stack1_word', 'queue0_POS', 'queue1_POS',
    #                   'queue0_word', 'queue1_word', '1_POS', '1_word', '2_POS', '2_word', 'can-re', 'can-la']


    classifier = linear_model.LogisticRegression(penalty='l2', dual=False, solver='lbfgs', max_iter=100,
                                                 multi_class='auto')

    # solver = lbfgs is good. Also sag and saga is good for large scale problems. liblinear handles only binary class.
    # multiclass: ‘auto’ selects ‘ovr’ if the data is binary, or if solver=’liblinear’, and otherwise selects ‘multinomial’
    X_train, y_train = get_Xy(train_file, column_names_2006, feature_names)
    model = classifier.fit(X_train, y_train)

    X_test, y_test = get_Xy(test_file, column_names_2006, feature_names)
    print(np.shape(X_train), np.shape(X_test))

    y_pred = classifier.predict(X_test)

    y_train = np.array(y_train)
    print(len(y_pred), y_pred[:10])
    print(len(y_train), y_train[:10])

    report = metrics.classification_report(y_test, y_pred, labels=None, target_names=None,
                                            sample_weight=None, digits=2, output_dict=False)

    print(report)

