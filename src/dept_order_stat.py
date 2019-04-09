import os
import csv
import glob
import shutil
import multiprocessing as mp
from collections import defaultdict, Counter
from functools import partial
from fsplit.filesplit import FileSplit


class DeptOrderStat(object):
    '''Base class to implement purchase analytics to generate order reports by
    department.
    '''

    def __init__(self, args):
        self.product_dept_map = defaultdict(str)
        self.order_count_dict = defaultdict(int)
        self.reorder_count_dict = defaultdict(int)
        self.order_file = args.orderfile
        self.product_file = args.productfile
        self.output_file = args.output
        self.product_col = args.productcol
        self.dept_col = args.deptcol
        self.reorder_col = args.reordercol

    def product_dept_relation_mapper(self):
        '''Maps the relationship between product and department.

        :return: Returns True if mapping operation completes successfully
        :rtype: bool
        '''
        # Read CSV data using DictReader
        product_data_reader = csv.DictReader(open(self.product_file,
                                                  encoding="utf8"))
        # Read data sequentially by row
        for row in product_data_reader:
            # Validate input
            if row[self.product_col].isdigit() and  \
                    row[self.dept_col].isdigit():
                # Save product-department mapping in a dictionary
                self.product_dept_map[row[self.product_col]] = \
                    row[self.dept_col]
            else:
                print('Invaid data. Skipping row: {}'.format(row))
        return True

    @staticmethod
    def stat_counter(file, product_dept_map, product_col, reorder_col):
        '''Generate order report by department, containing number of orders and
        number of first orders.

        :param file: Path to CSV file containing order requests data
        :param product_dept_map: Product-Department dictionary
        :param product_col: Name of column containing product id
        :param reorder_col: Name of column containing reorder information
        :type file: str
        :type product_dept_map: dict
        :type product_col: str
        :type reorder_col: str
        :return: Returns True if map generation is successful
        :rtype: bool
        '''
        # Initialize empty dictionaries to store stats
        order_count_dict = defaultdict(int)
        reorder_count_dict = defaultdict(int)
        # Read CSV data using DictReader
        order_data_reader = csv.DictReader(open(file, encoding="utf8"))
        # Read data sequentially by row and update stats
        for row in order_data_reader:
            try:
                dept_id = int(product_dept_map[row[product_col]])
                reorder_count_dict[dept_id] += (int(row[reorder_col]) ^ 1)
                order_count_dict[dept_id] += 1
            except ValueError as e:
                print(e)
                continue

        return [order_count_dict, reorder_count_dict]

    def report_generator(self):
        '''Wrapper function for order report generator. Saves the results into
        two dictionaries - one for order count by department, another for
        reorder count by department. The percentage information is calculated
        from these two dictionaries while saving the report to a CSV file.

        :return: Returns True if splitting is successful
        :rtype: bool
        '''
        [self.order_count_dict, self.reorder_count_dict] = self.stat_counter(
            file=self.order_file, product_dept_map=self.product_dept_map,
            product_col=self.product_col, reorder_col=self.reorder_col)
        return True

    def report_to_csv(self, csvheader=[]):
        '''Save report to a CSV file such that the department id is listed in
        ascending order, when it has non-zero number of orders. It traverse
        through the dictionaries containing order count and reorder count. The
        percentage column is calculated and rounded from these two dictionary
        data.

        :param csvheader: List of names of the header
        :type csvheader: list
        :return: Returns True if report saved successfully
        :rtype: bool
        '''
        with open(self.output_file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(csvheader)  # Write header
            keys = sorted(self.order_count_dict.keys())    # sort department-id
            for key in keys:
                csvwriter.writerow([key, self.order_count_dict[key],
                                    self.reorder_count_dict[key],
                                    "%.2f" % round(self.reorder_count_dict[key]
                                                   / self.order_count_dict[key], 2)])
        return True


class DeptOrderStatMP(DeptOrderStat):
    '''Extends the DeptOrderStat class for parallel processing of input data.
    Assumes that disk has enough free space to store temporary files generated
    by splitting the input file.
    '''

    def __init__(self, args):
        super().__init__(args)
        self.temp_dir = '../input/temp'   # Directory to save temporary files

    @staticmethod
    def input_file_splitter(file, output_dir, n=mp.cpu_count()):
        '''Split a file into parts based on CPU count in the system.

        :param file: Path of the file that needs to be splitted
        :param output_dir: Directory where the splitted files would be saved
        :param n: Number of parts the files would be splitted into
        :type file: str
        :type output_dir: str
        :return: Returns True if splitting is successful
        :rtype: bool
        '''
        # Create temporary directory to store splitted files
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Split file based into n parts, where n = cpu-count
        file_size = os.path.getsize(file)
        fs = FileSplit(file=file, splitsize=(file_size/n)+1024,
                       output_dir=output_dir)
        fs.split(include_header=True)
        return True

    @staticmethod
    def dict_value_addition(dict1, dict2):
        '''Combine two dictionaries by adding values for common keys.

        :param dict1: Python dictionary
        :param dict2: Python dictionary
        :type dict1: dict
        :type dict2: dict
        :return: A combined dictionary
        :rtype: dict
        '''
        return Counter(dict1) + Counter(dict2)

    def report_generator(self):
        '''Wrapper function for order report generator. Uses parallel
        processing to distribute work among different report generator
        processes. Combines the results into a single dictionary for each
        type of data; namely, order count and reorder count.

        :return: Returns True if splitting is successful
        :rtype: bool
        '''
        if self.input_file_splitter(self.order_file, self.temp_dir):
            # Setup multiprocessingusing Pool
            input_files = glob.glob(self.temp_dir + '/*.csv')
            pool = mp.Pool(len(input_files))
            lst = pool.map(partial(super(DeptOrderStatMP, self).stat_counter,
                                   product_dept_map=self.product_dept_map,
                                   product_col=self.product_col,
                                   reorder_col=self.reorder_col), input_files)
            # Consolidate results of all processes
            for order_count, reorder_count in lst:
                self.order_count_dict = self.dict_value_addition(
                    self.order_count_dict, order_count)
                self.reorder_count_dict = self.dict_value_addition(
                    self.reorder_count_dict, reorder_count)
            # Clean up temporary directory
            shutil.rmtree(self.temp_dir)
        return True
