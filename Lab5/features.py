
import transition
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn import linear_model
from sklearn import metrics
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV

# feature example :
# x = ['nil', 'nil', 'nil', 'nil', 'ROOT', 'NN', 'ROOT', 'Äktenskapet', False, False]
# y = sh

def extract(stack, queue, graph, feature_names, sentence):
    # Boolean parameters, "can do left arc" and "can do reduce"
    features = list()
    x = list()
    # print(feature_names)
    if len(feature_names) == 6:
        # print('vi gör den lilla')

        # the first 4 features
        if stack:
            x.append(stack[0]['postag'])
            x.append(stack[0]['form'])
        else:
            x.append('nil')
            x.append('nil')

        if queue:
            x.append(queue[0]['postag'])
            x.append(queue[0]['form'])
        else:
            x.append('nil')
            x.append('nil')

    else: # len(feature_names) == 10:
        # stack0_POS, stack1_POS, stack0_word, stack1_word, queue0_POS, queue1_POS, queue0_word, queue1_word
        nbr_nil = 0
        if len(stack) > 1:
            x.append(stack[0]['postag'])
            x.append(stack[1]['postag'])
            x.append(stack[0]['form'])
            x.append(stack[1]['form'])
        elif stack:
            x.append(stack[0]['postag'])
            x.append('nil')
            x.append(stack[0]['form'])
            x.append('nil')

        else:
            x.append('nil')
            x.append('nil')
            x.append('nil')
            x.append('nil')

        if len(queue) > 1:
            x.append(queue[0]['postag'])
            x.append(queue[1]['postag'])
            x.append(queue[0]['form'])
            x.append(queue[1]['form'])
        elif queue:
            x.append(queue[0]['postag'])
            x.append('nil')
            x.append(queue[0]['form'])
            x.append('nil')

        else:
            x.append('nil')
            x.append('nil')
            x.append('nil')
            x.append('nil')

    if len(feature_names) > 10: # == 14:
        # you will extract at least two more features,
        # one of them being the part of speech and the word form of
        # the word following the top of the stack in the sentence order.
        x.append('nil')
        x.append('nil')
        x.append('nil')
        x.append('nil')
        if stack:
            wftositso_id = int(stack[0]['id']) + 1
            for word in sentence:
                if int(word['id']) == wftositso_id:
                    x[-4] = word['postag']
                    x[-3] = word['form']
                    break

            wftositso_id += 1
            for word in sentence:
                if int(word['id']) == wftositso_id:
                    x[-2] = word['postag']
                    x[-1] = word['form']
                    break

    #else:
     #   print('Something is wrong')

    # can-re, can-la
    x.append(transition.can_reduce(stack, graph))
    x.append(transition.can_leftarc(stack, graph))

    features.append(dict(zip(feature_names, x)))
    # print(x)
    # print(features)

    return features

if __name__ == '__main__':
    # extract(stack, queue, graph, feature_names, sentence)
    feature_names_1 = ['stack0_POS', 'stack0_word', 'queue0_POS', 'queue0_word', 'can-re', 'can-la']
    feature_names_2 = ['stack0_POS', 'stack1_POS', 'stack0_word', 'stack1_word', 'queue0_POS', 'queue1_POS', 'queue0_word', 'queue1_word', 'can-re', 'can-la']
    feature_names_3 = ['stack0_POS', 'stack1_POS', 'stack0_word', 'stack1_word', 'queue0_POS', 'queue1_POS', 'queue0_word', 'queue1_word', '1_POS', '1_word', '2_POS', '2_word', 'can-re', 'can-la']
    f = extract([], [], [], feature_names_2, [])

    vec = DictVectorizer(sparse=True)
    X = vec.fit_transform(f)

    classifier = linear_model.LogisticRegression(penalty='l2', dual=False, solver='newton-cg', max_iter=100,
                                                 multi_class='auto')
    # solver =’warn’, lbfgs
    # multiclass = 'auto'
    # classifier = tree.DecisionTreeClassifier()
    # classifier = linear_model.Perceptron(penalty='l2')
    # classifier = svm.SVC()
    model = classifier.fit(X, y)
    print(model)

    #print(f)