import requests
import json
from flask import Flask
from flask import request
import pymysql
# GET HTTP/1.1
#https://kauth.kakao.com/oauth/authorize?client_id=7de6eba98a900d9c18e21fedc74b92ae&redirect_uri=http://127.0.0.1:5000/portfolio&response_type=code
#code = "MAcE0cPkDxM2U1h3gIF_lVjkU_laxcs711JjPG-S0DHzehDtVl3S6YVo3vSjk5SvOmNAfworDR4AAAF2TbSUdg"

class code_login:

    def __init__(self):
        return

    def save_token(self, code):
        app_key = "7de6eba98a900d9c18e21fedc74b92ae"
        url = "https://kauth.kakao.com/oauth/token"

        data = {
            "grant_type": "authorization_code",
            "client_id": app_key,
            "redirect_uri": "http://127.0.0.1:5000/portfolio",
            "code": code
        }
        response = requests.post(url, data=data)
        tokens = response.json()
        print("token: "+ str(tokens))

        # access 토큰과 refresh token저장하기
        with open("kakao_code.json", "w") as fp:
            json.dump(tokens, fp)

        # 저장, 읽어오기
        #with open("kakao_code.json", "r") as fp:
        #    ts = json.load(fp)

    # 참고자료
    # https://dydrlaks.medium.com/flask-%EC%B9%B4%EC%B9%B4%EC%98%A4-%EC%82%AC%EC%9A%A9%EC%9E%90%EA%B4%80%EB%A6%AC-rest-api-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0-e07ff5aff018

    def code_auth(self,code):

        url = "https://kauth.kakao.com/oauth/token"
        payload = "grant_type=authorization_code&client_id=7de6eba98a900d9c18e21fedc74b92ae&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fportfolio&code=" + str(code)
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }
        #  response = requests.request("POST", url, data=payload, headers=headers)
        #  print("response status:\n%d" % response.status_code)
        #  print("response headers:\n%s" % response.headers)
        # print("response body:\n%s" % response.text)
        with open('./kakao_code.json.') as json_file:
            json_data = json.load(json_file)
            access_token = json_data["access_token"]
        #access_token = json.loads(((response.text).encode('utf-8')))['access_token']
        print("access_token:"+access_token)

        #return access_token
        #
        url = "https://kapi.kakao.com/v1/user/access_token_info"
        #
        headers.update({'Authorization': "Bearer " + str(access_token)})
        response = requests.request("GET", url, headers=headers)
        print("response status:\n%d" % response.status_code)
        print("response headers:\n%s" % response.headers)
        print("response body:\n%s" % response.text)

        url = "https://kapi.kakao.com/v2/user/me"
        response = requests.request("GET", url, headers=headers)

        jsonObject = json.loads(response.text)
        IDArray = jsonObject.get("id")
        NickArray = jsonObject.get("properties").get("nickname")
        print("ID: ",IDArray)
        print("Nick: ",NickArray)
        self.db_insert(IDArray,NickArray)
        return (response.text)

    def db_insert(self, ID, Nickname):
        db_root = pymysql.connect(
            host='ls-360d5e5827a35e0a46fa340307d68f5a00a3b151.cvbhe0hq8rxv.ap-northeast-2.rds.amazonaws.com', port=3306,
            user='dbmasteruser', passwd='Qa]HHh]dc1NsX>VLfo<=JA^1GcEWOCY$', db='dbmaster', charset='utf8')

        db = db_root
        cur = db.cursor()
        sql = "INSERT INTO user_info(ID, Nickname) VALUES (%s, %s)"
        cur.execute(sql, (ID, Nickname))
        db.commit()

        db = db_root
        cur = db.cursor()

        sql = "SELECT * from user_info"
        cur.execute(sql)

        data_list = cur.fetchall()

        return




