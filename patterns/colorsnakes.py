import cubehelper
# import numpy as np
import random
from collections import deque

class Pattern(object):
    TRAIL_LENGTH = 5

    def init(self):
        # self.snake = Snake()
        self.head = (0, 0, 0)
        self.trail = deque([], self.TRAIL_LENGTH)
        self.direction = (1, 0, 0)
        self.color = (1.0, 0.0, 0.0)
        self.max = self.cube.size-1

        # Direction vectors leaving a particular corner vertex
        m = self.max
        self.corner_leave_directions = {}
        self.corner_leave_directions[(0, 0, 0)] = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        self.corner_leave_directions[(0, 0, m)] = [(1, 0, 0), (0, 1, 0), (0, 0, -1)]
        self.corner_leave_directions[(0, m, 0)] = [(1, 0, 0), (0, -1, 0), (0, 0, 1)]
        self.corner_leave_directions[(0, m, m)] = [(1, 0, 0), (0, -1, 0), (0, 0, -1)]
        self.corner_leave_directions[(m, 0, 0)] = [(-1, 0, 0), (0, 1, 0), (0, 0, 1)]
        self.corner_leave_directions[(m, 0, m)] = [(-1, 0, 0), (0, 1, 0), (0, 0, -1)]
        self.corner_leave_directions[(m, m, 0)] = [(-1, 0, 0), (0, -1, 0), (0, 0, 1)]
        self.corner_leave_directions[(m, m, m)] = [(-1, 0, 0), (0, -1, 0), (0, 0, -1)]

        return 1.0 / self.cube.size / 2

    def tick(self):
        self.draw()

        self.trail.appendleft(self.head)

        # Add the direction vector to the current location
        self.head = tuple(map(lambda x, y: x + y, self.head, self.direction))

        if self.is_corner(self.head):
            self.direction = self.new_direction(self.head, self.direction)


    def draw(self):
        self.cube.clear()
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
