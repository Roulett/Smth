import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import datetime
from pandas.tseries.offsets import BDay
import requests
import lxml
import numpy as np

def parse_curr_cb(date, curncy):
    crncy_id = {'USD': 'R01235', 'EUR': 'R01239'}

    year = date.year
    day = date.day
    month = date.month
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req={day}/{month}/{year}'.format(day = day,
                                                                                         month = month,
                                                                                         year = year)
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        result = soup.find('valute', {'id': crncy_id[curncy]})
        result_1 = float(result.find('value').get_text().replace(',', '.'))
    except Exception:
        return None
    return result_1



def sort_array(mu, sigma, array):
    y = (2.* np.pi * sigma **2.)-0.5* np.exp(-0.5 * (array - mu)**2. / sigma**2.)
    y = 1. / y * (array >= 0) + (-y) * (array < 0)
    return array[np.argsort(y)]

def gen_df(dict, today, number_of_quotes):
    Spot = dict['Spot']
    Ticker = dict['Ticker']
    Distribution = dict['Distribution']
    Volatility = dict['Volatility']
    Curncy = dict['Curncy']
    Amount = dict['Amount']

    if Distribution == 'Normal':
        data_gen = np.random.normal(0.0, 1.0, number_of_quotes)
        sorted_array = sort_array(0.0, 1.0, data_gen)
        # you can choose another distribution for another ticker, but now i do not choose it
    Price_list = (Spot * np.exp(np.array(sorted_array)*Volatility)).tolist()
    dates_list = [(today - BDay(a + 1)) for a in range(0, number_of_quotes)] #

    columns = ['Date', 'Price']
    df_output = pd.DataFrame(list(zip(dates_list, Price_list)), columns = columns)
    df_output['Date'] = pd.to_datetime(df_output['Date'])
    df_output['Ticker'] = Ticker
    df_output['Curncy'] = Curncy
    df_output['Amount'] = Amount
    # df_output['Curncy rate'] = [parse_curr_cb(date, curncy) for date, curncy in zip(df_output['Date'], df_output['Curncy'])]
    return df_output


def historical_var(var_interval, number_of_quotes, df):
    number_least = int((1 - var_interval) * number_of_quotes)
    df['Value change'] = df['Price change'] * df['value_share']
    df_combined = df_full[['Value change', 'Date']].groupby("Date").sum()
    var = df['Value change'].nsmallest(number_least).iloc[-1]
    return var

def gen_df_rub(dict, today, number_of_quotes, df_crncy):
    df = gen_df(dict, today, number_of_quotes)
    df_crncy = df_crncy[['Price', 'Date']]
    df_crncy = df_crncy.rename(columns={'Price': 'Curncy rate'})
    df_output =pd.merge(df, df_crncy, how='left', left_on='Date', right_on='Date')
    df_output['Value'] = df_output['Price'] * df_output['Amount']
    df_output['Price in RUB'] = df_output['Price'] * df_output['Curncy rate']
    df_output['Shift Price in RUB'] = df_output['Price in RUB'].shift(-1)
    df_output['Price change'] = (df_output['Price in RUB'] - df_output['Shift Price in RUB']) / df_output['Shift Price in RUB']
    return df_output

def historical_var_1(var_interval, number_of_quotes, df):
    number_least = int((1 - var_interval) * number_of_quotes)
    var = df['Price change'].nsmallest(number_least).iloc[-1]
    return var

if __name__ == "__main__":
    number_of_quotes = 500
    today = datetime.datetime.today().date()
    var_interval = 0.99

    USDRUB_SPOT = parse_curr_cb(today, 'USD')

    dict_tsla = {'Spot': 186.92, 'Ticker': 'TSLA', 'Curncy': 'USD', 'Distribution': 'Normal', 'Volatility': 0.55, 'Amount': 2 }
    dict_aapl = {'Spot': 148.79, 'Ticker': 'AAPL', 'Curncy': 'USD', 'Distribution': 'Normal', 'Volatility': 0.35, 'Amount': 1 }
    dict_usdrub = {'Spot': USDRUB_SPOT, 'Ticker': 'USD', 'Curncy': 'RUB', 'Distribution': 'Normal', 'Volatility': 0.01, 'Amount': 0 }
    dict_sp500 = {'Spot': 3958.79, 'Ticker': 'SP', 'Curncy': 'USD', 'Distribution': 'Normal', 'Volatility': 0.25, 'Amount': 0 }
    dicts = [dict_tsla, dict_aapl, dict_sp500]
    df_crncy = gen_df(dict_usdrub, today, number_of_quotes)
    for dict in dicts:
        df = gen_df_rub(dict, today, number_of_quotes, df_crncy)
        var_h = historical_var_1(var_interval, number_of_quotes, df)
        df['VaR historical'] = var_h
        print('VaR historical for ', dict['Ticker'], " ", var_h)
        try:
            df_full = pd.concat([df_full, df])
        except Exception:
            df_full = df
    value_sum = df_full.loc[df_full['Date'] == today - BDay(1)].loc[:, 'Value'].sum()
    new_dict_value_share = {}
    for dict in dicts:
        value_share = df_full.loc[(df_full['Date'] == today - BDay(1)) & (df_full['Ticker'] == dict['Ticker'])].loc[:, 'Value'].iloc[-1] / value_sum
        dict['value_share'] = value_share
        new_dict_value_share[dict['Ticker']] = value_share
    df_full['value_share'] = [new_dict_value_share[a] for a in df_full['Ticker']]
    var = historical_var(var_interval, number_of_quotes, df_full)
    print('Combined var ', var)
