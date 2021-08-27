#!/usr/bin/env python

# P - prolongation
# R - repetition
# B - block
# N - normal

import sys
import os
import argparse
import numpy as np
import time
from slicer.slicer import Slicer

parser = argparse.ArgumentParser(description="Slicer for Audacity labels, used primary for dataset creation for deep learning.")
parser.add_argument("SEARCH_PATH", type=str, help="Input search path for labels and related audio files")
parser.add_argument("OUTPUT_FOLDER_PATH", type=str, help="Output folder for sliced audio files.")
parser.add_argument("--verbose", default=False, dest="IS_VERBOSE", action="store_true", help="Print debug information.")
parser.add_argument("--slice_size", dest="SLICE_SIZE", default=2, type=int, help="Output slices size in seconds.")
args = parser.parse_args()

isVerbose = args.IS_VERBOSE

SEARCH_FILE_ENDING = "Labels.txt"

print("Search path is: " + args.SEARCH_PATH)
print("Output folder is: " + args.OUTPUT_FOLDER_PATH)

if not os.path.isdir(args.OUTPUT_FOLDER_PATH):
    print("Output folder created")
    os.mkdir(args.OUTPUT_FOLDER_PATH)

found_labeled_files_list = list()
found_folders_list = list()

def add_folder_to_list(parent_folder):
    if os.path.isdir(parent_folder):
        files = os.listdir(parent_folder)
        for file in files:
            file_path = parent_folder + "/" + file
            if os.path.isdir(file_path):
                found_folders_list.append(file_path)
                add_folder_to_list(file_path)

def add_labels_to_list(folder):
    if os.path.isdir(folder):
        files = os.listdir(folder)
        for file in files:
            file_path = folder + "/" + file
            if os.path.isfile(file_path):
                if file_path.find(SEARCH_FILE_ENDING) > 0:
                    audio_file_path = file_path.replace(SEARCH_FILE_ENDING, ".wav")
                    if os.path.isfile(audio_file_path):
                        found_labeled_files_list.append([file_path, audio_file_path])
                    else:
                        print("Can't find any related audio file to: " + file_path)

add_folder_to_list(args.SEARCH_PATH)
for folder in found_folders_list:
    add_labels_to_list(folder)

#print("Folders: "found_folders_list)


for labeled_files in found_labeled_files_list:

    label_file_path = labeled_files[0]
    audio_file_path = labeled_files[1]

    file_name_index = audio_file_path.rfind('/')
    folder_name_end_index = audio_file_path[0:file_name_index].rfind('/')
    #folder_name_end_index = audio_file_path[0:folder_name_end_index].rfind('/')
    folder_name_start_index = audio_file_path[0:folder_name_end_index].rfind('/')
    files_names = audio_file_path[file_name_index + 1:len(audio_file_path) - 4]

    folder_name = audio_file_path[folder_name_start_index + 1:folder_name_end_index]
    folder_name = folder_name[-6:]

    files_prefix = files_names + "_" + folder_name + "_"

    slicer = Slicer(audio_file_path=audio_file_path,
                    txt_label_file_path=label_file_path,
                    output_folder_path=args.OUTPUT_FOLDER_PATH + "/prolongation",
                    output_file_length_seconds=args.SLICE_SIZE,
                    output_file_prefix=files_prefix,
                    label_value_filer={"P"})
    slicer.export_all()

    slicer = Slicer(audio_file_path=audio_file_path,
                    txt_label_file_path=label_file_path,
                    output_folder_path=args.OUTPUT_FOLDER_PATH + "/repetition",
                    output_file_length_seconds=args.SLICE_SIZE,
                    output_file_prefix=files_prefix,
                    label_value_filer={"R"})
    slicer.export_all()

    slicer = Slicer(audio_file_path=audio_file_path,
                    txt_label_file_path=label_file_path,
                    output_folder_path=args.OUTPUT_FOLDER_PATH + "/block",
                    output_file_length_seconds=args.SLICE_SIZE,
                    output_file_prefix=files_prefix,
                    label_value_filer={"B"})
    slicer.export_all()

    slicer = Slicer(audio_file_path=audio_file_path,
                    txt_label_file_path=label_file_path,
                    output_folder_path=args.OUTPUT_FOLDER_PATH + "/normal",
                    output_file_length_seconds=args.SLICE_SIZE,
                    output_file_prefix=files_prefix,
                    label_value_filer={"N"})
    slicer.export_all()

print("Searching and slicing is done!")