# Display a spectrum analysis of incoming waveform
# Copyright (C) Alex Silcock <alex@alexsilcock.net>
# Released under the terms of the GNU General Public License version 3

import cubehelper
import pyaudio
import struct
import numpy
import math
import audioop

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
        self.history = []
        self.min_amplitude = 0
        self.max_amplitude = 16000
        self.amplitude_diff = 16000

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
        self.cube.clear()
        if self.current_audio:
            amplitude = audioop.rms(self.current_audio, 2)
            # print amplitude
            self.history.append(amplitude)
            
            self.draw()

        if len(self.history) > 16:
            self.min_amplitude = min(self.history)
            # self.max_amplitude = max(max(self.history)*1.08, self.max_amplitude)
            self.amplitude_diff = self.max_amplitude - self.min_amplitude
            print "updating min " + str(self.min_amplitude) + " max " + str(self.max_amplitude)
            self.history = []

    def draw(self):
        levels = self.calculate_levels(self.current_audio)
        print levels

        color = cubehelper.color_to_float(0xFFFFFF)

        transformed = self.transform_on(levels)
        for y in range(0, self.cube.size):
            for x in range(0, self.cube.size):
                if transformed[x][y] == 1:
                    self.cube.set_pixel((x, 0, y), color)



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

    def transform_on(self, levels):
        matrix = [[0 for x in range(0, len(levels))] for x in range(0, len(levels))]

        for x in range(0, len(levels)):
            for height in range(0, levels[x]):
                matrix[x][self.cube.size-height-1] = 1

        return matrix

    def vu_color(self, amount):
        """Return a VU meter colour from green to red, with amount between 0 and 1"""
        green = cubehelper.color_to_float(0x00FF00)
        yellow = cubehelper.color_to_float(0xFFFF00)
        red = cubehelper.color_to_float(0xFF0000)

        if amount<0.5:
            return cubehelper.mix_color(green, yellow, amount/0.5)
        else:
            return cubehelper.mix_color(yellow, red, min(1.0, (amount-0.5)/0.4))
