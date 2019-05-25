import numpy
import random


class Neuron:

    def __init__(self):
        """
        Initiates a new neuron
        """
        self._connected_neurons = []
        self._input = 0
        self._weights = []

    def feed_forward(self):
        """
        This function feeds the signal forward to all connected neurons
        :return: None
        """
        c = 0
        for neuron in self._connected_neurons:
            neuron._input += self._weights[c] * self._input
            c += 1

    def flush(self):
        """
        This function flushes the neuron signal.
        :return: None
        """
        self._input = 0


class NeuralNetwork:
    def __init__(self, layers, layer_definition):
        """
        This function initializes a new NeuralNetwork
        :param layers: amount of layers
        :param layer_definition: a list containing definition of each layer.
        """
        self._layers = []
        self._definition = layer_definition
        for i in range(0, layers):
            self._layers.append([])
            for c in range(0, layer_definition[i]):
                self._layers[len(self._layers) - 1].append(Neuron())
        c = 0
        for i in range(0, layers - 1):
            for source_neuron in self._layers[i]:
                for target_neuron in self._layers[i + 1]:
                    source_neuron._connected_neurons.append(target_neuron)
                    source_neuron._weights.append(random.uniform(-1,1))

        for neuron in self._layers[len(self._layers) - 1]:
            neuron._weights.append(random.uniform(-1,1))

    def activate(self, inputs):
        """
        This activates the NN on the given inputs.
        :param inputs: the inputs
        :return: the list of outputs.
        """
        for layer in self._layers:
            for neuron in layer:
                neuron.flush()
        c = 0
        for neuron in self._layers[0]:
            neuron._input = inputs[c]
            c += 1

        for layer in self._layers:
            for neuron in layer:
                neuron.feed_forward()
        return [n._input * n._weights[0] for n in self._layers[len(self._layers) - 1]]

    def print(self):
        """
        This function prints the NN weights
        :return:
        """
        for layer in self._layers:
            for neuron in layer:
                print(neuron._weights)


def Merge(net1, net2, mutation_rate=0.3):
    """
    This function does a genetic merge between two NN's with a given mutation rate.
    :param net1: the first NN
    :param net2: the second NN
    :param mutation_rate: the chance of mutation upon merging
    :return:
    """
    merged_net = NeuralNetwork(len(net1._layers), net1._definition)
    count = 1
    for d in net1._definition:
        count *= d
    c = 0;
    for i in range(0, len(net1._layers)):
        for j in range(0, len(net1._layers[i])):
            for k in range(0, len(net1._layers[i][j]._weights)):
                if c > count / 2:
                    merged_net._layers[i][j]._weights[k] = (net1._layers[i][j]._weights[k]);
                else:
                    merged_net._layers[i][j]._weights[k] = (net2._layers[i][j]._weights[k]);
                c += 1

    for t in range(0,3):
        i = random.randint(0,len(net1._layers)-1)
        j = random.randint(0,len(net1._layers[i])-1)
        k = random.randint(0,len(net1._layers[i][j]._weights)-1)
        merged_net._layers[i][j]._weights[k] *= random.uniform(-2,2)
    return merged_net
