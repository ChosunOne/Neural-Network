class node:
    def __init__(self, inputs = [], inputNodes = [], outputNodes = [], modifier = 1, operation = '*', output = 0, isInput = False, isOutput = False, network = None, dead = False):
        #self.neighbors = neighbors
        self.inputNodes = inputNodes
        self.outputNodes = outputNodes
        self.modifier = modifier
        self.operation = operation
        self.inputs = inputs
        self.output = output
        self.isInput = isInput
        self.isOutput = isOutput
        self.network = network
        self.dead = dead

    def checkNode(self):
        """Checks node to see if it is a dead end"""
        if ((not self.isInput) and (not self.isOutput)) and (self.outputNodes == [] or self.inputNodes == []):
            print("Marking", self, "as dead.")
            self.dead = True

    def checkNeighbors(self):
        """Checks for dead neighbors"""
        buff = self.inputNodes

        for n in buff:
            if n[0] == None:
                buff.remove(n)
            elif n[0].dead:
                buff.remove(n)

        self.inputNodes = buff

        buff = self.outputNodes

        for n in buff:
            if n[0] == None:
                buff.remove(n)
            elif n[0].dead:
                buff.remove(n)

        self.outputNodes = buff

    #def addNeighbor(self, neighbor = None, weight = 1, location = 'out'):
    #    """Adds a neighbor to the node.  If an existing neighbor is added again, it updates the existing neighbor with new information"""
    #    if neighbor == self:
    #        return
    #
    #    for n in self.neighbors:
    #        if neighbor in n:
    #            self.neighbors.remove(n)
#
#        self.neighbors.append((neighbor, weight, location))

    def addInput(self, n = None, weight = 1):
        """Adds an input node to the node, if it already exists then it updates the weight"""
        if n == self or n == None:
            return

        #print("Adding ", n, "as an input to", self)

        buff = self.inputNodes
        for inp in buff:
            if n in inp:
                buff.remove(inp)

        self.inputNodes.append((n, weight))

    def addOutput(self, n = None, weight = 1):
        """Adds an output node to the node, if it already exists then it updates the weight"""
        if n == self or n == None:
            return

        #print("Adding", n, "as an output to", self)

        buff = self.outputNodes
        for out in buff:
            if n in out:
                buff.remove(out)

        self.outputNodes.append((n, weight))

    def sendOutput(self):
        """Sends output to all connected neighbors"""
        #print(self)
        for n in self.outputNodes:
            neighbor = n[0]
            weight = n[1]
            #print(neighbor, location)
            
            #print(self, "sending", self.output * weight, "to", neighbor)
            neighbor.inputs.append(self.output * weight)

    def calcOutput(self):
        """Calculates the output based on inputs and properties of the node"""
        #print(self.inputs)
        if len(self.inputs) == 0:
            print("Error:  No inputs to", self)
            return
        avg = 0
        for i in self.inputs:
            avg += i
        avg = avg / len(self.inputs)

        out = str(avg) + self.operation + str(self.modifier)
        out = eval(out)
        self.output = out

    def clearInputs(self):
        """Clears previous inputs"""
        self.inputs = []
