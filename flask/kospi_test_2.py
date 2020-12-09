# import pandas_datareader as web
# import datetime
#
#
# # 시간 설정
# start = datetime.datetime(2016,1,1)
# end = datetime.datetime(2020,12,1)
#
# # KOSPI는 종목 이름, google은 api 사용처임
# # KOSPI = web.DataReader('KRX:KOSPI','google', start, end)
# KOSPI = web.DataReader('KRX:KOSPI','google')
# KOSPI
#
# KOSPI['Open'].plot()
# KOSPI['Close'].plot()
from pandas_datareader import data

# 두 가지의 방식
# 방법 1
df = data.DataReader("^KS11", "yahoo")
# 방법 2
# df = data.get_data_yahoo("^KS11")
# df