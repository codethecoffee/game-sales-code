from node import Node
import math
from copy import deepcopy

# TODO: Parse the list of genres
# Right now the best attribute is always platform
# because no two lists of genres are "identical"
# We need to look for OVERLAP in genres, not whether they are
# exactly the same


def ID3(examples, default):
    '''
    Takes in an array of examples, and returns a tree (an instance of Node)
    trained on the examples.  Each example is a dictionary of attribute:value pairs,
    and the target class variable is a special attribute with the name "Class".
    Any missing attributes are denoted with a value of "?"
    '''
    print("CALLING ID3")
    if len(examples) == 0:
        print("len == 0")
        return Node(default, True)
    info_gains = attributeList(examples)
    if allTrivial(info_gains):
        print("all trivial")
        pop_class = mostFrequentClass(examples)
        return Node(pop_class, True)
    if allSameClass(examples):
        print("all same class")
        pop_class = mostFrequentClass(examples)
        return Node(pop_class, True)
    else:
        print("other case")
        # Choose the best attribute
        best_att = chooseAttribute(examples)
        print("Best attribute: {}".format(best_att))

        # List of all the values the attribute can take
        values = [entry[best_att] for entry in examples]
        unique_values = set(values)

        # Create a root of new subtree with best attribute
        root_node = Node(best_att)

        for val in unique_values:
            # Examples with best_att == val
            sub_examples = []

            for entry in examples:
                if entry[best_att] == val:
                    sub_examples.append(entry)

            sub_tree = ID3(split(sub_examples, best_att, val), default)
            root_node.children[val] = sub_tree

        root_node.children["?"] = Node(mostFrequentClass(examples), True)

    return root_node


def allSameClass(examples):
    classes = [entry.get("Greatest_Sales") for entry in examples]
    if classes.count(classes[0]) == len(classes):
        return True
    return False


def bestAtt(attributes):
    best_ig = -math.inf
    best_att = None

    for key, value in attributes.items():
        if value > best_ig:
            best_ig = value
            best_att = key

    return best_att


def allTrivial(info_gains):
    del_trivial = []

    for key, value in info_gains.items():
        if value == 0.0 or value == 0:
            del_trivial.append(key)

    if len(del_trivial) == len(info_gains):
        return True

    return False


def chooseAttribute(examples):
    parent_entropy = entropy(examples)
    best_info_gain = 0.0
    best_att = None
    att_list = []

    for key in examples[0]:
        if key == "Greatest_Sales":
            continue
        att_list.append(key)

    value_lists = {}

    for att in att_list:
        curr_list = set()
        for entry in examples:
            curr_list.add(entry[att])
        value_lists[att] = curr_list

    for att in att_list:
        unique_values = value_lists[att]
        curr_entropy = 0.0
        for val in unique_values:
            new_data = split(examples, att, val)
            curr_prob = len(new_data) / float(len(examples))
            curr_entropy += curr_prob * entropy(new_data)
        info_gain = parent_entropy - curr_entropy
        if info_gain > best_info_gain:
            best_info_gain = info_gain
            best_att = att

    return best_att


def attributeList(examples):
    parent_entropy = entropy(examples)
    att_list = []

    for key in examples[0]:
        if key == "Greatest_Sales":
            continue
        att_list.append(key)

    value_lists = {}

    for att in att_list:
        curr_list = set()
        for entry in examples:
            curr_list.add(entry[att])
        value_lists[att] = curr_list

    info_gains = {}

    for att in att_list:
        unique_values = value_lists[att]
        curr_entropy = 0.0
        for val in unique_values:
            new_data = split(examples, att, val)
            curr_prob = len(new_data) / float(len(examples))
            curr_entropy += curr_prob * entropy(new_data)
        info_gain = parent_entropy - curr_entropy
        info_gains[att] = info_gain

    return info_gains


def majorityClass(node):
    '''
    Takes in a root node. Returns the majority class in that subtree.
    '''
    values = {}
    stack = [node]

    while (len(stack) > 0):
        curr_node = stack.pop()
        if curr_node.children == {}:
            val = curr_node.label
            if val not in values:
                values[val] = curr_node.instances
            else:
                values[val] += curr_node.instances

        for value in curr_node.children.values():
            stack.append(value)

    max_instances = -math.inf
    majority = None
    for key, value in values.items():
        if value > max_instances:
            majority = key
            max_instances = value

    return majority


def mostFrequentClass(examples):
    classes = [ex.get('Greatest_Sales') for ex in examples]
    unique_classes = (list(set(classes)))
    target = unique_classes[0]
    curr_counter = 0
    for uniques in unique_classes:
        counter = 0
        for curr_class in classes:
            if curr_class == uniques:
                counter += 1
        if counter > curr_counter:
            target = uniques
            curr_counter = counter
    return target


def numFails(node, examples):
    num_fails = 0

    for ex in examples:
        given_cls = evaluate(node, ex)
        if given_cls != ex["Greatest_Sales"]:
            num_fails += 1

    return num_fails


def alterTree(node, targetNode, majority):
    stack = [node]
    while len(stack) > 0:
        curr_node = stack.pop()
        for key, value in curr_node.children.items():
            if value is not None:
                if value.label == targetNode.label and value.instances == targetNode.instances and value.leaf == targetNode.leaf:
                    curr_node.children[key] = Node(majority, True)
                    targetNode = Node(majority, True)
                    break
            stack.append(value)
    return


def prune(node, examples):
    '''
    Takes in a trained tree and a validation set of examples.  Prunes nodes in order
    to improve accuracy on the validation data; the precise pruning strategy is up to you.
    '''
    num_fails = numFails(node, examples)

    stack = [node]
    del_node = None
    maj = None

    while (len(stack) > 0):
        curr_node = stack.pop()
        majority = majorityClass(curr_node)
        curr_fails = 0  # Counter for fails on pruned tree
        head = deepcopy(node)
        alterTree(head, curr_node, majority)
        for ex in examples:
            given_ans = evaluate(head, ex)
            if ex["Greatest_Sales"] != given_ans:
                curr_fails += 1

        if curr_fails < num_fails:
            del_node = curr_node
            maj = majority
            break

        for value in curr_node.children.values():
            if value.children != {}:
                stack.append(value)
    if del_node is None:
        return
    alterTree(node, del_node, maj)
    return


def test(node, examples):
    '''
    Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
    of examples the tree classifies correctly).
    '''
    acc = 0.0
    num_correct = 0.0
    total = len(examples)

    for ex in examples:
        answer = ex["Greatest_Sales"]
        given_ans = evaluate(node, ex)
        if answer == given_ans:
            num_correct += 1.0

    acc = num_correct / total
    return acc


def evaluate(node, example):
    '''
    Takes in a tree and one example.  Returns the Class value that the tree
    assigns to the example.
    '''
    if node.children == {}:
        return node.label

    curr_att = node.label
    ex_val = example[curr_att]
    if node.children.__contains__(ex_val):
        next_node = node.children[ex_val]
    else:
        return node.children["?"].label
    return evaluate(next_node, example)


def entropy(examples):
    num_entries = len(examples)
    classes = {}

    for entry in examples:
        label = entry["Greatest_Sales"]

        if label not in classes:
            classes[label] = 1
        else:
            classes[label] += 1

    entropy = 0.0

    for item in classes:
        curr_prob = classes[item] / num_entries
        entropy -= curr_prob * math.log(curr_prob, 2)

    return entropy


def sameClasses(examples):
    classes = [ex.get('Greatest_Sales') for ex in examples]
    first_class = examples[0].get('Greatest_Sales')
    for y in classes:
        if y != first_class:
            return False
    return True


def split(data, att, val):
    new_data = []
    for entry in data:
        if entry[att] == val:
            new_data.append(entry)
    return new_data


def getAllVals(attribute, examples):
    values = [ex.get(attribute) for ex in examples]
    return list(set(values))
