import cubehelper
# import numpy as np
import random
from collections import deque

class Pattern(object):
    TRAIL_LENGTH = 5

    def init(self):
        # Direction vectors leaving a particular corner vertex
        m = self.cube.size-1
        corner_leave_directions = {}
        corner_leave_directions[(0, 0, 0)] = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        corner_leave_directions[(0, 0, m)] = [(1, 0, 0), (0, 1, 0), (0, 0, -1)]
        corner_leave_directions[(0, m, 0)] = [(1, 0, 0), (0, -1, 0), (0, 0, 1)]
        corner_leave_directions[(0, m, m)] = [(1, 0, 0), (0, -1, 0), (0, 0, -1)]
        corner_leave_directions[(m, 0, 0)] = [(-1, 0, 0), (0, 1, 0), (0, 0, 1)]
        corner_leave_directions[(m, 0, m)] = [(-1, 0, 0), (0, 1, 0), (0, 0, -1)]
        corner_leave_directions[(m, m, 0)] = [(-1, 0, 0), (0, -1, 0), (0, 0, 1)]
        corner_leave_directions[(m, m, m)] = [(-1, 0, 0), (0, -1, 0), (0, 0, -1)]

        self.snakes = []
        self.snakes.append(Snake(self.cube, (1.0, 0.0, 0.0), self.TRAIL_LENGTH, corner_leave_directions))
        self.snakes.append(Snake(self.cube, (0.0, 1.0, 0.0), self.TRAIL_LENGTH, corner_leave_directions))
        self.snakes.append(Snake(self.cube, (0.0, 0.0, 1.0), self.TRAIL_LENGTH, corner_leave_directions))
        self.snakes.append(Snake(self.cube, (1.0, 1.0, 0.0), self.TRAIL_LENGTH, corner_leave_directions))

        return 1.0 / self.cube.size / 2

    def tick(self):
        self.cube.clear()
        for snake in self.snakes:
            snake.draw()
            snake.tick()
        


class Snake(object):
    def __init__(self, cube, color, trail_length, corner_leave_directions):
        self.cube = cube
        self.corner_leave_directions = corner_leave_directions

        self.head = self.corner_leave_directions.keys()[random.randrange(8)]
        self.color = color
        self.trail = deque([], trail_length)
        self.direction = self.new_direction(self.head, [])

    def tick(self):
        self.trail.appendleft(self.head)

        # Add the direction vector to the current location
        self.head = tuple(map(lambda x, y: x + y, self.head, self.direction))

        if self.is_corner(self.head):
            self.direction = self.new_direction(self.head, self.direction)

    def draw(self):
        self.cube.set_pixel(self.head, self.color)

        for coord in self.trail:
            self.cube.set_pixel(coord, self.color)

    def is_corner(self, coord):
        return coord in self.corner_leave_directions

    def new_direction(self, coord, curr_direction):
        potential_directions = self.corner_leave_directions[coord]

        # Prevent returning along the edge we've just travelled
        return_direction = tuple(map(lambda x: -x, curr_direction))

        while True:
            next_dir_index = random.randrange(3)
            if potential_directions[next_dir_index] != return_direction:
                break

        return potential_directions[next_dir_index]
