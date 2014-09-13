import network
import copy

neunet = network.network(size = 20, depth = 2, mutaterate = .2, numin = 2, numout = 2)
neunet.arrangeNodes()
neunet.checkNodes()

inputlist = [1, 2]
expectedoutputlist = [3, 6]

neunet.setInputs(inputlist)
result = neunet.calcOutputs()
topscoreTable = neunet.scoreNetwork(expectedoutputlist)
print(topscoreTable)

loops = 0


while (max(topscoreTable) > .0001):

    mutant = copy.deepcopy(neunet)
    mutant.mutateNodes()

    mutant.setInputs(inputlist)
    result = mutant.calcOutputs()
    scoreTable = mutant.scoreNetwork(expectedoutputlist)

    passtest = True
    i = 0

    for field in scoreTable:
        if field > topscoreTable[i]:
            passtest = False
        i += 1

    if passtest:
        topscoreTable = scoreTable
        neunet = mutant
        print(result)

    loops += 1
print("Final result of", result)
print("Result achieved in", loops, "iterations")
    