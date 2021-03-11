#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Crunch Time
Author: Cody Hill
Date Created: March 10, 2021
Last Modified: March 11, 2021
This Software is released under the MIT License:
http://www.opensource.org/licenses/mit-license.html
See LICENSE at root of project for more details.
(C) 2021 Cody Hill
"""
import time
import os
import subprocess
import glob

VERSION = '0.0.1'

# MARK: Global Variables

# Directories
ffmpeg = "./ffmpeg"
inputPath = "./input/"
cachePath = "./cache/"
commonPath = "./common/"
outputPath = "./output/"

# MARK: Functions

def setup():
    # Make sure things are good to go.
    if not os.path.isfile(ffmpeg):
        print("ffmpeg not found.")
        exit()

    # Check to see if directory exists.
    if not os.path.isdir(outputPath):
        # If not create it.
        os.makedirs(outputPath)
        
def makePreview(input, output):
    if not os.path.isfile(output):
        execute = [
            ffmpeg,
            '-i', input, # Input filename
            '-ss', '0:00:03', # Skip ahead to
            '-to', '0:00:13', # copy until
            '-filter:v',
            'fps=15, crop=ih/3*4:ih, scale=320:240, format=yuv420p, eq=brightness=-0.3', # filter chain
            '-an', # Do not extract audio
            f'{output}', # output filename
            '-y' # overwrite output if it exists
        ]
        try:
            subprocess.run(execute, check=True)
        except subprocess.CalledProcessError as e:
            print("Early exit on file ", input , " due to error.")
            exit()
    else:
        print("Warning: ", output, " already exits.")


def main():
    setup()
    
    filenames = []
    
    textfiles = glob.glob("*list.txt")
    
    for textfile in textfiles:
        with open(textfile) as f:
            filenames.extend(f.read().splitlines())
            
    for filename in filenames:
        if filename == "\n":
            print("Encountered newline.")
            break
        
    # Make target input
    input = inputPath + filename

    # Make target output
    pre, ext = os.path.splitext(filename)
    output = outputPath + pre + "-preview.mp4"
    pre, ext = os.path.splitext(input)
    
    makePreview(input, output)


if __name__ == "__main__":
    # execute only if run as a script
    main()
