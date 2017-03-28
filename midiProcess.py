
from sys import exit
import argparse
import pickle
import midi
import math
import sys
import os
import copy


def getFilesFromDir(path):
    ''' returns all files ending with any of the extensions in <suffices>'''
    return [name for name in os.listdir(path) if name.upper().endswith(".MID")]


def GetRangeOfEvents(pattern):
    ''' Returns the range of the notes from a pattern '''
    Inf = 1000000
    minmax = [Inf, -Inf]

    for track_idx in range(len(pattern)):
        for event_idx in range(len(pattern[track_idx])):
            event1 = pattern[track_idx][event_idx]
            if len(event1.data) == 2:  # note event
                tmp = event1.data[0]
                if tmp < minmax[0]:  # min
                    minmax[0] = tmp
                if tmp > minmax[1]:  # max
                    minmax[1] = tmp
    return minmax


def ConvertEvents(pattern, fun):
    ''' Convert events in pattern using function fun '''
    err = 0

    for track_idx in range(len(pattern)):
        for event_idx in range(len(pattern[track_idx])):
            event1 = pattern[track_idx][event_idx]
            if len(event1.data) == 2:  # note event
                event1.data[0] = fun(event1.data[0])
                if err < 5 and (event1.data[0] > 255 or event1.data[0] < 0):
                    print "WARNING: value out of bounds: {}".format(event1.data)


def invertFunc(x):
    # return 120-x
    return 25 + abs(100 - x)


def InvertMidi(pattern):
    ConvertEvents(pattern, invertFunc)


def main():
    parser = argparse.ArgumentParser(
        description='Wallpaper revolver arguments.')

    parser.add_argument("-p", "--path",
                        help="path to midi files [REQUIRED]", type=str,
                        default='.', required=True)

    parser.add_argument("-i", "--invert",
                        help="invert midi files",
                        action='store_true', required=False)

    args = vars(parser.parse_args())
    path = args['path']
    invert = args['invert']

    if not invert:
        exit(0)

    files = getFilesFromDir(path)

    print "reading path", path

    for file in files:
        filename = path + "/" + file
        fname, ext = os.path.splitext(file)
        outfname = fname + "_out" + ext
        outFilename = path + os.sep + outfname
        print "Processing... \t{} ==> {}".format(file, outfname)
        sys.stdout.flush()

        pattern = midi.read_midifile(filename)

        if invert:
            InvertMidi(pattern)
        try:
            midi.write_midifile(outFilename, pattern)
        except:
            print " an error occured attempting to save midi, skipping..."
            pass

if __name__ == '__main__':
    main()
