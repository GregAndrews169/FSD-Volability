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


def coin_data(coins, window_size=21):
    coin_dataframes = {}

    for coin in coins:
        # Construct the full filepath. Add your own directory path if needed
        file_path = f"{coin}.csv"

        # Read the CSV file into a DataFrame
        try:
            coin_dataframes[coin] = pd.read_csv(file_path).iloc[:, 3:]
            print(f"Loaded data for {coin}")

        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred while reading {file_path}: {e}")

    for coin, df in coin_dataframes.items():
        # Ensure the data is sorted by date, as the calculation of returns is sequential
        df.sort_values(by="Date", inplace=True)

        # Convert 'Date' to datetime if it's not already
        df["Date"] = pd.to_datetime(df["Date"])

        # Calculate daily returns as percentage change in closing price
        df["Daily_Return"] = (
            df["Close"].pct_change() * 100
        )  # pct_change() computes the percentage change from the immediately previous row by default.

        # Calculate rolling volatility
        window_size = 21  # Number of trading days in a typical month; can vary depending on your specific analysis
        volatility = df["Rolling_Volatility"] = df["Daily_Return"].rolling(
            window=window_size
        ).std() * (
            252**0.5
        )  # Annualized

        # The 'Volatility' column now stores the standard deviation of daily returns
        # The 'Rolling_Volatility' column now stores the rolling volatility based on the window size specified
        coin_dataframes[coin]["Volatility"] = volatility

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



   # Initialize the combined dataframe with the first coin's data
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



