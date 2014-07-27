# Display a blob in the centre of the cube that increases in size proportionally with audio amplitude
# Copyright (C) Alex Silcock <alex@alexsilcock.net>
# Released under the terms of the GNU General Public License version 3

import cubehelper
import pyaudio
import struct
import math

FORMAT = pyaudio.paInt24
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 44100  
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

class Pattern(object):
    def init(self):
        self.double_buffer = True

        pa = pyaudio.PyAudio()
        self.stream = pa.open(format = FORMAT,
                      channels = CHANNELS,
                      rate = RATE,
                      input = True,
                      frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return 1.0 / self.cube.size

    def tick(self):
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Error recording in audioblob"
            raise StopIteration

        amplitude = self.get_rms(block)
        print amplitude
        return

        if amplitude > tap_threshold: # if its to loud...
            quietcount = 0
            noisycount += 1
            if noisycount > OVERSENSITIVE:
                tap_threshold *= 1.1 # turn down the sensitivity

        else: # if its to quiet...

            if 1 <= noisycount <= MAX_TAP_BLOCKS:
                print 'tap!'
            noisycount = 0
            quietcount += 1
            if quietcount > UNDERSENSITIVE:
                tap_threshold *= 0.9 # turn up the sensitivity

    def get_rms(self, block):
        # Ripped from StackOverflow http://stackoverflow.com/a/10669054/172666

        # RMS amplitude is defined as the square root of the 
        # mean over time of the square of the amplitude.
        # so we need to convert this string of bytes into 
        # a string of 16-bit samples...

        # we will get one short out for each 
        # two chars in the string.
        count = len(block) / 2
        format = "%dh" % (count)
        shorts = struct.unpack(format, block)

        # iterate over the block.
        sum_squares = 0.0
        for sample in shorts:
            # sample is a signed short in +/- 32768. 
            # normalize it to 1.0
            n = sample * SHORT_NORMALIZE
            sum_squares += n*n

        return math.sqrt(sum_squares / count)
