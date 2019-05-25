import Agent
import NeuralNetwork
import math


class AgentAI:

    def __init__(self, parent_agent: Agent, net: NeuralNetwork):
        """
        Initiates a new agent.
        :param parent_agent: the parent agent
        :param net: the net of the agent.
        """
        self._handled_agent = parent_agent
        self._net = net

    def act(self, distances, goal):
        """
        This function makes the agent act
        :param distances: the distances from walls.
        :param goal: the goal position.
        :return: None.
        """
        inputs = distances + [math.sqrt(math.pow(goal.x - self._handled_agent._position.x, 2)),
                              math.sqrt(math.pow(goal.y - self._handled_agent._position.y, 2))]
        # print(inputs)
        result = sigmoid(self._net.activate(sigmoid(inputs)))
        result = [x - 0.5 for x in result]
        print(result)
        self._handled_agent._acceleration_x += result[0]
        self._handled_agent._acceleration_y += result[1]


def sigmoid(data):
    try:
        return [1 / (1 + math.pow(math.e, -x)) for x in data]
    except:
        return [1 for x in data]
