# app.py
from flask import Flask, jsonify, send_file, request
from flask import current_app as app
from flask_cors import CORS
#
# Input from the user
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import matplotlib
from matplotlib.colors import LinearSegmentedColormap
from pandas_datareader.data import DataReader
import json
from coins_list import coins
from data import create_JSON, coin_data, correlation, matrix_to_objects
import traceback


sns.set_style("whitegrid")
plt.style.use("fivethirtyeight")
warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/api/crypto', methods=['POST'])
def get_crypto_data():
    try:

        start_period_str = request.json.get("start_date")
        end_period_str = request.json.get("end_date")

        start_period = datetime.strptime(start_period_str, '%Y-%m-%d').date()
        end_period = datetime.strptime(end_period_str, '%Y-%m-%d').date()

        coin_crypto = coin_data(coins, start_period, end_period)
        create_JSON(["coin_Cardano", "coin_Bitcoin", "coin_Ethereum"], coin_crypto, start_period, end_period)

        # Assuming "volatility_data.json" is correct and the file is in the correct path relative to the application
        return send_file('volatility_data.json', as_attachment=True, download_name='volatility_data.json')
    except Exception as e:
        # Handle exception here
        return str(e), 500
    

@app.route('/api/correlation', methods=['POST'])
def get_correlation_data():
    try:

        start_period_str = request.json.get("start_date")
        end_period_str = request.json.get("end_date")

        start_period = datetime.strptime(start_period_str, '%Y-%m-%d').date()
        end_period = datetime.strptime(end_period_str, '%Y-%m-%d').date()

        coin_crypto = coin_data(coins, window_size=21)
        cor = correlation(["coin_Bitcoin",
                           "coin_Ethereum",
                           "coin_Tether",
                           "coin_BinanceCoin",
                           "coin_XRP",
                           "coin_USDCoin",
                           "coin_Stellar",
                           "coin_Cardano", 
                           "coin_Dogecoin", 
                           "coin_Tron"], coin_crypto, start_period, end_period)

        matrix_to_objects(cor)

        # Assuming "volatility_data.json" is correct and the file is in the correct path relative to the application
        return send_file('matrix_objects.json', as_attachment=True, download_name='matrix_objects.json')
    except Exception as e:
        # Handle exception here
        return str(e), 500



if __name__ == "__main__":
    app.run(debug=True)
