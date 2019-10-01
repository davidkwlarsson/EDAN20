
import transition


def extract(stack, queue, graph, feature_names, sentence):
    nbr_param = len(feature_names)
    features = list()
    if nbr_param == 6:
        x = list()
        x.append(stack[0][0])
        x.append(queue[0][0])
        x.append(transition.can_leftarc(stack, graph))
        x.append(transition.can_reduce(stack, graph))

    elif nbr_param == 10:
        x = list()
        for j in range(2):
            x.append(stack[0][j])

        for j in range(2):
            x.append(queue[0][j])

        x.append(transition.can_leftarc(stack, graph))
        x.append(transition.can_reduce(stack, graph))

    elif nbr_param == 16:
        x = list()
        for j in range(2):
            x.append(stack[0][j])

        for j in range(2):
            x.append(queue[0][j])

    features.append(dict(zip(feature_names, x)))
    return features
