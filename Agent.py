import math
from graphics import *
import AgentAI


class Agent:
    def __init__(self, startingPos, speed_x, speed_y, acceleration_x, acceleration_y, net):
        self._position = startingPos
        self._speed_x = speed_x
        self._speed_y = speed_y
        self._acceleration_x = acceleration_x
        self._acceleration_y = acceleration_y
        self._dead = False
        self._acceleration_vector_line = Line(Point(0, 0), Point(0, 0))
        self._speed_vector_line = Line(Point(0, 0), Point(0, 0))
        self._left_fov = Line(Point(0, 0), Point(0, 0))
        self._center_fov= Line(Point(0, 0), Point(0, 0))
        self._right_fov = Line(Point(0, 0), Point(0, 0))
        self._agent_ai = AgentAI.AgentAI(self, net)

    def draw(self, window):
        bias = 2.5
        x = self._position.x
        y = self._position.y

        m = self._acceleration_y / self._acceleration_x

        tailX = -20 / math.sqrt(1 + m * m) + x
        tailY = m * tailX - m * x + y
        tailPoint = Point(tailX, tailY)

        self._acceleration_vector_line= Line(self._position, tailPoint)

        self._acceleration_vector_line.draw(window)

        m = self._speed_y / self._speed_x

        radius = -bias * math.sqrt(self._speed_x ** 2 + self._speed_y ** 2) if self._speed_x < 0 else bias * math.sqrt(
            self._speed_x ** 2 + self._speed_y ** 2)
        tailX = radius / math.sqrt(1 + m * m) + x
        tailY = m * tailX - m * x + y
        tailPoint = Point(tailX, tailY)

        self._speed_vector_line = Line(self._position, tailPoint)
        self._speed_vector_line.setFill('blue')
        self._speed_vector_line.draw(window)

    def update(self, window, collidables,goal):
        if not self._dead:
            self._acceleration_vector_line.undraw()
            self._speed_vector_line.undraw()
            self._left_fov.undraw()
            self._right_fov.undraw()
            self._center_fov.undraw()
            distances = self.calculate_raycasts(collidables, window)
            self._agent_ai.act(distances, goal)
            self.move(window.width,window.height)
            if check_collisions(self._position.x, self._position.y, collidables):
                self._dead = True
                self.draw(window)
                self._acceleration_vector_line.setFill('red')
                self._speed_vector_line.setFill('red')
            else:
                self.draw(window)

    def get_neural_net(self):
        return self._agent_ai._net

    def undraw(self):
        self._acceleration_vector_line.undraw()
        self._speed_vector_line.undraw()
        self._left_fov.undraw()
        self._right_fov.undraw()
        self._center_fov.undraw()


    def calculate_raycasts(self, collidables, window):
        fovAngle = math.atan(self._speed_y / self._speed_x)

        right_view_gradient = math.tan(fovAngle + math.pi / 8)
        if fovAngle + math.pi / 8 > math.pi / 2:
            right_view_gradient *= -1
        left_view_gradient = math.tan(fovAngle - math.pi / 8)
        if fovAngle - math.pi / 8 < -math.pi / 2:
            left_view_gradient *= -1

        if self._speed_x > 0:
            direct_hit = get_raycast_hit(self._position, self._speed_y / self._speed_x, collidables,0.5)
            left_hit = get_raycast_hit(self._position, left_view_gradient, collidables,0.5)
            right_hit = get_raycast_hit(self._position, right_view_gradient, collidables, 0.5)
        else :
            direct_hit = get_raycast_hit(self._position, self._speed_y / self._speed_x, collidables, -0.5)
            left_hit = get_raycast_hit(self._position, left_view_gradient, collidables, -0.5)
            right_hit = get_raycast_hit(self._position, right_view_gradient, collidables, -0.5)


        return [distance(left_hit, self._position), distance(direct_hit, self._position),
                distance(right_hit, self._position)]

    def move(self, width,height):
        self._speed_x += self._acceleration_x
        self._speed_y += self._acceleration_y
        self._position.x += self._speed_x
        self._position.y += self._speed_y
        if self._position.x > width or self._position.x < 0 :
            self._dead = True
        if self._position.y > height or self._position.y < 0:
                self._dead = True


def distance(p1, p2):
    return math.sqrt(math.pow(p1.x - p2.x, 2) + math.pow(p1.y - p2.y, 2))


def get_raycast_hit(position, gradient, collidables,direction, maxW=700, maxH=700):
    current_point = position.clone()
    while not check_collisions(current_point.x, current_point.y,
                               collidables) and current_point.x < 700 and current_point.y < 700 \
            and current_point.x > 0 and current_point.y > 0:
        current_point.x += direction
        current_point.y += gradient * direction
    return current_point


def check_collisions(x, y, collidables):
    for c in collidables:
        if c[0].x < x < c[1].x and c[0].y < y < c[1].y:
            return True
    return False
