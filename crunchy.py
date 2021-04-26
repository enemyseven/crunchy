#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Crunchy Time
Author: Cody Hill
Date Created: March 10, 2021
Last Modified: April 26, 2021
This Software is released under the MIT License:
http://www.opensource.org/licenses/mit-license.html
See LICENSE at root of project for more details.
(C) 2021 Cody Hill
"""
import time
import os
import subprocess
import glob

VERSION = '0.0.2'

# MARK: Global Variables

# Locations
ffmpeg = "./ffmpeg"
inputPath = "./input/"
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
            'fps=15, crop=ih/3*4:ih, scale=320:240, format=yuv420p, eq=brightness=-0.3:saturation=0.6', # filter chain
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

def getFilenames(directory):
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(".mp4")]
    return filtered_files

def main():
  setup()
  
  # Get files
  filenames = getFilenames(inputPath)
  
  # Note start time
  start = time.time()
  
  # Process files
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
    
  # Output time spent
  end = time.time()
  totalTime = end - start
  print("\n\n--- Complete ---")
  print("Total time: " + str(totalTime))


if __name__ == "__main__":
    # execute only if run as a script
    main()
