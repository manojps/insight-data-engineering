import time
import argparse
from dept_order_stat import DeptOrderStat
from dept_order_stat import DeptOrderStatMP


if __name__ == '__main__':
    # Initialize argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--orderfile', help='order file path',
                        default='./input/order_products.csv')
    parser.add_argument('-p', '--productfile', help='product file path',
                        default='./input/products.csv')
    parser.add_argument('-o', '--output', help='output file path',
                        default='./output/report.csv')
    parser.add_argument('-d', '--deptcol', help='depertment column name',
                        default='department_id')
    parser.add_argument('-c', '--productcol', help='product column name',
                        default='product_id')
    parser.add_argument('-r', '--reordercol', help='reordered column name',
                        default='reordered')
    parser.add_argument('-m', '--mp', help='turn on multiprocessing',
                        action='store_true', default=False)
    args = parser.parse_args()

    start = time.time()     # Start timer
    if args.mp:
        report = DeptOrderStatMP(args)  # Initialize multiprocessing solution
    else:
        report = DeptOrderStat(args)    # Initialize lazy solution class

    # Map product-id and department -id relationships
    report.product_dept_relation_mapper()
    # Generate aggregate report of orders by department
    report.report_generator()
    # Save report in a CSV file
    report.report_to_csv(['department_id', 'number_of_orders',
                          'number_of_first_orders', 'percentage'])
    # Print time taken to generate report
    print('Time taken for processing: {} seconds'.format(time.time()-start))
