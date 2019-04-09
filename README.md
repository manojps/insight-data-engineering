# Insight Data Engineering Challenge

## Solution
I have tried to solve the problem using two different approaches. The first approach uses a single threaded process, and is memory efficient, but takes a long time to finish. The second approach uses multiple processes running in parallel, and is time efficient, but assumes that the system has enough free space in secondary storage. Both of the approaches reads the data in row by row to make sure the solution scales for large data, and use Python dictionaries as the underlying data structure to store relationship maps and resulting statistics for fast access. The first approach is implemented in the `DeptOrderStat` class. The second  approach is implemneted in the `DeptOrderStatMP` class, which extends the `DeptOrderStat` class. 

The assumption behind the parallel solution is that the machine has enough free space to store some temporary files (equals the size of the input files). The parallel solution splits the order request file into separate files, process each file using a separate process, and then consolidates the results. For large input files, this reduces the time required to generate the report by a linear factor of m, where m is the number of cpus in the system.

Interface for both the classes are same. To run the parallel solution just pass `--mp` after the script name.

To run the parallel solution use:
`python3 report_generator.py --mp`

To run the sequential solution use:
`python3 report_generator.py`

To pass product file, order request file, and output file manually use the following format:
`python3 report_generator --orderfile <order_file_path> --productfile <product_file_path> --output <output_file_path>`

To pass the name of the columns in CSV file identifying the product-id, department-id and reorder information use:
`python3 report_generator --productcol <column_name> --deptcol <column_name> --reordercol <column_name>`

## Dependencies
My solution uses one external Python module (`filesplit`) for file splitting, in the parallel solution. It can be installed using:

`python3 -m pip install filesplit`

Apart from this, I have used Python's builtin modules:
`csv, os, glob, shutil, multiprocessing, collections, functools`




