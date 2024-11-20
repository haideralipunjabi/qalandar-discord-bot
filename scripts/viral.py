import requests
import logging

API_URL = "https://hin0r4g4zi.execute-api.ap-south-1.amazonaws.com/api/postMessage/"


def run(uid, amount, content):
    for i in range(amount):
        r = requests.post(API_URL + uid, json={"message": content})
        if r.status_code != 200:
            logging.debug(r.content)
            raise Exception(f"Error occured on run {i+1}")
