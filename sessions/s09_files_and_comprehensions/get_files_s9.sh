#!/bin/bash
#
# Downloads data files from Github repo to local folder on Google Colab
#
# This file is a Linux shell script. All of the following lines could
# be executed at a Linux Bash command line (Bash is a type of command
# line).

# Create a variable with a URL to the session 9 folder in the Github repo
base_url="https://raw.githubusercontent.com/irs1318dev/pyclass_frc/master"
base_url="${base_url}/sessions/s09_files_and_comprehensions"

# wget is a Linux command line program that downloads a file from a URL
wget -nv $base_url/hopper.txt
mkdir misc_files
cd misc_files
base_url="${base_url}/misc_files"
wget -nv $base_url/TTY33ASR.jpg
wget -nv $base_url/YaleNews_hopper-grace.UNIVAC.102635875-CC_0.jpg
wget -nv $base_url/cwd
wget -nv $base_url/districts.json
wget -nv $base_url/matches.json
wget -nv $base_url/temp.json
cd ..
echo File Downloads Complete!