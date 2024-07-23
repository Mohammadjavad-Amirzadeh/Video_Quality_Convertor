#!/bin/bash

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null
then
    echo "ffmpeg could not be found"
    exit
fi

# Check if input video is provided
if [ -z "$1" ]
then
    echo "No input video provided"
    exit
fi

# Check if output video name is provided
if [ -z "$2" ]
then
    echo "No output video name provided"
    exit
fi

input_video=$1
output_video=$2

# Reduce size of the video
ffmpeg -i $input_video -vf "scale=iw/2:ih/2" $output_video

echo "Video size reduced successfully"
