# Input from the user
import pandas as pd
from pandas import Timestamp
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import matplotlib
from matplotlib.colors import LinearSegmentedColormap
from pandas_datareader.data import DataReader
import json


sns.set_style("whitegrid")
plt.style.use("fivethirtyeight")

warnings.filterwarnings("ignore")


from pandas import read_csv, to_datetime, Timestamp

def coin_data(coins, date_start, date_end):
    coin_dataframes = {}
    date_start = Timestamp(date_start)
    date_end = Timestamp(date_end)
    days = (date_end - date_start).days

    # Determine the window size based on the date range
    if days <= 29:
        window_size = 2
    elif days > 29 and days <= 180:  # Corrected logical operator and added parentheses
        window_size = 7
    else:
        window_size = 30

    for coin in coins:
        file_path = f"{coin}.csv"

        try:
            df = read_csv(file_path).iloc[:, 3:]
            print(f"Loaded data for {coin}")
            
            df.sort_values(by="Date", inplace=True)
            df["Date"] = to_datetime(df["Date"])
            
            df["Daily_Return"] = df["Close"].pct_change() * 100
            
            # Calculate rolling volatility
            df["Volatility"] = df["Daily_Return"].rolling(window=window_size).std()
            
            coin_dataframes[coin] = df

        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred while reading {file_path}: {e}")

    return coin_dataframes



def create_JSON(coin_names, coin_dataframes, date_start, date_end):
    vol_dfs = {}  # Dictionary to store the volatility DataFrames

    for coin_name in coin_names:
        # Selecting the DataFrame for the coin
        coin_df = coin_dataframes[
            coin_name
        ].copy()  # Create a copy to avoid changing the original DataFrame

        date_start = Timestamp(date_start)
        date_end = Timestamp(date_end)

        # Create a new DataFrame containing only 'Date' and 'Rolling_Volatility'
        vol_df = coin_df[["Date", "Volatility", "Open", "Close", "Volume", "Marketcap"]].loc[(coin_df['Date'] >= date_start) & (coin_df['Date'] < date_end)]

        # Remove NaN values that resulted from the rolling window calculation
        vol_df.dropna(inplace=True)

        # Store this DataFrame in the dictionary with the coin's name as the key
        vol_dfs[coin_name] = vol_df

    json_data = {
        name: df.to_json(orient="index", date_format="iso")
        for name, df in vol_dfs.items()
    }

    # Write the JSON data to a file
    with open("volatility_data.json", "w") as outfile:
        json.dump(json_data, outfile)

    return vol_dfs  # Return the dictionary of DataFrames


def correlation(coin_names, coin_dataframes, date_start, date_end):
    vol_dfs = {}  # Dictionary to store the volatility DataFrames

    for coin_name in coin_names:
        # Selecting the DataFrame for the coin
        coin_df = coin_dataframes[
            coin_name
        ].copy()  # Create a copy to avoid changing the original DataFrame

        date_start = Timestamp(date_start)
        date_end = Timestamp(date_end)

        # Create a new DataFrame containing only 'Date' and 'Daily_Return'
        vol_df = coin_df[["Date", "Daily_Return"]].loc[(coin_df['Date'] >= date_start) & (coin_df['Date'] < date_end)]


        # Remove NaN values that resulted from the rolling window calculation
        vol_df.dropna(inplace=True)

        # Store this DataFrame in the dictionary with the coin's name as the key
        vol_dfs[coin_name] = vol_df



   # Initialize the combined dataframe with the first coin's data (Bitcoin). Bitcoin is oldest coin. 
    combined_df = vol_dfs[coin_names[0]].set_index("Date")

    # Merge the other dataframes
    for coin_name in coin_names[1:]:
        vol_df = vol_dfs[coin_name].set_index("Date")
        combined_df = combined_df.merge(vol_df[["Daily_Return"]], left_index=True, right_index=True, how="outer", suffixes=('', f'_{coin_name}'))
    
    # Rename columns for clarity
    combined_df.columns = coin_names


    # Return the correlation matrix
    return combined_df.corr().abs()


def matrix_to_objects(matrix):
    
    # Convert the matrix to a DataFrame if it's a list
    if isinstance(matrix, list):
        matrix = pd.DataFrame(matrix)

    # Check if the matrix (DataFrame) is empty
    if matrix.empty:
        return []

    matrix_values = matrix.values
    
    n = len(matrix_values)
    
    # Check if the matrix is nxn
    for row in matrix_values:
        if len(row) != n:
            raise ValueError("The input matrix is not square")
    
    objects = []
    for i in range(n):
        for j in range(n):
            objects.append({"x": i + 1, "y": j + 1, "v": matrix_values[i][j]})

        # Export to a JSON file
    with open('matrix_objects.json', 'w') as json_file:
        json.dump(objects, json_file, indent=4)
            
    return objects


def profit_loss(coin_names, coin_dataframes, date_start, date_end, date_purchase, quantities):
    vol_dfs = {}  # Dictionary to store the DataFrames
    
    # Convert dates to Timestamp outside the loop
    date_start = Timestamp(date_start)
    date_end = Timestamp(date_end)
    date_purchase = Timestamp(date_purchase)

    active = np.nonzero(quantities)[0]

    active_names = [coin_names[i] for i in active]
    
    for coin_name in coin_names:
        # Selecting the DataFrame for the coin
        coin_df = coin_dataframes[coin_name].copy()  # Create a copy to avoid changing the original DataFrame
        
        # Assuming 'Date' is a column in coin_df
        vol_df = coin_df[["Date", "Close"]].loc[coin_df['Date'] >= date_purchase]
        vol_df.dropna(inplace=True)  # Assuming there is a reason for potential NaNs
        vol_dfs[coin_name] = vol_df

    # Initialize the combined dataframe with the first coin's data
    combined_df = vol_dfs[coin_names[0]].set_index("Date")
    
    # Merge the other dataframes
    for coin_name in coin_names[1:]:
        vol_df = vol_dfs[coin_name].set_index("Date")
        combined_df = combined_df.merge(vol_df["Close"], left_index=True, right_index=True, how="outer", suffixes=('', f'_{coin_name}'))
    
    # Rename columns for clarity
    combined_df.columns = coin_names

    # Filter out the coins with zero quantities
    
    nonz_df = combined_df[active_names]
    
    # Filter out the zero quantities
    filtered_quantities = quantities[np.nonzero(quantities)]

    # Calculate total portfolio value
    nonz_df["total_portfolio"] = np.sum(nonz_df * filtered_quantities, axis=1)
    init_investment = nonz_df["total_portfolio"].iloc[0]

    nonz_df["init_investment"] = round(init_investment, 0)
    nonz_df["profit"] = round(nonz_df["total_portfolio"] - init_investment, 0)
    nonz_df["profit_perc"] = round((nonz_df["profit"] / init_investment)*100,0)

    # Filter the DataFrame for the specified date range
    filtered_df = nonz_df.loc[(nonz_df.index >= date_start) & (nonz_df.index < date_end)]


    filtered_df.reset_index(inplace=True)
    filtered_df.rename(columns={'index': 'Date'}, inplace=True)

    json_data = filtered_df.to_json(orient="index", date_format="iso")

    # Write the JSON data to a file
    with open("pna_data.json", "w") as outfile:
        outfile.write(json_data)
    
    # Return the DataFrame
    return filtered_df
