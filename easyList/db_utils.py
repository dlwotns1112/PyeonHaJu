from .models import *
import pandas as pd


class DatabaseManager:

    def get_db_posts(self):
        all_posts = Post.objects.all()
        posts = [{
            'post_key': post.post_key,
            'pick_date': post.pick_date,
            'item_type_count': post.item_type_count,
            'item_name': post.item_name,
            'user_key': post.user.user_key  # 외래 키 필드
        } for post in all_posts]

        return pd.DataFrame(posts)

    def get_users(self):
        all_users = User.objects.all()
        return all_users

    def insert_posts(self, post_list):
        if not post_list:
            return

        # user_key를 추출해서 중복을 제거한 후 리스트로 변환
        user_keys = list(set(data.get('user_key') for data in post_list if 'user_key' in data))
        if not user_keys:
            return

        # 한 번의 쿼리로 필요한 사용자 객체 가져오기
        existing_users = User.objects.filter(user_key__in=user_keys)

        # user_key를 기준으로 사용자 객체를 딕셔너리로 변환
        user_dict = {user.user_key: user for user in existing_users}

        # 추가할 새로운 사용자 객체 리스트 생성
        new_users = []
        for data in post_list:
            user_key = data.get('user_key')
            if user_key and user_key not in user_dict:
                new_user = User(user_key=user_key, name=data.get('name', ''))
                new_users.append(new_user)
                user_dict[user_key] = new_user

        # 새로운 사용자 객체를 bulk_create로 추가
        User.objects.bulk_create(new_users)

        # Post 객체 리스트 생성
        post_objects = [
            Post(post_key=data.get('post_key'), user=user_dict.get(data.get('user_key')))
            for data in post_list if 'post_key' in data and 'user_key' in data
        ]

        if post_objects:
            # bulk_create를 사용하여 Post 객체를 데이터베이스에 저장
            Post.objects.bulk_create(post_objects)


    def insert_users(self, user_list):
        user_objects = [User(**user) for user in user_list]
        User.objects.bulk_create(user_objects)
        return
