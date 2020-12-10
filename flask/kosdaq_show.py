import pandas as pd
# 필요한 모듈 import 하기
import plotly.express as px

df = pd.DataFrame()
for page in range(1,21):
    url = 'https://finance.naver.com/sise/sise_index_day.nhn?code=KOSDAQ'
    url = '{url}&page={page}'.format(url=url, page=page)
    # print(url)
    df = df.append(pd.read_html(url, header=0)[0], ignore_index=True)

# df.dropna()를 이용해 결측값 있는 행 제거
df = df.dropna()

df = df.rename(columns= {'날짜': 'date', '체결가': 'close'})
# 데이터의 타입을 int형으로 바꿔줌
df['close','volume'] = df['close'].astype(int)

# 컬럼명 'date'의 타입을 date로 바꿔줌
df['date'] = pd.to_datetime(df['date'])

#반응형 그래프 그리기
fig = px.line(df, x='date', y='close', title='코스닥 지수')

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=3, label="3m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(step="all")
        ])
    )
)
fig.show()

# fig.write_html("file.html")