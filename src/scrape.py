from io import StringIO
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def scrape_data(url='https://finance.yahoo.com/most-active/?offset=0&count=100'):
    # Send a GET request
    response = requests.get(url)

    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table
    table = soup.find('table')

    # Parse the table with pandas
    dfs = pd.read_html(StringIO(str(table)))
    most_active_stocks = dfs[0]
    most_active_stocks['% Change'] = most_active_stocks['% Change'].str.replace('%', '').astype(float) / 100
    most_active_stocks["Color"] = np.where(most_active_stocks["% Change"] < 0, 'red', 'green')

    return most_active_stocks


