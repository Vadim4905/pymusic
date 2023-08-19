# from home import models
import base64
import requests
import json


CLIENT_ID = 'f2ca18ad51b346cab6d52d36a781252a'
CLIENT_SECRET = '297fd336672c47418dce7068d0a675c1'

def get_token():
    auth_string = CLIENT_ID +':'+ CLIENT_SECRET
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes),'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': "Basic " + auth_base64,
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    result = requests.post(url,headers=headers,data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def get_auth_headers(token):
    return {'Authorization' : 'Bearer ' + token}

def search_for_artist(token,artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_headers(token)
    query = f'?q={artist_name}&type=artist&limit=1'

    query_url = url+query
    result = requests.get(query_url,headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    if json_result:
        return json_result[0]
    else:
        print("Artist wasn't found ")
        return None

token = get_token()
artist_json = search_for_artist(token,'twenty one pilots')
artist_id = artist_json['id']