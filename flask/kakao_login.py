import requests

# GET HTTP/1.1
# https://kauth.kakao.com/oauth/authorize?client_id=7de6eba98a900d9c18e21fedc74b92ae&redirect_uri=http://127.0.0.1:5000/&response_type=code
app_key = "7de6eba98a900d9c18e21fedc74b92ae"
code = "z_UQ00KWDgFIqbRWYJ4Mo7Tt-wzVQCJ5QNkCFXicg724qiX5YXgOUk0yo8YOny2X84uKGQo9dNoAAAF16zARKA"

url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type": "authorization_code",
    "client_id": app_key,
    "redirect_uri": "http://127.0.0.1:5000/portfolio",
    "code": code

}
response = requests.post(url, data=data)

tokens = response.json()

print(tokens)
