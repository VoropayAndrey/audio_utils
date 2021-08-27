#!/usr/bin/env python

import sys
import os
import argparse
import numpy as np
import time
from slicer.slicer import Slicer

parser = argparse.ArgumentParser(description="Slicer for Audacity labels, used primary for dataset creation for deep learning.")
parser.add_argument("INPUT_AUDIO_FILE_PATH", type=str, help="Input .wav audio file path.")
parser.add_argument("INPUT_LABEL_FILE_PATH", type=str, help="Input Audacity label .txt file path.")
parser.add_argument("OUTPUT_FOLDER_PATH", type=str, help="Output folder for sliced audio files.")
parser.add_argument("--verbose", default=False, dest="IS_VERBOSE", action="store_true", help="Print debug information.")
parser.add_argument("--slice_size", dest="SLICE_SIZE", default=2, type=int, help="Output slices size in seconds.")
args = parser.parse_args()

isVerbose = args.IS_VERBOSE

print("Input audio file is: " + args.INPUT_AUDIO_FILE_PATH)
print("Input label file is: " + args.INPUT_LABEL_FILE_PATH)

slicer = Slicer(audio_file_path=args.INPUT_AUDIO_FILE_PATH,
                txt_label_file_path=args.INPUT_LABEL_FILE_PATH,
                output_folder_path=args.OUTPUT_FOLDER_PATH,
                output_file_length_seconds=args.SLICE_SIZE)

slicer.export_all()

print("Slicing is done!")