from io import StringIO
import requests
from bs4 import BeautifulSoup
import pandas as pd


def clean_trending_ticker_data():
    # get the trending ticker data into a DataFrame
    trending_df = scrape_table_data('trending-tickers')
    # change numeric columns into ints
    trending_df['% Change'] = trending_df['% Change'].str.replace('%', '').astype(float)
    trending_df['Market Cap'] = trending_df['Market Cap'].apply(convert_to_int)
    trending_df['Volume'] = trending_df['Volume'].apply(convert_to_int)
    return trending_df


def convert_to_int(value):
    value = str(value)
    # define multipliers
    multiplier = {'M': 1e6, 'B': 1e9, 'T': 1e12}

    # extract the numeric part and suffix if not null
    if value == "nan":
        result = 0
    else:
        numeric_part, suffix = value[:-1], value[-1]

        # convert to integer after multiplying by the corresponding multiplier
        result = int(float(numeric_part) * multiplier.get(suffix, 1))
    return result


def scrape_table_data(path):
    global df
    url = f'https://finance.yahoo.com/{path}/'

    # send a GET request to the URL
    response = requests.get(url)

    # check if the request was successful (status code 200)
    if response.status_code == 200:
        # parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # find the table with the class 'W(100%)'
        table = soup.find('table', class_='W(100%)')

        # read the table into a pandas DataFrame
        df = pd.read_html(StringIO(str(table)))[0]
    else:
        print(f"Error: Failed to fetch the page {url}. Status code: {response.status_code}")

    return df


