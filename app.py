from flask import Flask, request, render_template, redirect, url_for
import requests
from dotenv import load_dotenv
load_dotenv()
import os
app = Flask(__name__)

# Replace 'YOUR_API_KEY' with your actual Marketstack API key
API_KEY = os.getenv('MARKETSTACK_API_KEY')
API_URL = 'https://api.marketstack.com/v1/eod'


@app.route('/')
def home():
    # Render the home page with no initial result or error
    return render_template("index.html", result=None, error=None)


@app.route('/get_stock_quote', methods=['POST'])
def get_stock_quote():
    symbol = request.form.get('symbol')

    if not symbol:
        # Redirect back to the home page with an error
        return render_template('index.html', result=None, error='Stock symbol is required')

    params = {
        'access_key': API_KEY,
        'symbols': symbol.upper(),
        'limit': 1  # Fetch only the latest record
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if 'data' not in data or not data['data']:
            # Return to the home page with an error if no data is found
            return render_template('index.html', result=None, error=f'No data found for symbol: {symbol}')

        # Extract the stock data
        stock_data = data['data'][0]
        result = {
            'symbol': stock_data['symbol'],
            'open': stock_data['open'],
            'high': stock_data['high'],
            'low': stock_data['low'],
            'last': stock_data['close'],
            'volume': stock_data['volume']
        }

        # Render the home page with the result
        return render_template('index.html', result=result, error=None)

    except requests.exceptions.RequestException as e:
        # Handle API errors and render with an error message
        return render_template('index.html', result=None, error=f'Error fetching stock data: {str(e)}')


if __name__ == '__main__':
    app.run(debug=True)
