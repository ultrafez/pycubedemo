import cubehelper
# import numpy as np
import random
from collections import deque, defaultdict
from operator import add

class Pattern(object):
    TRAIL_LENGTH = 7

    def init(self):
        # Direction vectors leaving a particular corner vertex
        m = self.cube.size-1
        self.corner_leave_directions = {}
        self.corner_leave_directions[(0, 0, 0)] = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        self.corner_leave_directions[(0, 0, m)] = [(1, 0, 0), (0, 1, 0), (0, 0, -1)]
        self.corner_leave_directions[(0, m, 0)] = [(1, 0, 0), (0, -1, 0), (0, 0, 1)]
        self.corner_leave_directions[(0, m, m)] = [(1, 0, 0), (0, -1, 0), (0, 0, -1)]
        self.corner_leave_directions[(m, 0, 0)] = [(-1, 0, 0), (0, 1, 0), (0, 0, 1)]
        self.corner_leave_directions[(m, 0, m)] = [(-1, 0, 0), (0, 1, 0), (0, 0, -1)]
        self.corner_leave_directions[(m, m, 0)] = [(-1, 0, 0), (0, -1, 0), (0, 0, 1)]
        self.corner_leave_directions[(m, m, m)] = [(-1, 0, 0), (0, -1, 0), (0, 0, -1)]

        self.ticks = 0

        self.snakes = []
        self.snakes.append(Snake(self.cube, [1.0, 0.0, 0.0], self.TRAIL_LENGTH, self.corner_leave_directions))

        return 1.0 / self.cube.size / 3

    def tick(self):
        self.ticks += 1
        if self.ticks == 11:
            self.snakes.append(Snake(self.cube, [0.0, 1.0, 0.0], self.TRAIL_LENGTH, self.corner_leave_directions))

        if self.ticks == 23:
            self.snakes.append(Snake(self.cube, [0.0, 0.0, 1.0], self.TRAIL_LENGTH, self.corner_leave_directions))

        if self.ticks == 36:
            self.snakes.append(Snake(self.cube, [1.0, 0.0, 0.0], self.TRAIL_LENGTH, self.corner_leave_directions))

        if self.ticks == 50:
            self.snakes.append(Snake(self.cube, [0.0, 1.0, 0.0], self.TRAIL_LENGTH, self.corner_leave_directions))

        if self.ticks == 56:
            self.snakes.append(Snake(self.cube, [0.0, 0.0, 1.0], self.TRAIL_LENGTH, self.corner_leave_directions))
            
        # if self.ticks == 38:
        #     self.snakes.append(Snake(self.cube, [1.0, 1.0, 0.0], self.TRAIL_LENGTH, self.corner_leave_directions))

        self.draw()

    def draw(self):
        self.cube.clear()

        def get_black():
            return [0, 0, 0]

        pixels_to_change = defaultdict(get_black)

        for snake in self.snakes:
            snake.draw(pixels_to_change)
            snake.tick()

        for k, v in pixels_to_change.items():
            self.cube.set_pixel(k, map(min, v, [1.0, 1.0, 1.0])) # ensure the color doesn't exceed white


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

    def draw(self, pixels_to_change):
        pixels_to_change[self.head] = map(add, self.color, pixels_to_change[self.head])

        for coord in self.trail:
            pixels_to_change[coord] = map(add, self.color, pixels_to_change[coord])

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
