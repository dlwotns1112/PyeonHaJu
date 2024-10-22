import requests
import pandas as pd
from .models import *
from .db_utils import DatabaseManager
import json
with open('config.json') as config_file:
    config = json.load(config_file)

access_token = config['ACCESS_TOKEN']
band_key = config['BAND_KEY']

db_manager = DatabaseManager()

def get_band_list(access_token):
    url = 'https://openapi.band.us/v2.1/bands'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


def get_band_posts(access_token, band_key, after):
    if after == '':
        url = f'https://openapi.band.us/v2/band/posts?band_key={band_key}'
    else:
        url = f'https://openapi.band.us/v2/band/posts?band_key={band_key}&after={after}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'result_data' not in data or 'items' not in data['result_data']:
            return None
        return data
    else:
        print(f"Error: {response.status_code}")
        return None


def get_band_posts2():
    after = ''
    post_list = []
    # 20개씩 10번 호출해서 postLists에 저장
    for i in range(0, 10):
        posts = get_band_posts(access_token, band_key, after)
        if posts is None or 'result_data' not in posts or 'items' not in posts['result_data']:
            continue
        after = posts['result_data']['paging']['next_params']['after']
        for post in posts['result_data']['items']:
            post_list.append(post)
    return post_list


def search_post(keyword, post_list):
    if not post_list:
        return pd.DataFrame()
    search_list = []
    for post in post_list:
        if (keyword in post['content']):
            search_list.append(
                {'post_key': post['post_key'], 'content': post['content'], 'comment_count': post['comment_count'], 'user_key': post['author']['user_key'], 'name': post['author']['name']}
            )
    if not search_list:
        return pd.DataFrame()
    search_posts = pd.DataFrame(search_list)
    return search_posts



def get_post_comments(access_token, band_key, post_key, after):
    if after == '':
        url = f'https://openapi.band.us/v2/band/post/comments?band_key={band_key}&post_key={post_key}'
    else:
        url = f'https://openapi.band.us/v2/band/post/comments?band_key={band_key}&post_key={post_key}&after={after}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'result_data' not in data or 'items' not in data['result_data']:
            return None
        return data
    else:
        print(f"Error: {response.status_code}")
        return None



# Extract the relevant fields
def extract_fields(json_obj):
    items = json_obj.get('result_data', {}).get('items', [])
    extracted_data = []
    for item in items:
        author = item.get('author', {})
        extracted_data.append({
            'author_name': author.get('name'),
            'user_key': author.get('user_key'),
            'comment_key': item.get('comment_key'),
            'content': item.get('content'),
        })
    return extracted_data


def get_comments(post_key):
    tmpComments = get_post_comments(access_token, band_key, post_key, '')
    if tmpComments is None:
        return pd.DataFrame()
    comments = extract_fields(tmpComments)
    commentsDf = pd.DataFrame(comments)
    while tmpComments['result_data']['paging']['next_params'] != None:
        tmpComments = get_post_comments(access_token, band_key, post_key, tmpComments['result_data']['paging']['next_params']['after'])
        if tmpComments is None:
            break
        tmp = extract_fields(tmpComments)
        tmpCommentsDf = pd.DataFrame(tmp)
        commentsDf = pd.concat([commentsDf, tmpCommentsDf], ignore_index=True)
    return commentsDf
