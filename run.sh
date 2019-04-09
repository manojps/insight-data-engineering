#!/bin/bash
#
# Use this shell script to compile (if necessary) your code and then execute it. Below is an example of what might be found in this file if your program was written in Python
#
# Install filesplit module
python3 -m pip install filesplit

# Run script with parallel processing
python3 ./src/report_generator.py --mp

# Run script without parallel processing
# python3 ./src/report_generator.py
