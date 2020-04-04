import time
import requests
import json
from authlib.integrations.requests_client import OAuth2Session
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def execute():
    client_id = '45338'
    client_secret = '71939ef0bec5a6e9f956cb0a72f30e51ce224bf1'
    scope = 'read'  # we want to fetch user's email

    # using requests implementation
    client = OAuth2Session(client_id, client_secret, scope=scope)

    # get webpage for authentication
    authorization_endpoint = 'https://www.strava.com/oauth/authorize'
    redirect_uri = 'http://localhost/exchange_token'
    approval_prompt = 'force'
    uri, state = client.create_authorization_url(authorization_endpoint)
    uri += '&redirect_uri=' + redirect_uri
    uri += '&approval_prompt=' + approval_prompt

    # navigate to authentication webpage
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(uri)
    loginUrl = driver.current_url

    # wait for user to act on authentication
    while(not driver.current_url.startswith(redirect_uri)):
        time.sleep(2)

    # act on permission granted to app
    if(driver.current_url.startswith(redirect_uri)):
        if("error=acces_denied" not in driver.current_url):
            oFile = open('/home/gabe/Strava/UserData/user', "w")
            # need to change this filepath to be dynamic

    # prepare our URL to post for user metadata
    files = {
        'client_id': (None, '45338'),
        'client_secret': (None, '71939ef0bec5a6e9f956cb0a72f30e51ce224bf1'),
        'code': (None, (driver.current_url.split('code='))[1].split('&')[0]),
        'grant_type': (None, 'authorization_code'),
    }

    # response is not in json
    response = requests.post('https://www.strava.com/oauth/token', files=files)

    # print our json with double quotes instead of single quotes
    print(json.dumps(response.json()), file=oFile)


    oFile.close()
    driver.quit()
