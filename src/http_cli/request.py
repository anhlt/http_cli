import requests


def make_request(url):
    r = requests.get(url)
    return r.text