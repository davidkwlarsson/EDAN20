
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
            x.append(stack[j]['postag'])

        for j in range(2):
            x.append(stack[j]['form'])

        for j in range(2):
            x.append(queue[j]['postag'])

        for j in range(2):
            x.append(queue[j]['form'])

        for word in sentence:
            if word['id'] == stack[0]['id']+1:
                x.append(word['postag'])
                x.append(word['form'])
            if word['id'] == stack[0]['id']+2:
                x.append(word['postag'])
                x.append(word['form]'])

    x.append(transition.can_leftarc(stack, graph))
    x.append(transition.can_reduce(stack, graph))
    features.append(dict(zip(feature_names, x)))
    return features
