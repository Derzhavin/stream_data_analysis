from multiprocessing import Pool
import requests
import time

HOST = "0.0.0.0"
PORT = 5000
LOGIN_URL = f"http://{HOST}:{PORT}/v1/users/login"
USERNAME = "denis"
PASSWORD = "denis"
POST_ID = 1
COMMENTS_TIME_PERIOD_SEC = 0.0
PUBLISHERS_NUM = 32
CONTENT = "Throughout the rest of its running time, “Black Adam” leans into the inevitability of Adam’s evolution toward good-guy status, condensing the transformation of the title character in the first two “Terminator” films (there are even comic bits where people try to teach Adam sarcasm and the Geneva Conventions). \"Black Adam\" then stirs in dollops of a macho sentimentality that used to be common in old Hollywood dramas about loners who needed to get involved in a cause in order to reset their moral compasses or recognize their own worth. But the sharp edge that the film brings to the early parts of its story never dulls."

def task():
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
        "content": CONTENT
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
        time.sleep(t_pause)


if __name__ == '__main__':
    with Pool(PUBLISHERS_NUM) as p:
        p.apply(task)
