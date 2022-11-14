import requests
import time

HOST = "0.0.0.0"
PORT = 5000
LOGIN_URL = f"http://{HOST}:{PORT}/v1/users/login"

USERNAME = "denis"
PASSWORD = "denis"

POST_ID = 1

COMMENTS_TIME_PERIOD_SEC = 0.0

login_data = {
    "grant_type": "",
    "username": USERNAME,
    "password": PASSWORD,
    "scope": "",
    "client_id": "",
    "client_secret": "",

}
response = requests.post(url=LOGIN_URL, data=login_data)

response_json = response.json()
access_token = response_json['access_token']
token_type = response_json['token_type']

data = {
    "grant_type": "",
    "username": USERNAME,
    "password": PASSWORD,
    "scope": "",
    "client_id": "",
    "client_secret": "",

}
params = {
    "post_id": POST_ID,
    "content": "content"
}
headers = {
    'content-type': 'application/json',
    'Authorization': token_type + " " + access_token
}

URL = f"http://{HOST}:{PORT}/v1/comments"
while True:
    begin_t = time.time()
    response = requests.post(url=URL, data=data, params=params, headers=headers)
    end_t = time.time()
    delta_t = end_t - begin_t

    t_pause = max(.0, COMMENTS_TIME_PERIOD_SEC - delta_t)
    print('status: ', response.status_code, f' time: {delta_t * 1000:.0f} ms, pause: {t_pause * 1000: .0f} ms')
    time.sleep(t_pause)
