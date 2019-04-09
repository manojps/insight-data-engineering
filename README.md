# Insight Data Engineering Challenge

## Solution
I have implemented the solution using Python dictionaries. The solution can be run sequentially (`DeptOrderStat` class) or parallelly(`DeptOrderStatMP` class). The sequential solution reads the input files row by row. Hence, has very limited space complexity, but a very high time complexity. The parallel solution extends the sequential solution. The assumption behind this solution is that the machine has enough free space to store some temporary files (equals the size of the input files). The parallel solution splits the order request file into separate files, process each file using a separate process, and then consolidates the results.

Interface for both the classes are same. To run the parallel solution just pass `--mp` after the script name.

To run the parallel solution use:
`python3 report_generator.py --mp`

To run the sequential solution use:
`python3 report_generator.py`

## Dependencies
My solution uses one external Python module (`filesplit`) for file splitting, in the parallel solution. It can be installed using:

`python3 -m pip install filesplit`

Apart from this, I have used Python's builtin modules:
`csv, os, glob, shutil, multiprocessing, collections, functools`


 
 
