# Insight Data Engineering Challenge - June 2019

## Solution
I have implemented the solution using Python dictionaries. The solution can be
run sequentially (`DeptOrderStat` class) or parallelly(`DeptOrderStatMP` class).
Interface for both the classes are same. To run the parallel solution just pass
`--mp` after the script name.

To run the parallel solution use:
`python3 report_generator.py --mp`

To run the sequential solution use:
`python3 report_generator.py`

## Dependencies
My solution uses one external Python module (`filesplit`) for file splitting,
in the parallel solution. It can be installed using:

`python3 -m pip install filesplit`

Apart from this, I have used Python's builtin modules:
`csv, os, glob, shutil, multiprocessing, collections, functools`


 
 
