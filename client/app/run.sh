#!/bin/bash

echo "Running client script"

log="app-setup.log"
IDKEY="localhost"
appfile="/app/main.py"

srcdir="/videos/"
dstdir="/reports/"
filetypes="*.mp4"

# find all files in /Videos
for file in $(find $srcdir -iname $filetypes -type f)
do
    extension=${file##*.}
    filename=${file##*\/}
    fileNoExt=${filename%.*}
    framedir="${dstdir}videos/${fileNoExt}_frames/"
    reportdir="${dstdir}${fileNoExt}/"

    # make directory for output frames
    echo "Creating frame directory: ${framedir}" >> log
    mkdir -p $framedir
    mkdir -p $reportdir

    # src and destination paths for ffmpeg
    fullsrc="${srcdir}${filename}"
    dstname="${fileNoExt// /_}"
    fulldstname="${framedir}${IDKEY}_${dstname}_%d.jpg"
    echo "Video file: ${fullsrc}" >> log
    echo "Destination pattern: ${fulldstname}" >> log

    # extract frames
    echo "ffmpeg -i ${fullsrc} ${fulldstname}" >> log
    ffmpeg -i $fullsrc $fulldstname

    # call python script here with the path to the input directory
    python $appfile $framedir $reportdir >> log
done

