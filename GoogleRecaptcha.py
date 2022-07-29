import json
import requests

def GoogleRecaptcha(GoogleToken,IpAdress=None):
    # RECAPTCHA_SITE_KEY='6LfWPykhAAAAAHg0pYSkTHNnzYI2bDlQAUPXwCzt'
    
    RECAPTCHA_SECRET_KEY='6LfWPykhAAAAACnf4rIu71Gs_WBmJZdZe-i5J1EE'
    headers = {
    "Content-Type": "application/x-www-form-urlencoded"
    }
    body= {
        "secret": RECAPTCHA_SECRET_KEY,
        "response": GoogleToken,
        "remoteip": IpAdress
    }
    recaptcha_resp = requests.post(" https://www.google.com/recaptcha/api/siteverify",data=body,headers=headers)
    recaptcha_resp=recaptcha_resp.json()
    print(recaptcha_resp)
    return recaptcha_resp