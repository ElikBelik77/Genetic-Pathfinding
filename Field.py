from Agent import Agent
import math
from graphics import *
import threading
import random
import numpy
import NeuralNetwork


class Field:
    def __init__(self, width, height, goal):
        """
        This function initializes a new game field.
        :param width: the widht of the game field.
        :param height: the height of the game field.
        :param goal: the position of the goal.
        """
        self._window = GraphWin("Field", width, height)
        self._window.setBackground('white')
        self._collidables = []
        self._goal = goal
        self._agents = []
        ellipsis = Circle(goal, 4)
        ellipsis.setFill('black')
        ellipsis.draw(self._window)

    def add_agent(self, agent):
        """
        Adds an agent to the game field.
        :param agent: the agent to add
        :return: None
        """
        self._agents.append(agent)

    def add_collidable(self, p1, p2):
        """
        This function adds a rectangular collideable.
        :param p1: the bottom left point.
        :param p2: the top right point.
        :return:
        """
        self._collidables.append((p1, p2))
        rect = Rectangle(p1, p2)
        rect.setFill('gray')
        rect.draw(self._window)
        pass

    def record_collidables(self, n):
        """
        This function gets user input for n collidables
        :param n: the amount of collidables to read.
        :return: None
        """
        while n > 0:
            p1 = self._window.getMouse()
            p2 = self._window.getMouse()
            topLeft = Point(min(p1.x, p2.x), min(p1.y, p2.y))
            bottomRight = Point(max(p1.x, p2.x), max(p1.y, p2.y))
            self.add_collidable(topLeft, bottomRight)
            n -= 1

    def start_simulation(self, time_limit):
        """
        This function starts the simulation.
        :param time_limit: the time limit of each generation.
        :return: None
        """
        dead_count = 0
        now = time.time()

        while dead_count < len(self._agents) and time.time() < now + time_limit:
            for agent in self._agents:
                agent.update(self._window, self._collidables, self._goal)
                if not agent._dead:
                    agent.calculate_raycasts(self._collidables, self._window)

            dead_count = 0
            for agent in self._agents:
                if agent._dead:
                    dead_count += 1
            # time.sleep(1 / 60)

    def get_fitness_vector(self):
        """
        This function returns the fitness vectors for all the agents.
        :return: the fitness vector.
        """
        fitness = []

        for agent in self._agents:
            fitness.append((agent, math.sqrt(math.pow(agent._position.x - self._goal.x, 2)
                                             + math.pow(agent._position.y - self._goal.y, 2)) + 1000 * agent._dead))
        return fitness

    def get_best_agents(self, amount):
        """
        This function gets the best agents of the current generation.
        :param amount: the amount of agents to pick.
        :return: the best agents.
        """
        fitness = self.get_fitness_vector()
        fitness.sort(key=lambda tup: tup[1])
        print(fitness)
        return fitness[0:amount]

    def clear(self):
        """
        This function clears the game field.
        :return:
        """
        for agent in self._agents:
            agent.undraw()
        agents = []


def breed(agents, max_amount):
    """
    This function breads agents.
    :param agents: the agents to breed.
    :param max_amount: the maximum amount of children to create.
    :return:
    """
    result = []
    for a1 in agents:
        for a2 in agents:
            if a1 == a2:
                pass
            result.append(Agent(Point(50, 50), 0.01, 0.01, 0.01, 0.01,
                                NeuralNetwork.Merge(a1[0].get_neural_net(), a2[0].get_neural_net())))

        result.append(Agent(Point(50, 50), 0.01, 0.01, 0.01, 0.01,
                            NeuralNetwork.Merge(a1[0].get_neural_net(), a1[0].get_neural_net())))
    return result[0:max_amount]


'''
net = NeuralNetwork.NeuralNetwork(3, [3, 5, 2])
net.print()

print(net.activate([50, 50, 50]))
'''

goal = Point(550, 450)
f = Field(700, 700, goal)
n = 30
while n > 0:
    f.add_agent(Agent(Point(50, 50), 0.01, 0.01, 0.01, 0.01, NeuralNetwork.NeuralNetwork(5, [5, 4, 4, 4, 2])))
    n -= 1
f.record_collidables(2)
while True:
    f.start_simulation(10)
    best_agents = f.get_best_agents(10)
    f.clear()
    breed_agents = breed(best_agents, 50)
    f._agents = breed_agents

# print(numpy.average(f.get_fitness_vector()))
