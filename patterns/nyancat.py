# Nyan Cat scrolling around the edges of the cube
# Copyright (C) Alex Silcock <alex@alexsilcock.net>
# Released under the terms of the GNU General Public License version 3

import cubehelper

class Pattern(object):
    def init(self):
        self.double_buffer = True
        self.buffer_width = (self.cube.size-1) * 4
        self.edges = list(self.edge_generator())
        self.buffer_offset = 0

        return 0.1

    def edge_generator(self):
        for x in range(self.cube.size-1):
            yield (x, 0)

        for y in range(self.cube.size-1):
            yield (self.cube.size-1, y)

        for x in range(self.cube.size-1, 0, -1):
            yield (x, self.cube.size-1)

        for y in range(self.cube.size-1, 0, -1):
            yield (0, y)

    def trail_generator(self):
        colors = [
            0xFF0000,
            0xFF5A00,
            0xFFDC00,
            0x00FF00,
            0x00FFFF,
            0xAA00FF
        ]
        while True:
            for i in range(3):
                yield [0] + colors + [0]

            for i in range(3):
                yield colors + [0, 0]

    def tick(self):
        self.cube.clear()
        self.buffer_offset += 1
        self.trail = self.trail_generator()

        # make the trail stationary on the edges of the cube
        for q in range(self.buffer_offset % 6):
            next(self.trail)

        for i in range(12):
            edge_index = (i + self.buffer_offset) % len(self.edges)
            self.render_column(self.edges[edge_index], next(self.trail))
            print i

    def render_column(self, position, pixel_column):
        x, y = position
        for i, color in enumerate(pixel_column):
            z = self.cube.size-1-i
            self.cube.set_pixel((x, y, z), color)
