from dotenv import load_dotenv
from epic_mapping import epicMapping
import json
import os
import requests


class Broker:

    def __init__(self):
        load_dotenv()
        self.username = os.environ.get("IG_USERNAME")
        self.password = os.environ.get("IG_PASSWORD")
        self.apiKey = os.environ.get("IG_API_KEY")
        self.useOauth = False

    def login(self):
        url = "https://demo-api.ig.com/gateway/deal/session"
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "X-IG-API-KEY": self.apiKey,
            "Version": "2"
        }
        body = {
            "identifier": self.username,
            "password": self.password,
            "encryptedPassword": "null"
        }
        r = requests.post(url, headers=headers, json=body)
        if r.status_code == 200:
            self.authToken = r.headers["X-SECURITY-TOKEN"]
            self.CST = r.headers["CST"]
            self.accountId = json.loads(r.content.decode("utf-8"))["currentAccountId"]
            print("Access token retrieved.")
        elif r.status_code == 403:
            raise ValueError("Api Key rate limit has been exceeded, please wait and try again later.")
        else:
            raise ValueError("IG API has failed with error code {} and message: {}".format(r.status_code, r.text))

    def oauth_login(self):
        url = "https://demo-api.ig.com/gateway/deal/session"
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "X-IG-API-KEY": self.apiKey,
            "Version": "3",
            "Authorization": self.authToken,
            "IG-ACCOUNT-ID": self.accountId
        }
        body = {
            "identifier": self.username,
            "password": self.password
        }
        r = requests.post(url, headers=headers, json=body)
        if r.status_code == 200:
            oauthContent = json.loads(r.content.decode("utf-8"))["oauthToken"]
            self.oauthAccessToken = oauthContent["access_token"]
            self.oauthRefreshToken = oauthContent["refresh_token"]
            self.useOauth = True
            print("oauth access token retrieved.")
        elif r.status_code == 403:
            raise ValueError("Api Key rate limit has been exceeded, please wait and try again later.")
        else:
            raise ValueError("IG API has failed with error code {} and message: {}".format(r.status_code, r.text))


    def logout(self):
        url = "https://demo-api.ig.com/gateway/deal/session"
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "X-IG-API-KEY": self.apiKey,
            "Version": "1",
            "_method": "DELETE"
        }
        if self.useOauth:
            headers["Authorization"] = "Bearer {}".format(self.oauthAccessToken)
            headers["IG-ACCOUNT-ID"] = self.accountId
        else:
            headers["X-SECURITY-TOKEN"] = self.authToken
            headers["CST"] = self.CST
        r = requests.delete(url=url, headers=headers)
        if r.status_code == 204:
            print("Successfully logged out.")
        elif r.status_code == 403:
            raise ValueError("Api Key rate limit has been exceeded, please wait and try again later.")
        else:
            raise ValueError("IG API has failed with error code {} and message: {}".format(r.status_code, r.text))

    def create_position(self, size, epic, direction):
        url = "https://demo-api.ig.com/gateway/deal/positions/otc"
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "X-IG-API-KEY": self.apiKey,
            "Version": "2"
        }
        if self.useOauth:
            headers["Authorization"] = "Bearer {}".format(self.oauthAccessToken)
            headers["IG-ACCOUNT-ID"] = self.accountId
        else:
            headers["X-SECURITY-TOKEN"] = self.authToken
            headers["CST"] = self.CST
        body = {
            "epic": epic,
            "expiry": "-",
            "direction": direction,
            "size": size,
            "orderType": "MARKET",
            # "timeInForce": "null",
            # "level": "null",
            "guaranteedStop": "false",
            # "stopLevel": "null",
            # "stopDistance": "null",
            "trailingStop": "false",
            # "trailingStopIncrement": "null",
            "forceOpen": "false",
            # "limitLevel": "null",
            # "limitDistance": "null",
            # "quoteId": "null",
            "currencyCode": "USD"
        }
        r = requests.post(url=url, headers=headers, json=body)
        if r.status_code == 200:
            dealReference = json.loads(r.content.decode("utf-8"))["dealReference"]
            print("Successfully created position.")
        elif r.status_code == 403:
            raise ValueError("Api Key rate limit has been exceeded, please wait and try again later.")
        else:
            raise ValueError("IG API has failed with error code {} and message: {}".format(r.status_code, r.text))
        return dealReference

    def confirm_trade(self, dealReference):
        url = "https://demo-api.ig.com/gateway/deal/confirms/{}".format(dealReference)
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "X-IG-API-KEY": self.apiKey,
            "Version": "1"
        }
        if self.useOauth:
            headers["Authorization"] = "Bearer {}".format(self.oauthAccessToken)
            headers["IG-ACCOUNT-ID"] = self.accountId
        else:
            headers["X-SECURITY-TOKEN"] = self.authToken
            headers["CST"] = self.CST
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            dealStatus = json.loads(r.content.decode("utf-8"))["dealStatus"]
            if dealStatus == "REJECTED":
                dealStatusReason = json.loads(r.content.decode("utf-8"))["reason"]
                raise ValueError("Failed to confirm trade with status {} and reason {}.".format(dealStatus, dealStatusReason))
            dealId = json.loads(r.content.decode("utf-8"))["dealId"]
            print("Successfully confirmed trade.")
        elif r.status_code == 403:
            raise ValueError("Api Key rate limit has been exceeded, please wait and try again later.")
        else:
            raise ValueError("IG API has failed with error code {} and message: {}".format(r.status_code, r.text))
        return dealId

    def open_position(self, dealId):
        url = "https://demo-api.ig.com/gateway/deal/positions/{}".format(dealId)
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "X-IG-API-KEY": self.apiKey,
            "Version": "1"
        }
        if self.useOauth:
            headers["Authorization"] = "Bearer {}".format(self.oauthAccessToken)
            headers["IG-ACCOUNT-ID"] = self.accountId
        else:
            headers["X-SECURITY-TOKEN"] = self.authToken
            headers["CST"] = self.CST
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            content = json.loads(r.content.decode("utf-8"))["dealStatus"]
            contractSize = content["position"]["contractSize"]
            direction = content["position"]["direct"]
            openLevel = content["position"]["openLevel"]
            instrumentType = content["market"]["instrumentType"]
            instrumentName = content["market"]["instrumentType"]
            currency = content["position"]["currency"]
            createdDate = content["position"]["createdDate"]
            print(
                "Successfully executed trade to {} {} {} of {} at {} {} on {}.".format(
                    direction,
                    contractSize,
                    instrumentType,
                    instrumentName,
                    openLevel,
                    currency,
                    createdDate
                )
            )
        elif r.status_code == 403:
            raise ValueError("Api Key rate limit has been exceeded, please wait and try again later.")
        else:
            raise ValueError("IG API has failed with error code {} and message: {}".format(r.status_code, r.text))

    def ticker_symbol_to_epic(self, ticker_symbol):
        return epicMapping[ticker_symbol]

    def buy(self, ticker_symbol, size):
        epic = self.ticker_symbol_to_epic(ticker_symbol)
        dealReference = self.create_position(size, epic, "BUY")
        dealId = self.confirm_trade(dealReference)
        self.open_position(dealId)
        return

    def sell(self, ticker_symbol, size):
        epic = self.ticker_symbol_to_epic(ticker_symbol)
        dealReference = self.create_position(size, epic, "SELL")
        dealId = self.confirm_trade(dealReference)
        self.open_position(dealId)
        return

