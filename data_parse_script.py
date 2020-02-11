"""This script takes in the arguments for the path of the users local copy of "Spring 2018 - Product Case Data.xlsx"
which, for the sake of running in a linux terminal, we rename to "spring_2018_product_case_data.csv" and parses out
metrics such as the conversion rate, bounce rate and necessary graphs as described in parts 1-5 of part 1 of the case
"""

# Import necessary libraries
import argparse
import pandas as pd
import numpy as np


def parser_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="path to your copy of spring_2018_product_case_data.csv")
    args = parser.parse_args()
    return args


def main(args):
    path = args.path

    # Read in the dataset and convert to pandas dataframe.
    dataset = pd.read_csv(path, index_col=[0])
    dataset = pd.DataFrame(dataset)

    # Remove the extraneous "Unnamed" columns.
    dataset = dataset.loc[:, ~dataset.columns.str.contains('^Unnamed')]
    print(dataset.head())



if __name__ == "__main__":
    arguments = parser_arguments()
    main(arguments)
