
import transition


def extract(stack, queue, graph, feature_names, sentence):
    nbr_param = len(feature_names)
    features = list()
    if nbr_param == 6:
        x = list()
        if stack:
            x.append(stack[0]['postag'])
            x.append(stack[0]['form'])
        else:
            x.append('nil')
        if queue:
            x.append(queue[0]['postag'])
            x.append(queue[0]['form'])
        else:
            x.append('nil')

    elif nbr_param == 10:
        x = list()
        for j in range(2):
            try:
                x.append(stack[j]['postag'])
            except:
                x.append('nil')
        for j in range(2):
            try:
                x.append(stack[j]['form'])
            except:
                x.append('nil')
        for j in range(2):
            try:
                x.append(queue[j]['postag'])
            except:
                x.append('nil')
        for j in range(2):
            try:
                x.append(queue[j]['form'])
            except:
                x.append('nil')

    elif nbr_param == 14:
        x = list()
        for j in range(2):
            try:
                x.append(stack[j]['postag'])
            except:
                x.append('nil')
        for j in range(2):
            try:
                x.append(stack[j]['form'])
            except:
                x.append('nil')
        for j in range(2):
            try:
                x.append(queue[j]['postag'])
            except:
                x.append('nil')
        for j in range(2):
            try:
                x.append(queue[j]['form'])
            except:
                x.append('nil')
        if stack:
            word1found = False
            word2found = False
            for word in sentence:
                if int(word['id']) == int(stack[0]['id'])+1:
                    x.append(word['postag'])
                    x.append(word['form'])
                    word1found = True

            if not word1found:
                x.append('nil')
                x.append('nil')

            for word in sentence:
                if int(word['id']) == int(stack[0]['id'])+2:
                    x.append(word['postag'])
                    x.append(word['form'])
                    word2found = True

            if not word2found:
                x.append('nil')
                x.append('nil')
        else:
            x.append('nil')
            x.append('nil')
            x.append('nil')
            x.append('nil')

    x.append(transition.can_reduce(stack, graph))
    x.append(transition.can_leftarc(stack, graph))
    features.append(dict(zip(feature_names, x)))
    # print(features)
    return features
