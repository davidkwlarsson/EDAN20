"""
Gold standard parser
"""
__author__ = "Pierre Nugues"

import transition
import conll
import features
from sklearn.feature_extraction import DictVectorizer
from sklearn import linear_model
from sklearn import metrics
import time
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
    # print('sh', [], queue[0]['cpostag'])
    stack, queue, graph = transition.shift(stack, queue, graph)
    return stack, queue, graph, 'sh'


if __name__ == '__main__':
    train_file = 'swedish_talbanken05_train.conll'
    test_file = 'swedish_talbanken05_test_blind.conll'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']

    sentences = conll.read_sentences(train_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006)

    # feature_names = ['stack0_POS', 'stack0_WORD', 'queue0_POS', 'queue0_WORD', 'can-re' , 'can-la']
    # feature_names = ['stack0_POS', 'stack1_POS', 'stack0_WORD', 'stack1_WORD',
    #                  'queue0_POS', 'queue1_POS', 'queue0_WORD', 'queue1_WORD', 'can-re', 'can-la']
    feature_names = ['stack0_POS' , 'stack1_POS', 'stack0_WORD', 'stack1_WORD',
                     'queue0_POS', 'queue1_POS', 'queue0_WORD', 'queue1_WORD',
                     '1_POS', '1_WORD', '2_POS', '2_WORD', 'can-re', 'can-la']

    if len(feature_names) == 6:
        classifier_filename = "classifier1.p"
    elif len(feature_names) == 10:
        classifier_filename = "classifier2.p"
    else:
        classifier_filename = "classifier3.p"

    X_dict = []
    Y = []
    DEPRELS = []
    sent_cnt = 0
    for sentence in formatted_corpus:
        sent_cnt += 1

        if sent_cnt % 1000 == 0:
            print(sent_cnt, 'sentences of', len(formatted_corpus), flush=True)
        stack = []
        queue = list(sentence)
        graph = {}
        graph['heads'] = {}
        graph['heads']['0'] = '0'
        graph['deprels'] = {}
        graph['deprels']['0'] = 'ROOT'
        transitions = []

        # print('Equal graphs:', transition.equal_graphs(sentence, graph))
        x_dict = []
        deprels = []
        while queue:
            x = features.extract(stack, queue, graph, feature_names, sentence)
            # x_dict.extend(x)
            X_dict.extend(x)
            stack, queue, graph, trans = reference(stack, queue, graph)
            transitions.append(trans)
            deprels.append(trans[2:])
        # print('Equal graphs:', transition.equal_graphs(sentence, graph))

        # Y.extend(transitions)
        stack, graph = transition.empty_stack(stack, graph)

        # if transition.equal_graphs(sentence, graph):
        #     X_dict.extend(x_dict)
        DEPRELS.extend(deprels)
        Y.extend(transitions)
        # if not transition.equal_graphs(sentence, graph):
        #     for word in sentence:
        #         print(word['form'])
        #     print(transitions)
        #     print(graph)
        #     break

        # Poorman's projectivization to have well-formed graphs.
        for word in sentence:
            word['head'] = graph['heads'][word['id']]
        # print(transitions)
        # print(graph)

    for k in range(4):
        print(X_dict[k].values(), "  , y = ", Y[k])


    print("Encoding the features...")
    # Vectorize the feature matrix and carry out a one-hot encoding
    vec = DictVectorizer(sparse=True)
    X = vec.fit_transform(X_dict)
    # print(vec.get_feature_names())
    print(X.shape)
    print(len(Y))
    training_start_time = time.clock()
    print("Training the model...")
    classifier = linear_model.LogisticRegression(solver='lbfgs', multi_class='auto', n_jobs=-1)
    model = classifier.fit(X, Y)
    y_train_predict = classifier.predict(X)
    print("Classification report for classifier %s:\n%s\n"
          % (classifier, metrics.classification_report(Y, y_train_predict)))
    # print(model)
    print("writing to pickle file: --> ", classifier_filename)
    with open(classifier_filename, "wb") as handle:
        pickle.dump(classifier, handle)

