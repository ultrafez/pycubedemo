import cubehelper
# import numpy as np
import random

class Pattern(object):
    def init(self):
        # self.snake = Snake()
        self.head = (0, 0, 0)
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
        self.cube.clear()
        
        # Add the direction vector to the current location
        self.head = tuple(map(lambda x, y: x + y, self.head, self.direction))

        if self.is_corner(self.head):
            self.direction = self.new_direction(self.head, self.direction)

        self.cube.set_pixel(self.head, self.color)

    def is_corner(self, coord):
        return coord in self.corner_leave_directions

    def new_direction(self, coord, curr_direction):
        potential_directions = self.corner_leave_directions[coord]
        next_dir_index = random.randrange(3)

        return potential_directions[next_dir_index]
