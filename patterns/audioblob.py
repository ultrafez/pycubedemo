# Display a blob in the centre of the cube that increases in size proportionally with audio amplitude
# Copyright (C) Alex Silcock <alex@alexsilcock.net>
# Released under the terms of the GNU General Public License version 3

import cubehelper
import pyaudio
import struct
import math
import audioop

FORMAT = pyaudio.paInt24
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1
RATE = 44100
INPUT_BLOCK_TIME = 0.05
# INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
INPUT_FRAMES_PER_BLOCK = 1024

class Pattern(object):
    def init(self):
        self.double_buffer = True
        self.current_audio = None
        self.history = []
        self.min_amplitude = 0
        self.max_amplitude = 17000
        self.amplitude_diff = 17000
        self.tick_counter = 0

        pa = pyaudio.PyAudio()
        self.stream = pa.open(format = FORMAT,
                      channels = CHANNELS,
                      rate = RATE,
                      input = True,
                      frames_per_buffer = INPUT_FRAMES_PER_BLOCK,
                      stream_callback = self.incoming_audio)

        return 0.5 / self.cube.size

    def incoming_audio(self, in_data, frame_count, time_info, status_flags):
        self.current_audio = in_data
        return (None, pyaudio.paContinue)

    def tick(self):
        self.tick_counter += 1
        if self.current_audio:
            amplitude = audioop.rms(self.current_audio, 2)
            # print amplitude
            self.history.append(amplitude)
            size = max(0, (amplitude - self.min_amplitude) / float(self.amplitude_diff))
            self.draw(math.floor(size * self.cube.size))

        if len(self.history) > 16:
            print "updating"
            self.min_amplitude = min(self.history)
            self.amplitude_diff = self.max_amplitude - self.min_amplitude
            self.history = []

    def draw(self, size):
        # print size
        # for coord in cubehelper.line((0, 0, 0), (7, 0, 0)):
            # self.cube.set_pixel(coord, (0, 0, 0))

        # for coord in cubehelper.line((0, 0, 0), (size, 0, 0)):
            # self.cube.set_pixel(coord, (1.0, 1.0, 1.0))

        size = max(1.0, size)
        self.sphere(size)

    def get_pulsing_color(self):
        meld = math.sin(self.tick_counter / 10.0)
        # color1 = (1.0, 0.0, 0.0)
        color1 = cubehelper.color_to_float(0x006AFF)
        color2 = cubehelper.color_to_float(0x003580)
        # color2 = (0.0, 0.0, 1.0)
        return cubehelper.mix_color(color1, color2, (meld / 2.0) + 0.5)

    def get_sphere_radius(self, volume):
        """Get an approximation of the radius of a sphere, given the volume"""
        multiplier = 0.083 # ~1/12
        return (multiplier * volume) ** 0.5

    def sphere(self, size):
        origin = (3.5, 3.5, 3.5)
        black = (0.0, 0.0, 0.0)
        red = (1.0, 0.0, 0.0)

        print size
        # size = 3.0

        # radius = ((0.1 * size) ** 0.4) * 70 # vaguely based on the inverse equation for the volume of a sphere
        radius = self.get_sphere_radius(size)
        upscaled = radius * self.cube.size*0.75
        print upscaled

        pulsing = self.get_pulsing_color() # get a breathing effect
        # as the size of the sphere increases, fade the breathing towards a red colour
        blended = cubehelper.mix_color(pulsing, red, radius)

        for y in range(0, self.cube.size):
            for x in range(0, self.cube.size):
                for z in range(0, self.cube.size):
                    dist = self.distance(origin, (x, y, z))
                    # print (x, y, z), dist, size

                    if dist < upscaled:
                        color = blended
                    else:
                        color = black

                    self.cube.set_pixel((x, y, z), color)


    def distance(self, c1, c2):
        diff = (c1[0] - c2[0], c1[1] - c2[1], c1[2] - c2[2])
        return math.sqrt(diff[0]**2 + diff[1]**2 + diff[2]**2)