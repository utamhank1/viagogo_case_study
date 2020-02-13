"""This script takes in the arguments for the path of the users local copy of "Spring 2018 - Product Case Data.xlsx"
which, for the sake of running in a linux terminal, we rename to "spring_2018_product_case_data.csv" and parses out
metrics such as the conversion rate, bounce rate for each date as well as a summary table of average conversion rate,
bounce rate, and aggregate differences ONLY for users who landed on the viagogo homepage directly.
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
    dataset = pd.read_csv(path)
    dataset = pd.DataFrame(dataset)

    # Remove the extraneous "Unnamed" columns.
    dataset = dataset.loc[:, ~dataset.columns.str.contains('^Unnamed')]

    # Extract all of the "unique dates" in the dataset.
    uniqueDates = dataset['Date'].unique()

    ####################################################################################################################
    ############################################# Secondary Analysis ###################################################
    ####################################################################################################################

    # Create empty dataframe to hold average values for conversion rate, and bounce rate for control and variants in
    # addition to their aggregate differences.
    columns_results = ["Type", "Conversion Rate Avg", "Bounce Rate Avg"]
    zero_data = np.zeros(shape=(3, len(columns_results)))
    results = pd.DataFrame(zero_data, columns=columns_results)
    results['Type'][0] = "Control"
    results['Type'][1] = "Variant"
    results['Type'][2] = "Aggregate Difference"

    # Create empty dataframe to hold, for each date, the total number of users that purchased, the total number of users
    # that bounced, and the total number of users that visited the site for control and variant.
    columns = ["Date", "Users Purchased Control", "Users Purchased Variant", "Users Landed Control",
               "Users Bounced Control", "Users Landed Variant", "Users Bounced Variant", "Users Visited Control",
               "Users Visited Variant", "Conversion Rate Control", "Conversion Rate Variant", "Bounce Rate Control",
               "Bounce Rate Variant"]
    zero_data = np.zeros(shape=(len(uniqueDates), len(columns)))
    primary_results = pd.DataFrame(zero_data, columns=columns)
    print(primary_results.head())

    # Iterate over the dataset and extract required data for each unique cooresponding date.
    for i in range(0, len(uniqueDates)):
        # Set the first row of primary_results equal to the unique date.
        primary_results['Date'][i] = uniqueDates[i]

        # Iterate over the dataset and sum together the desired metrics for each date, control and variant.
        for j in range(0, len(dataset)):
            if dataset['Date'][j] == uniqueDates[i]:
                if dataset['Channel'][j] == 'Direct':
                    if dataset['Land'][j] == 1:
                        primary_results['Users Landed Control'][i] = primary_results['Users Landed Control'][i] \
                                                                     + dataset['Visitors_Control'][j]
                        primary_results['Users Landed Variant'][i] = primary_results['Users Landed Variant'][i] \
                                                                     + dataset['Visitors_Variant'][j]

                    if dataset['Purchase'][j] == 1:
                        primary_results['Users Purchased Control'][i] = primary_results['Users Purchased Control'][i] \
                                                                        + dataset['Visitors_Control'][j]
                        primary_results['Users Purchased Variant'][i] = primary_results['Users Purchased Variant'][i] \
                                                                        + dataset['Visitors_Variant'][j]

                    if dataset['Bounce'][j] == 1:
                        primary_results['Users Bounced Control'][i] = primary_results['Users Bounced Control'][i] \
                                                                      + dataset['Visitors_Control'][j]
                        primary_results['Users Bounced Variant'][i] = primary_results['Users Bounced Variant'][i] \
                                                                      + dataset['Visitors_Variant'][j]
                    primary_results['Users Visited Control'][i] = primary_results['Users Visited Control'][i] \
                                                                  + dataset['Visitors_Control'][j]
                    primary_results['Users Visited Variant'][i] = primary_results['Users Visited Variant'][i] \
                                                                  + dataset['Visitors_Variant'][j]

        # Calculate conversion rates and bounce rates for both control and variant tests.
        primary_results["Conversion Rate Control"][i] = primary_results["Users Purchased Control"][i] / \
                                                        primary_results["Users Visited Control"][i]
        primary_results["Conversion Rate Variant"][i] = primary_results["Users Purchased Variant"][i] / \
                                                        primary_results["Users Visited Variant"][i]
        primary_results["Bounce Rate Control"][i] = primary_results["Users Bounced Control"][i] / \
                                                    primary_results["Users Landed Control"][i]
        primary_results["Bounce Rate Variant"][i] = primary_results["Users Bounced Variant"][i] / \
                                                    primary_results["Users Landed Variant"][i]

    # Save the primary analysis results to .csv file.
    primary_results.to_csv('secondary_results_land_affiliates_only.csv')

    # Fill empty summary results dataframe with average values for conversion rate, bounce rate, and their differences.
    results["Conversion Rate Avg"][0] = primary_results['Conversion Rate Control'].mean()
    results["Conversion Rate Avg"][1] = primary_results['Conversion Rate Variant'].mean()
    results["Bounce Rate Avg"][0] = primary_results['Bounce Rate Control'].mean()
    results["Bounce Rate Avg"][1] = primary_results['Bounce Rate Variant'].mean()

    # Calculate aggregate differences between the conversion and bounce rates of the control and the variant.
    results["Conversion Rate Avg"][2] = results["Conversion Rate Avg"][1] - results["Conversion Rate Avg"][0]
    results["Bounce Rate Avg"][2] = results["Bounce Rate Avg"][1] - results["Bounce Rate Avg"][0]

    # Save summary results to a separate table.
    results.to_csv('secondary_summary_results_land_affiliates_only.csv')


if __name__ == "__main__":
    arguments = parser_arguments()
    main(arguments)
