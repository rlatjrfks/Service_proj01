# 수집할 페이지 주소를 naver_index 변수에 담아보기

index_cd = 'KPI200'

page_n = 1

naver_index = 'https://finance.naver.com/sise/sise_index_day.nhn?code=' + index_cd + '&page=' + str(page_n)

# 해당 URL의 소스 코드를 긁어와서 source 변수에 담아보기

from urllib.request import urlopen

source = urlopen(naver_index).read()

source

# 소스 코드를 출력해보니 너무 복잡해서 읽을 수가 없음.

# 뷰티플 수프를 이용해 태그별로 분류하겠음.

# 소스명.prettify()는 소스를 태그별로 보기 좋게 정돈하는 기능임.

# BeautifulSoup가 들어있는 bs4 라이브러리를 호출하고, 그 다음 뷰티플 수프의 함수를 이용해

# source를 해석한다.


import bs4

source = bs4.BeautifulSoup(source, 'lxml')

# 보기 좋게 출력함

print(source.prettify())

# 우리가 필요한 데이터(날짜와 종가)는 모두 <td> 태그에 들어있는 것을 확인했으니.

# 뷰티플 수프를 이용해서 <td> 태그를 찾아 안에 들어 있는 데이터를 뽑아내는 것을 최종 목표로 함.

# 본격적으로 <td> 태그 분석을 하기 전에 우선 <td> 태그가 몇 개나 있는지 체크.


td = source.find_all('td')

len(td)  # td의 개수 확인

# 화면에 있는 <td? 태그의 개수가 54개로 나왔지만, 일일이 눈으로 확인하기에는 너무 많은 양임.

# 데이터를 대량으로 제공하는 사이트에서 원하는 데이터의 위치를 찾아낼 때는 XPath 주소를 이용하면 편리.

# XPath(XML Path Language)란 웹사이트 또는  XML 문서에 있는

# 각 항목의 주소를 문서에 포함된 태그를 조합한 경로 형태로 포함한 언어임.

# 크롬 브라우저에서 데이터의 XPath 를 확인하는 방법

# 1. 스크린 우측에서 음영으로 선택된 부분에 마우스를 갖다 댄 후,

# 2. 오른쪽 클릭을 하면 나오는 메뉴 중 Copy를 선택한 후,

# 3. Copy XPath를 클릭


# /html/body/div/table[1]/tbody/tr[3]/td[1]

source.find_all('table')[0].find_all('tr')[2].find_all('td')[0]

# 출력  결과 <td class="number_1">297.65</td>

# <td class="date">처럼 class 이름을 이용해 특별히 이름을 붙인 td태그는 아래와 같이

# 이름을 지정해서 뽑아낼 수도 있는데, 이렇게 할 경우 td앞에 붙는 태그를 생략할 수 있어 유용

d = source.find_all('td', class_='date')[0].text

d

# 주의할 점은. XPath는 숫자를 1부터 세지만, 파이썬은 숫자를 0부터 세기 때문에

# Xpath 수에서 -1을 해줘야 한다.

# 원하는 데이터를 찾기는 했는데. 네이버가 지정해놓은 날짜 형식은 파이썬의 날짜 형식과는 다름.

# 파이썬이 날짜를 인식할 수 있도록 형식을 바꿔줌.

# 점(.)으로 구분된 년,월,일을 분리하고, 이를 datetime 라이브러리를 이용해 date 형식으로 바꿔줌.


# datetime 라이브러리를 이용하기 위해 먼저 datetime 라이브러리를 dt라는 이름으로 호출

import datetime as dt

# 이제 문자열.split(구분자) 함수를 이ㅏ용해 구분자를 기준으로 문자열을 년,월,일로 분해

# 분해한 문자열은 dt.date(년,월,일) 함수를 이용해 날짜 형식으로 바꿔서 this_date 함수에 저장

yyyy = int(d.split('.')[0])

mm = int(d.split('.')[1])

dd = int(d.split('.')[2])

this_date = dt.date(yyyy, mm, dd)

this_date


# 닐짜 형식으로 바뀐 this_date값을 확인 가능

# 읽어온 날짜 정보를 date형식으로 바꿀 일이 계속 생기므로 이 기능을 함수로 정의해줌.

# 함수명은 date_format()

def date_format(d):
    d = str(d).replace('-', '.')

    yyyy = int(d.split('.')[0])

    mm = int(d.split('.')[1])

    dd = int(d.split('.')[2])

    this_date = dt.date(yyyy, mm, dd)

    return this_date


## 이번에는 지수를 가져올 차례

# 해당 일자의 종가지수를 가져옴.


this_close = source.find_all('tr')[2].find_all('td')[1].text

this_close = this_close.replace(',', '')  # 쉼표(,),제거

this_close = float(this_close)  # data를 숫자로 인식

this_close

# 종가지수 역시 간단하게 다음 코드처럼 나타낼 수 있음.

p = source.find_all('td', class_='number_1')[0].text

p

# 이제, 간단한 코드를 이용해 페이지에 있는 모든 날짜와 가격을 불러오자.

dates = source.find_all('td', class_='date')

prices = source.find_all('td', class_='number_1')

# e data의 갯수 확인

print(len(dates))

print(len(prices))

# 소스 코드를 보면 <td class = "number_1"> 코드가 4개 보이는 것을 확인

# 마우스로 각 태그들을 가리켜보면 '체결가','등락률','거래량','거래대금' 칼럼이 모두 같은 태그 사용

# 이 4개의 값 중 첫번째 값만 필요하므로 0,4,8,...등 4의 배수로 나타나는 값들만 추출하기로 함.


# 이제 테이블의 날짜를 한 줄씩 순환하며 날짜와 종가지수를 추출

for n in range(len(dates)):  # dates 개수만큼 반복

    this_date = dates[n].text  # n번째 dates 값 추출

    this_date = date_format(this_date)  # 날짜 형식으로 반환

    this_close = prices[n * 4].text  # 0,4,8,... 등 4의 배수에 해당하는 종가지수 추출

    this_close = this_close.replace(',', '')  # 쉼표(,) 제거

    this_close = float(this_close)  # 숫자 형식으로 변환

    this_close

    print(this_date, this_close)  # 결과값 출력

# 현재 페이지에서의 날짜와 종가지수 추출을 위처럼 완료

# 이제, 다음 페이지,그 다음 페이지에서 반복해서 추출할 차례

# 페이지를 하나씩 넘겨가며 추출을 하다가 마지막 페이지에 도달하면 더 이상 다음 페이지로 못 넘어가도록 해야함

# 이를 위해 마지막 페이지가 어딘지 알아보자

# 마지막 페이지 주소를 가리키는 하이퍼링크 <a> 태그는 <td class = "pgRR"> 태그임.

# 그러면 다음과 같이 하이퍼링크 주소를 뽑아올 수 있음.

paging = source.find('td', class_='pgRR').find('a')['href']

paging

# 뽑아온 하이퍼링크 주소에서 페이지 번호인 507만 추출하기 위해 &를 기준으로 문자열을 잘라

# 뒷부분만 가져옴

paging = paging.split('&')[1]

paging

# 많이 줄어들었음.. 이제 = 을 기준으로 한 번 더 잘라내면 페이지 번호만 남음

paging = paging.split('=')[1]

paging

# 이제 뽑아온 페이지 번호를 숫자 형식으로 바꿔주면 끝.

# 지금까지 내용을 종합해 마지막 페이지 번호를 뽑는 과정 정리


last_page = source.find('td', class_='pgRR').find('a')['href']

last_page = last_page.split('&')[1]

last_page = last_page.split('=')[1]

last_page = int(last_page)

## 마지막 페이지까지 페이지 갱신하면서 원하는 데이터 호출하는 함수 만들기


# -*- coding: utf-8 -*-

# 현재 페이지에서 데이터를 추출하는 작업을 페이지마자 반복해야 하기 때문에

# 함수를 만들어 사용

# 함수 이름은 historical_index_naver()라고 하자.

def historical_index_naver(index_cd, page_n=1, last_page=0):
    naver_index = 'http://finance.naver.com/sise/sise_index_day.nhn?code=' + index_cd + '&page=' + str(page_n)

    source = urlopen(naver_index).read()  # 지정한 페이지에서 코드 읽기

    source = bs4.BeautifulSoup(source, 'lxml')  # 뷰티풀 스프로 태그별로 코드 분류

    dates = source.find_all('td', class_='date')  # <td class="date">태그에서 날짜 수집

    prices = source.find_all('td', class_='number_1')  # <td class="number_1">태그에서 지수 수집

    for n in range(len(dates)):

        if dates[n].text.split('.')[0].isdigit():
            # 날짜 처리

            this_date = dates[n].text

            this_date = date_format(this_date)

            # 종가 처리

            this_close = prices[n * 4].text  # prices 중 종가지수인 0,4,8,...번째 데이터 추출

            this_close = this_close.replace(',', '')

            this_close = float(this_close)

            # 딕셔너리에 저장

            historical_prices[this_date] = this_close

    # 페이지 네비게이션

    if last_page == 0:
        last_page = source.find('td', class_='pgRR').find('a')['href']

        # 마지막페이지 주소 추출

        last_page = last_page.split('&')[1]  # & 뒤의 page=506 부분 추출

        last_page = last_page.split('=')[1]  # = 뒤의 페이지번호만 추출

        last_page = int(last_page)  # 숫자형 변수로 변환

    # 다음 페이지 호출

    if page_n < last_page:
        page_n = page_n + 1

        historical_index_naver(index_cd, start_date, end_date, page_n, last_page)

    return historical_prices


# 네이버에서 일자별 인덱스를 추출하는 함수 정의


def historical_index_naver(index_cd, start_date='', end_date='', page_n=1, last_page=0):
    if start_date:  # start_date가 있으면

        start_date = date_format(start_date)  # date 포맷으로 변환

    else:  # 없으면

        start_date = dt.date.today()  # 오늘 날짜를 지정

    if end_date:

        end_date = date_format(end_date)

    else:

        end_date = dt.date.today()

    naver_index = 'http://finance.naver.com/sise/sise_index_day.nhn?code=' + index_cd + '&page=' + str(page_n)

    source = urlopen(naver_index).read()  # 지정한 페이지에서 코드 읽기

    source = bs4.BeautifulSoup(source, 'lxml')  # 뷰티풀 스프로 태그별로 코드 분류

    dates = source.find_all('td', class_='date')  # <td class="date">태그에서 날짜 수집

    prices = source.find_all('td', class_='number_1')  # <td class="number_1">태그에서 지수 수집

    for n in range(len(dates)):

        if dates[n].text.split('.')[0].isdigit():

            # 날짜 처리

            this_date = dates[n].text

            this_date = date_format(this_date)

            if this_date <= end_date and this_date >= start_date:

                # start_date와 end_date 사이에서 데이터 저장

                # 종가 처리

                this_close = prices[n * 4].text  # prices 중 종가지수인 0,4,8,...번째 데이터 추출

                this_close = this_close.replace(',', '')

                this_close = float(this_close)

                # 딕셔너리에 저장

                historical_prices[this_date] = this_close



            elif this_date < start_date:

                # start_date 이전이면 함수 종료

                return historical_prices

                # 페이지 네비게이션

    if last_page == 0:
        last_page = source.find('td', class_='pgRR').find('a')['href']

        # 마지막페이지 주소 추출

        last_page = last_page.split('&')[1]  # & 뒤의 page=506 부분 추출

        last_page = last_page.split('=')[1]  # = 뒤의 페이지번호만 추출

        last_page = int(last_page)  # 숫자형 변수로 변환

    # 다음 페이지 호출

    if page_n < last_page:
        page_n = page_n + 1

        historical_index_naver(index_cd, start_date, end_date, page_n, last_page)

    return historical_prices


#

index_cd = 'KPI200'

historical_prices = dict()

historical_index_naver(index_cd, '2020-12-1', '2020-12-4')

historical_prices