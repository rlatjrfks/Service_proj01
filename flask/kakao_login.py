import requests
import json

# 참고자료
# https://ai-creator.tistory.com/170

# GET HTTP/1.1
# https://kauth.kakao.com/oauth/authorize?client_id=7de6eba98a900d9c18e21fedc74b92ae&redirect_uri=http://127.0.0.1:5000/portfolio&response_type=code
app_key = "7de6eba98a900d9c18e21fedc74b92ae"
# code = "MAcE0cPkDxM2U1h3gIF_lVjkU_laxcs711JjPG-S0DHzehDtVl3S6YVo3vSjk5SvOmNAfworDR4AAAF2TbSUdg"

url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type": "authorization_code",
    "client_id": app_key,
    "redirect_uri": "http://127.0.0.1:5000/portfolio",
    "code": "NUrIiJf9i4XSP349IhI0cs6UB9YzsNKzTCMDrKODzANXuktnovvQj1h6jNm92HS11oYPngo9c04AAAF2TcBzDw"

}
response = requests.post(url, data=data)
tokens = response.json()
print(tokens)


#access 토큰과 refresh token저장하기
with open("kakao_code.json", "w") as fp:
    json.dump(tokens, fp)

#저장, 읽어오기
with open("kakao_code.json", "r") as fp:
    ts = json.load(fp)
ts


ts['access_token']



# 참고자료
# https://dydrlaks.medium.com/flask-%EC%B9%B4%EC%B9%B4%EC%98%A4-%EC%82%AC%EC%9A%A9%EC%9E%90%EA%B4%80%EB%A6%AC-rest-api-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0-e07ff5aff018


#  code = str(request.args.get('code'))
#     #return str(code)
#
#     url = "https://kauth.kakao.com/oauth/token"
#     payload = "grant_type=authorization_code&client_id=7de6eba98a900d9c18e21fedc74b92ae&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Foauth&code=" + str(code)
#     headers = {
#         'Content-Type': "application/x-www-form-urlencoded",
#         'Cache-Control': "no-cache",
#          }
#     response = requests.request("POST", url, data=payload, headers=headers)
#     access_token = json.loads(((response.text).encode('utf-8')))['access_token']
#     #return access_token
#
#     url = "https://kapi.kakao.com/v1/user/access_token_info"
#
#     headers.update({'Authorization': "Bearer" + str(access_token)})
#     response = requests.request("GET", url, headers=headers)
#
#     url = "https://kapi.kakao.com/v2/user/me"
#     response = requests.request("POST", url, headers=headers)
#     return (response.text)