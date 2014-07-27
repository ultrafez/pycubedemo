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
        if self.current_audio:
            amplitude = audioop.rms(self.current_audio, 2)
            print amplitude
            self.history.append(amplitude)
            size = max(0, (amplitude - self.min_amplitude) / float(self.amplitude_diff))
            self.draw(math.floor(size * self.cube.size))

        if len(self.history) > 16:
            # print "updating"
            self.min_amplitude = min(self.history)
            self.amplitude_diff = self.max_amplitude - self.min_amplitude
            self.history = []

    def draw(self, size):
        for coord in cubehelper.line((0, 0, 0), (7, 0, 0)):
            self.cube.set_pixel(coord, (0, 0, 0))

        for coord in cubehelper.line((0, 0, 0), (size, 0, 0)):
            self.cube.set_pixel(coord, (1.0, 1.0, 1.0))
