# Display a spectrum analysis of incoming waveform
# Copyright (C) Alex Silcock <alex@alexsilcock.net>
# Released under the terms of the GNU General Public License version 3

import cubehelper
import pyaudio
import struct
import numpy
import math
import audioop
import collections

FORMAT = pyaudio.paFloat32
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1
RATE = 44100
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = 512

class Pattern(object):
    def init(self):
        self.double_buffer = True
        self.current_audio = None
        self.sample_history = []
        self.plane_history = collections.deque() # previous spectrum planes displayed
        self.min_amplitude = 0
        self.max_amplitude = 16000
        self.amplitude_diff = 16000
        self.black = (0.0, 0.0, 0.0)

        if self.cube.size != 8:
            print "This pattern is unlikely to work properly (if at all) on cubes that aren't 8x8x8"

        pa = pyaudio.PyAudio()
        self.stream = pa.open(format = FORMAT,
                      channels = CHANNELS,
                      rate = RATE,
                      input = True,
                      frames_per_buffer = INPUT_FRAMES_PER_BLOCK,
                      stream_callback = self.incoming_audio)

        return 0.2 / self.cube.size

    def incoming_audio(self, in_data, frame_count, time_info, status_flags):
        self.current_audio = in_data
        return (None, pyaudio.paContinue)

    def tick(self):
        # self.cube.clear()
        if self.current_audio:
            amplitude = audioop.rms(self.current_audio, 2)
            # print amplitude
            self.sample_history.append(amplitude)
            
            self.draw()

        if len(self.sample_history) > 16:
            self.min_amplitude = min(self.sample_history)
            # self.max_amplitude = max(max(self.sample_history)*1.08, self.max_amplitude)
            self.amplitude_diff = self.max_amplitude - self.min_amplitude
            print "updating min " + str(self.min_amplitude) + " max " + str(self.max_amplitude)
            self.sample_history = []

    def draw(self):
        levels = self.calculate_levels(self.current_audio)
        levels_plane = self.levels_to_plane(levels)
        self.plane_history.appendleft(levels_plane)

        if len(self.plane_history) > 8:
            self.plane_history.pop()

        for index, plane in enumerate(self.plane_history):
            self.draw_plane(plane, index)

    def calculate_levels(self, data):
        fft_block_size = INPUT_FRAMES_PER_BLOCK/16
        data = numpy.fromstring(data, 'Float32')
        print data
        data = numpy.reshape(data, (fft_block_size, 16))
        data = numpy.average(data, axis=1)
        print data
        
        # return
        # print data
        # return
        # Convert raw data to numpy array
        # data = struct.unpack("%dh"%(len(data)/2),data)
        # data = numpy.array(data, dtype='h')
        # print data
        # Apply FFT - real data so rfft used
        # print len(data)
        fourier=numpy.fft.rfft(data)
        # print fourier
        # Remove last element in array to make it the same size as chunk
        fourier=numpy.delete(fourier,len(fourier)-1)
        # print fourier
        # Find amplitude
        # power = numpy.log10(numpy.abs(fourier))**2
        power = numpy.abs(fourier)
        # print power
        # print len(power)
        # Araange array into 8 rows for the 8 bars on LED matrix
        power = numpy.reshape(power, (8, fft_block_size/16))
        matrix = numpy.int_(numpy.average(power, axis=1)*float(self.cube.size))

        matrix = [min(x, 8) for x in matrix]
        return matrix

    def levels_to_plane(self, levels):
        matrix = [[0 for x in range(0, len(levels))] for x in range(0, len(levels))]

        for x in range(0, len(levels)):
            for height in range(0, levels[x]):
                matrix[x][height] = 1

        return matrix

    def draw_plane(self, plane, distance):
        """Draw the contents of the specified plane in the XZ axis, <distance> pixels from the front of the cube"""
        for x in range(0, len(plane)):
            for z in range(0, len(plane[x])):
                if plane[x][z] == 1:
                    self.cube.set_pixel((x, distance, z), self.vu_color(z, distance))
                else:
                    self.cube.set_pixel((x, distance, z), self.black)

    def vu_color(self, value, distance):
        """Return a green/yellow/red VU meter colour based on the value (between 0 and 7 inclusive). Higher distances fade the colour out"""
        if value <= 3:
            base_color = (0.0, 1.0, 0.0)
        elif value <= 5:
            base_color = (1.0, 1.0, 0.0)
        else:
            base_color = (1.0, 0.0, 0.0)

        if distance == 0:
            return base_color
        else:
            return cubehelper.mix_color(base_color, self.black, (distance/10.0)+0.2)