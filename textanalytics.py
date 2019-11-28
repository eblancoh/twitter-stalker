import os
import configparser
import requests
import json

# Configuration loading
config = configparser.ConfigParser()
config.read("config.ini")

# Cuidado con las cuotas de los Tweets

headers = {
        'Content-Type': "application/json",
        'Ocp-Apim-Subscription-Key': config["textanalytics"]["apiKey"],
        'User-Agent': "PostmanRuntime/7.17.1",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "a8d7dcec-04bd-48f9-80d1-f48df8540d11,05dc53d6-ae0a-46d6-ac53-2bb017cde002",
        'Host': "holygrail-textanalytics.cognitiveservices.azure.com",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "427",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

def language(e):

    url = "https://holygrail-textanalytics.cognitiveservices.azure.com/text/analytics/v2.1/languages"

    payload = json.dumps({
        "documents": [
            {
                "id": 1,
                "text": e["text"]
            }
        ]
    })

    response = requests.request("POST", url, data=payload, headers=headers)
    try:
        lang_resp = json.loads(response.text)['documents'][0]['detectedLanguages']
    except IndexError:
        lang_resp = None
    
    return lang_resp

def sentiments(e):

    url = "https://holygrail-textanalytics.cognitiveservices.azure.com/text/analytics/v2.1/sentiment"
    try:
        payload = json.dumps({
            "documents": [
                {
                    "language": e['detectedLanguages'][0]["iso6391Name"], # documents detectedLanguages iso6391Name
                    "id": 1,
                    "text": e["text"]
                }
                ]
        })

        response = requests.request("POST", url, data=payload, headers=headers)
        try:
            sentiment = json.loads(response.text)['documents'][0]['score']
        except IndexError:
            sentiment = None
    except TypeError: # 'NoneType' object is not subscriptable
        sentiment = None

    return sentiment

def keyPhrases(e):

    url = "https://holygrail-textanalytics.cognitiveservices.azure.com/text/analytics/v2.1/keyPhrases"
    try:
        payload = json.dumps({
            "documents": [
                {
                    "language": e['detectedLanguages'][0]["iso6391Name"], # documents detectedLanguages iso6391Name
                    "id": 1,
                    "text": e["text"]
                }
                ]
        })
        
        response = requests.request("POST", url, data=payload, headers=headers)
        try:
            keywords = json.loads(response.text)['documents'][0]['keyPhrases']
        except IndexError:
            keywords = None
    except TypeError: # 'NoneType' object is not subscriptable
        keywords = None

    return keywords

def entities(e):

    url = "https://holygrail-textanalytics.cognitiveservices.azure.com/text/analytics/v2.1/entities"
    try:
        payload = json.dumps({
            "documents": [
                {
                    "language": e['detectedLanguages'][0]["iso6391Name"], # documents detectedLanguages iso6391Name
                    "id": 1,
                    "text": e["text"]
                }
                ]
        })
        
        response = requests.request("POST", url, data=payload, headers=headers)
        try:
            entities = json.loads(response.text)['documents'][0]['entities']
        except IndexError:
            entities = None
    except TypeError: # 'NoneType' object is not subscriptable
        entities = None

    return entities

