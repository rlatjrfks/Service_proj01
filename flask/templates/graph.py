import time
import urllib.request
import json
from bs4 import BeautifulSoup

TODAY = time.strftime("%Y%m%d")

# 코스피
url1 = 'https://finance.naver.com/sise/sise_rise.nhn'
# 코스닥
url2 = 'https://finance.naver.com/sise/sise_rise.nhn?sosok=1'

up_list = {'kospi':url1, 'kosdaq':url2}


title_list = ['no', 'name', 'close', 'diff', 'per', 'qty', 'open', 'high', 'low', 'sichong', 'per', 'pbr']
for name, url in up_list.items() :
    with urllib.request.urlopen(url) as fs :
        soup = BeautifulSoup(fs.read().decode(fs.headers.get_content_charset()), 'html.parser')

    cnt = 1
    prices =[]
    # 각 데이터는 tr로 시작
    for tr in soup.find_all('tr') :
        # 각 항목은 td로 시작
        td_list = tr.find_all('td')
        try :
            # 빈줄, 라인 등 데이터가 아닌 경우도 있다.
            # 다행히 n 값에 1부터 증가하는 값이 기록되어 있으므로, 이 값이 맞으면 정상적인 데이터로 판단
            if int(td_list[0].text.strip()) == cnt :
                info = {}
                # 총 12 항목에 대하여 set 구조체(info)에 옮긴다.
                for i in range(0,len(td_list)) :
                    data = td_list[i].text.strip()
                    info[title_list[i]] = data
                # 종목 하나 정보 완성 list에 추가
                prices.append(info)
                cnt+=1
        except :
            continue
    # 저장
    fname = TODAY+'_'+name+'_up_list.txt'
    save_to_file_json(fname, prices)
    print('done ', name)