import pandas as pd
from django.shortcuts import render, redirect
from .utils import *  # 데이터프레임을 가져오는 함수
from .db_utils import DatabaseManager
import json

db_manager = DatabaseManager()


def table_view(request):
    post_list = request.session.get('post_list', None)
    if post_list:
        del request.session['post_list']
        df = pd.read_json(post_list, orient='split')
    else:
        df = pd.DataFrame()
    df['itemName'] = ''
    column_count = len(df.columns)
    # data2 = df.to_json(force_ascii=False, orient='split')
    data = df.values.tolist()

    # print("--------------------------------------------------------------------")
    # print(data)
    # for row in data:
    #     row.append('')
    columns = df.columns.tolist()
    # columns.append("itemName")
    # print(columns)
    # tmpcol = columns
    return render(request, 'table.html', {'columns': columns, 'data': data, 'step': 'post',
                                          'column_count': column_count})


def update_dataframe(request):
    if request.method == 'POST':
        # POST 요청에서 데이터 추출
        data = request.POST.getlist('data[]')
        columns = request.POST.getlist('columns[]')
        column_count = int(request.POST.get('column_count'))

        # DataFrame 생성
        if not data or not columns:
            return render(request, 'table.html', {'columns': [], 'data': [], 'step': 'comment', 'column_count': 0})

        rows = [data[i:i + column_count] for i in range(0, len(data), column_count)]
        new_df = pd.DataFrame(rows, columns=columns)
        # columns = new_df.columns.tolist()
        # data = new_df.values.tolist()
        # bulk update를 위한 리스트
        update_list = []

        for row in new_df.itertuples():
            post_key = row.post_key
            item_name = row.itemName
            if Post.objects.filter(post_key=post_key).exists():
                post = Post.objects.get(post_key=post_key)
                post.item_name = item_name
                update_list.append(post)

        # bulk update
        if update_list:
            Post.objects.bulk_update(update_list, ['item_name'])
        comment_df_list = [get_comments(post.post_key) for post in new_df.itertuples()]

        comments = pd.concat(comment_df_list, ignore_index=True)
        columns = comments.columns.tolist()
        data = comments.values.tolist()
        column_count = len(comments.columns)
        # 여기서 실제 데이터베이스나 모델에 업데이트를 적용해야 합니다.
        # print(new_df)
        return render(request, 'table.html',
                      {'columns': columns, 'data': data, 'step': 'comment', 'column_count': column_count})
        # return None  # 업데이트 후 테이블 뷰로 리디렉션


def search_view(request):
    return render(request, 'search.html')


def search_data(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        if not keyword:
            return redirect('search_view')
        search_posts = get_search_post(keyword)
        if search_posts.empty:
            return redirect('search_view')
        # db_posts = db_manager.get_db_posts()
        # create_list = []
        # update_list = []
        # # print(db_posts)
        # for post in search_posts.itertuples():
        #     if not (db_posts['post_key']==post.post_key).any():
        #         create_list.append({
        #             'post_key': post.post_key,
        #             'user_key': post.user_key,
        #             'name': post.name,
        #         })
        # db_manager.insert_posts(create_list)
        search_posts.drop(['user_key', 'name'], axis=1, inplace=True)
        # print(create_list)
        post_list = search_posts.to_json(force_ascii=False, orient='split')
        # print(post_list)

        request.session['post_list'] = post_list

    return redirect('table_view')


def comment_view(request):
    row_data = request.GET.getlist('row_data[]')
    # row_data를 활용한 추가 로직을 작성
    comments = get_comments(row_data[0])
    columns = comments.columns.tolist()
    data = comments.values.tolist()
    column_count = len(comments.columns)
    # 여기서 실제 데이터베이스나 모델에 업데이트를 적용해야 합니다.
    # print(new_df)
    return render(request, 'table.html',
                  {'columns': columns, 'data': data, 'step': 'comment', 'column_count': column_count})
