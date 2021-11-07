from django.shortcuts import render
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth

# Create your views here.

def login(*args, **kwargs):
    url = "https://api-sandbox.uphold.com/oauth2/token"
    payload={'code':'375f9acd02ebd852a8d815354a439d9293797eea','grant_type':'authorization_code'}
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.request("POST", url, headers=headers, data=payload, auth=HTTPBasicAuth('a25007a0360611d7925dd82511ee5cd46f3cfac7','18aca46cf8c28436a0375db9456bb5c3218f8ec4'))


    print(response.text)
    return HttpResponse(response.json())

def home(*args, **kwargs):
    return HttpResponse("<p>hello</p>")
