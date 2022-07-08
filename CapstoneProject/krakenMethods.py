"""
CTB (Crypto Trading Bot) - krakenMethods.py

Author:                     Mitchell Phelps
Date Last Modified:         July 6, 2022

Description:

    This file has all of the methods needed within the KrakenAPI.
    Notably, it has the methods to communicate with thier servers, get_kraken_signature
    and kraken_request. It also contains the methods to check account balances in
    getAccountBalance, and the ability to execute trades in addOrder.

    All methods are from the Kraken API documentation at: https://docs.kraken.com/rest/

"""

# Libaries needed for Kraken methods.
import urllib.parse
import hashlib
import hmac
import base64
import time
import requests

# Import api_key and api_sec.
from keys import api_key, api_sec

# URL for api.
api_url = "https://api.kraken.com"

# Method to allow access to perform actions on a Kraken account.
def get_kraken_signature(urlpath, data, secret):

    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

# Method to allow POST requests from Kraken servers. Returns results of request.
def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)             
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req

# Gets all cash balances from account.
def getAccountBalance():
    resp = kraken_request('/0/private/Balance', 
        {"nonce": str(int(1000*time.time()))}, 
        api_key, 
        api_sec)

# Adds an order the the account, either buy or sell.
def addOrder(ordertype, type, volume, pair, price):
    resp = kraken_request('/0/private/Balance',
        {"nonce": str(int(1000*time.time())),
        "ordertype": ordertype,
        "type":      type,
        "volume":    volume,
        "pair":      pair,
        "price":     price},
        api_key,
        api_sec)
