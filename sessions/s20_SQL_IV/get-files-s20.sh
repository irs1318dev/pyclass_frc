#!/bin/bash
#
# Downloads data files from Github repo to local folder on Google Colab
#
# This file is a Linux shell script. All of the following lines could
# be executed at a Linux Bash command line (Bash is a type of command
# line).

# Create a variable with a URL to the session 19 folder in the Github repo
base_url="https://raw.githubusercontent.com/irs1318dev/pyclass_frc/master"
base_url="${base_url}/sessions/s20_SQL_IV"

# wget is a Linux command line program that downloads a file from a URL
wget -nv $base_url/chinook.sqlite3
mkdir images
cd images
wget -nv $base_url/images/window-query.png
cd ..
mkdir SQL15Days
wget -nv $base_url/SQL15Days/GenSQLData15Days.ipynb
wget -nv $base_url/SQL15Days/SQL15Days.ipynb
wget -nv $base_url/SQL15Days/sql15days.sqlite3
wget -nv $base_url/SQL15Days/us-names.txt
cd ..
echo File Downloads Complete!.
