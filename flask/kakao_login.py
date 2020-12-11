import requests
import json

# GET HTTP/1.1
# https://kauth.kakao.com/oauth/authorize?client_id=7de6eba98a900d9c18e21fedc74b92ae&redirect_uri=http://127.0.0.1:5000/oauth&response_type=code
# app_key = "7de6eba98a900d9c18e21fedc74b92ae"
# code = "MAcE0cPkDxM2U1h3gIF_lVjkU_laxcs711JjPG-S0DHzehDtVl3S6YVo3vSjk5SvOmNAfworDR4AAAF2TbSUdg"

url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type": "authorization_code",
    "client_id": "7de6eba98a900d9c18e21fedc74b92ae",
    "redirect_uri": "http://127.0.0.1:5000/oauth",
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