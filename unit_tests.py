import ID3
from parser import parse
import random


def testPruningOnData(inFile):
    withPruning = []
    withoutPruning = []
    data = parse(inFile)
    # print(data)
    # for i in range(3):

    random.shuffle(data)
    train = data[:len(data)//2]
    #print("Train: {}".format(train))
    valid = data[len(data)//2:3*len(data)//4]
    test = data[3*len(data)//4:]

    tree = ID3.ID3(train, 'NA')
    acc = ID3.test(tree, train)
    print("training accuracy: ", acc)
    acc = ID3.test(tree, valid)
    print("validation accuracy: ", acc)
    acc = ID3.test(tree, test)
    print("test accuracy: ", acc)

    ID3.prune(tree, valid)
    acc = ID3.test(tree, train)
    print("pruned tree train accuracy: ", acc)
    acc = ID3.test(tree, valid)
    print("pruned tree validation accuracy: ", acc)
    acc = ID3.test(tree, test)
    print("pruned tree test accuracy: ", acc)
    withPruning.append(acc)
    tree = ID3.ID3(train+valid, 'NA')
    print("Finished ID3!")
    acc = ID3.test(tree, test)
    print("Finished calling test")
    print("no pruning test accuracy: ", acc)
    withoutPruning.append(acc)
    print(withPruning)
    print(withoutPruning)
    print("average with pruning", sum(withPruning)/len(withPruning),
          " without: ", sum(withoutPruning)/len(withoutPruning))

    with open("test.data", "a") as myfile:
        myfile.write(str(sum(withoutPruning)/len(withoutPruning)) +
                     "\n" + str(sum(withPruning)/len(withPruning)) + "\n\n")


def main():
    testPruningOnData("data/game_data.csv")
    # testID3AndTest()
    # testPruning()


if __name__ == '__main__':
    main()
