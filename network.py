import node
import random

random.seed()

class network:
    def __init__(self, inputs = [], outputs = [], hidden = [], size = 1, numin = 1, numout = 1, mutaterate = .5, depth = 1):
        self.inputs = inputs
        self.outputs = outputs
        self.size = size
        self.numin = numin
        self.numout = numout
        self.mutaterate = mutaterate
        self.hidden = hidden
        self.depth = depth

        if self.inputs == []:
            i = 0
            while(i < numin):
                n = node.node()
                n.inputNodes = []
                n.outputNodes = []
                n.inputs = []
                self.inputs.append(n)
                n.isInput = True
                i += 1

        if self.outputs == []:
            i = 0
            while(i < numout):
                n = node.node()
                n.inputNodes = []
                n.outputNodes = []
                n.inputs = []
                self.outputs.append(n)
                n.isOutput = True
                i += 1

        if self.hidden == []:
            i = 0
            while(i < size):
                n = node.node()
                n.inputNodes = []
                n.outputNodes = []
                n.inputs = []
                self.hidden.append(n)
                i += 1

        if depth > size:
            print('Warning:  Depth greater than the number of total nodes, reducing depth to accomodate the number of nodes.')
            depth = size


    def chunks(self, l, n):
        """ Yield successive n-sized chunks from l.
        """
        for i in range(0, len(l), n):
            yield l[i:i+n]

    def arrangeNodes(self):
        """Connects all the nodes of the network together"""
        nodesPerLayer = int(self.size / self.depth)

        layer = 0
        hiddenChunks = list(self.chunks(self.hidden, nodesPerLayer))

        while(layer < self.depth):
            hidden = hiddenChunks[layer]
            #print("Layer = ", layer)
            if layer == 0:
                #print("self.inputs =", self.inputs)
                for n in self.inputs:
                    #print("hidden =", hidden)
                    for h in hidden:
                        weight =  random.random()
                        if weight > 1:
                            weight = 1
                        elif weight < 0:
                            weight = 0

                        h.addInput(n, weight)
                        n.addOutput(h, weight)

                for h in hidden:
                    for n in hiddenChunks[layer + 1]:
                        weight =  random.random()
                        if weight > 1:
                            weight = 1
                        elif weight < 0:
                            weight = 0

                        h.addOutput(n, weight)
                        n.addInput(h, weight)


            if layer == self.depth - 1:
                #print("self.outputs = ", self.outputs)
                for n in self.outputs:
                    #print("hidden = ", hidden)
                    for h in hidden:
                        weight =  random.random()
                        if weight > 1:
                            weight = 1
                        elif weight < 0:
                            weight = 0

                        h.addOutput(n, weight)
                        
                        n.addInput(h, weight)

            else:
                for h in hidden:
                    for n in hiddenChunks[layer + 1]:
                        weight =  random.random()
                        if weight > 1:
                            weight = 1
                        elif weight < 0:
                            weight = 0

                        h.addOutput(n, weight)
                        n.addInput(h, weight)

            layer += 1

    def setInputs(self, inputs):
        """Sets the inputs values for the input nodes"""
        if len(inputs) != len(self.inputs):
            print("Error:  Number of inputs must equal the number of input nodes.")
            return

        i = 0
        for inp in inputs:
            #print("Setting input value", inp, "to", self.inputs[i])
            self.inputs[i].output = inp
            i += 1

    def calcOutputs(self):
        """Transform the inputs to the networks into the outputs from the network"""

        for n in self.hidden:
            n.clearInputs()

        for n in self.outputs:
            n.clearInputs()

        for inp in self.inputs:
            #print(self.inputs)
            inp.sendOutput()

        nodesPerLayer = int(self.size / self.depth)
        layer = 0
        hiddenChunks = list(self.chunks(self.hidden, nodesPerLayer))

        while(layer < self.depth):
            hidden = hiddenChunks[layer]
            for h in hidden:
                if h.dead == False:
                    h.calcOutput()
                    h.sendOutput()
            layer += 1
        finalout = []
        for n in self.outputs:
            n.calcOutput()
            finalout.append(n.output)
        return finalout

    def scoreNetwork(self, expectedOutputs = []):
        """Compares the output of the network with the expected output and creates a score"""
        if len(expectedOutputs) != len(self.outputs):
            print("Error:  Number of expected outputs must equal the number of output nodes")
            return

        i = 0
        difftable = []
        for out in expectedOutputs:
            diff = (out - self.outputs[i].output)**2
            difftable.append(diff)

        return difftable

    def mutateNode(self, n):
        """Randomly changes properties of the node"""

        for inp in n.inputNodes:
            neigh = inp[0]
            weight = inp[1]

            chance = random.random()
            if chance < .15:
                weight = weight * (random.random() * 2)
                if weight < 0:
                    weight = 0
                elif weight > 1:
                    weight = 1

                n.addInput(n = neigh, weight = weight)
                neigh.addOutput(n = n, weight = weight)

        for out in n.outputNodes:
            neigh = inp[0]
            weight = inp[1]

            chance = random.random()
            if chance < .15:
                weight = weight * (random.random() * 2)
                if weight < 0:
                    weight = 0
                elif weight > 1:
                    weight = 1

                n.addOutput(n = neigh, weight = weight)
                neigh.addInput(n = n, weight = weight)

        chance = random.random()
        if chance < .05:
            n.modifier = n.modifier * (2 * random.random())

        chance = random.random()
        if chance < .01:
            chance = random.random()
            if chance < .25:
                n.operator = '+'
            elif chance < .50:
                n.operator = '-'
            elif chance < .75:
                n.operator = '*'
            else:
                n.operator = '/'

    def mutateNodes(self):
        for h in self.hidden:
            chance = random.random()
            if chance < self.mutaterate:
                self.mutateNode(h)

    def checkNodes(self):
        for n in self.hidden:
            n.checkNode()
            n.checkNeighbors()

