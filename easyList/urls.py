from django.urls import path
from .views import *

urlpatterns = [
    path('', main_view, name='main_view'),
    path('table/', table_view, name='table_view'),
    path('search/', search_view, name='search_view'),
    path('update/', update_dataframe, name='update_dataframe'),
    path('searchData/', search_data, name='search_data'),
    path('comments/', comment_view, name='comment_view'),
    path('items/', item_list, name='item_list'),
    path('add_item/', add_item, name='add_item'),
    path('delete_item/<int:item_id>/', delete_item, name='delete_item'),
]
