import numpy as np
import investpy
Tabl1 = investpy.get_stock_historical_data(stock='TSLA',  country='United States', from_date='05/08/2010',
                                        to_date='30/05/2021')
Tabl2 = investpy.get_index_historical_data(index='S&P 500',  country='United States', from_date='05/08/2010',
                                        to_date='30/05/2021')
r_stock = Tabl1['Close'].resample('D').ffill().pct_change()
r_index = Tabl2['Close'].resample('D').ffill().pct_change()
cov = r_stock.cov(r_index)
print("COV(", "TSLA, S&P 500", ") = ", cov)
print("sigma^2(S&P 500) = ", np.var(r_index))
print("beta = ", cov / np.var(r_index))
