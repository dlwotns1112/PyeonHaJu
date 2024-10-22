import pandas as pd
from .bandAPI import *
from .db_utils import DatabaseManager

db_manager = DatabaseManager()


def get_dataframe():
    # 샘플 데이터프레임 생성
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [24, 30, 22],
        'City': ['New York', 'Los Angeles', 'Chicago']
    }
    df = pd.DataFrame(data)
    return df


def get_search_post(keyword):
    post_list = get_band_posts2()
    if not post_list:
        return pd.DataFrame()  # 빈 데이터프레임 반환

    db_posts = db_manager.get_db_posts()

    create_list = []
    update_list = []
    if db_posts.empty:
        for post in post_list:
            author = post.get('author', {})
            if all(key in post for key in ['post_key']) and all(key in author for key in ['user_key', 'name']):
                create_list.append({
                    'post_key': post['post_key'],
                    'user_key': author['user_key'],
                    'name': author['name'],
                })
    else:
        for post in post_list:
            if 'post_key' not in post or 'author' not in post or 'user_key' not in post['author'] or 'name' not in post[
                'author']:
                continue  # 필요한 키가 없는 경우 건너뜀
            if not (db_posts['post_key'] == post['post_key']).any():
                create_list.append({
                    'post_key': post['post_key'],
                    'user_key': post['author']['user_key'],
                    'name': post['author']['name'],
                })

    db_manager.insert_posts(create_list)

    data = search_post(keyword, post_list)
    return data if not data.empty else pd.DataFrame()  # 빈 데이터프레임 반환
