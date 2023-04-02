import pandas as pd
import numpy as np
import requests
import json

# функция для получения данных по акции с помощью Alpha Vantage API
def get_stock_data(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = json.loads(response.text)
    df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index').astype('float')
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    df.columns = [f'{symbol}_{colname.lower().replace(" ", "_")}' for colname in df.columns]
    return df

# получаем данные по акциям Apple и Microsoft
api_key = 'Y97HAN564IVVAABN'
aapl_df = get_stock_data('AAPL', api_key)
msft_df = get_stock_data('MSFT', api_key)

# Найти столбец с ключевым словом "close" в названии
# Переименовать столбец в "close"
aapl_df.rename(columns={[col for col in aapl_df.columns if "close" in col.lower()][0]: "close"}, inplace=True)
msft_df.rename(columns={[col for col in msft_df.columns if "close" in col.lower()][0]: "close"}, inplace=True)

# объединяем данные в один датафрейм
df = pd.concat([aapl_df['close'], msft_df['close']], axis=1)
df.columns = ['AAPL', 'MSFT']

# рассчитываем ежедневную доходность
returns = df.pct_change().dropna()

# рассчитываем коэффициенты беты
cov = np.cov(returns['AAPL'], returns['MSFT'])
beta = cov[0, 1] / cov[1, 1]

# создаем бета-нейтральный портфель
aapl_weight = beta / (1 + beta)
msft_weight = 1 / (1 + beta)
weights = pd.Series({'AAPL': aapl_weight, 'MSFT': msft_weight})

# проверяем, что веса дают бета-нейтральный портфель
portfolio_beta = np.cov(returns @ weights, returns @ weights)[0, 1] / np.var(returns @ weights)
print(f'Beta of the portfolio: {portfolio_beta:.2f}')
weights_dict = weights.mul(100).round(1).astype(str).add('%').to_dict()
print("Weights of assets in portfolio:", weights_dict)
