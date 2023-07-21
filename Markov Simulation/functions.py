"""
The following functions are meant to be used within the supermarket project
"""

from datetime import timedelta
import pandas as pd
import numpy as np

##################### Create unique Ids and combine files ######################

def unique_customers_and_combine_files(path='./'):
    """
    Reads in the CSV files for customer behavior from monday to friday and
    concatenates them into a single DataFrame with rolling customer numbering.
    Returns the concatenated DataFrame.
    """
    # Read in the five CSV files
    df_monday = pd.read_csv(f"{path}monday.csv", sep=';', parse_dates=True,
                            index_col=0, skipinitialspace=True)
    df_tuesday = pd.read_csv(f"{path}tuesday.csv", sep=';', parse_dates=True,
                            index_col=0, skipinitialspace=True)
    df_wednesday = pd.read_csv(f"{path}wednesday.csv", sep=';', parse_dates=True,
                            index_col=0, skipinitialspace=True)
    df_thursday = pd.read_csv(f"{path}thursday.csv", sep=';', parse_dates=True,
                            index_col=0, skipinitialspace=True)
    df_friday = pd.read_csv(f"{path}friday.csv", sep=';', parse_dates=True,
                            index_col=0, skipinitialspace=True)

    # Perform rolling customer numbering
    last_customer_number = 0
    for data in [df_monday, df_tuesday, df_wednesday, df_thursday, df_friday]:
        data["customer_no"] += last_customer_number
        last_customer_number = data["customer_no"].max()

    # Concatenate the DataFrames
    all_data = pd.concat([df_monday, df_tuesday, df_wednesday, df_thursday, df_friday])

    # Return the concatenated DataFrame
    return all_data.reset_index(names = 'timestamp')



##################### Create Minute based observations ####################

def to_minute(df):
    """Function to resample customer data to minute steps, forward interpolating the
    location value."""
    grouper = df.set_index('timestamp').groupby('customer_no').resample('min')['location'].ffill()
    resampled_df = grouper.reset_index('timestamp')
    # resampled_df = pd.to_datetime(resampled_df['timestamp'])
    return resampled_df.reset_index()


##################### Add entrance location to minute-1 timestamp ####################
def add_entrance(df):
    """This fuction takes a dataframe, identifies the first position for each customer
    id and returns a dataframe with the entrance location one minute before the first
    recorded observation.
    Args:
        df (pd.Dataframe): A dataframe of customer data within the re-netto supermarket.
        Expected columns: customer_no, timestamp, location
    Returns:
        pd.Dataframe: The same dataframe with entrance location rows included for each id."""

    # group by original dataframe by customer id
    grouped = df.groupby('customer_no')
    # initialize new DataFrame to hold results
    entrance_df = pd.DataFrame()
    # iterate over each customer id group
    for name, group in grouped:
        # sort the group by timestamp
        group = group.sort_values('timestamp')
        # get the first timestamp for this customer id
        first_timestamp = group.iloc[0]['timestamp']
        # subtract one minute from the first timestamp
        new_timestamp = first_timestamp - timedelta(minutes=1)
        # create a new row with the adjusted timestamp and add entrance to the location
        new_row = pd.DataFrame({'customer_no': name, 'timestamp': new_timestamp,
                                'location':'entrance'}, index=[0])
        # append the new row to the new DataFrame. Using ignore index to not use them
        # in the concatenation axis.
        entrance_df = pd.concat([entrance_df, new_row, group], ignore_index=True)
    return entrance_df

#################### Create missing checkouts for late customers ########################

def do_checkout(df):
    """This fuction takes a dataframe,
    identifies the customer_no which did not check out yet
    and returns a dataframe with the missing checkout-observations
    one minute after the last recorded observation.
    Args:
        df (pd.Dataframe): A dataframe of customer data within the re-netto supermarket.
        Expected columns: customer_no, timestamp, location
    Returns:
        pd.Dataframe: The same dataframe with appended lines of checkouts.
    """

    df_temp = df.copy()
    id_gone = list(df_temp[df_temp['location'] == 'checkout']['customer_no'])
    id_still_there = []
    for customer in df_temp['customer_no'].unique():
        if customer not in id_gone:
            id_still_there.append(customer)
    df_return = df_temp.copy()
    for customer in id_still_there:
        last_row = df_temp.tail(1).copy()
        last_row['customer_no'] = customer
        last_row['location'] = 'checkout'
        last_row['timestamp'] = last_row['timestamp'] + timedelta(minutes=1)
        df_return = pd.concat([df_return,last_row],ignore_index=True)
    return df_return

#################### Create the shift(-1) for crosstab Probabilities ########################

def create_next_location(df):
    """This function generates a shift(-1) column for a given dataframe
    based on locations of the supermarket.
    Args:
        df (pd.Dataframe): Dataframe with timestamp data of re-netto
    Returns:
        pd.Dataframe: returns the same dataframe with an added column for next locations.
    """
    df_test = df.copy()
    df_test.reset_index(inplace = True)
    df_test.sort_values('timestamp',inplace=True)
    df_test['next_location'] = df_test.groupby('customer_no')['location'].shift(-1)
    df_test['next_location'].replace(to_replace = np.nan, value='checkout',inplace=True)
    df_test.sort_values('timestamp',inplace=True)
    return df_test
