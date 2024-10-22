from django.urls import path
from .views import *

urlpatterns = [
    path('table/', table_view, name='table_view'),
    path('search/', search_view, name='search_view'),
    path('update/', update_dataframe, name='update_dataframe'),
    path('searchData/', search_data, name='search_data'),
    path('comments/', comment_view, name='comment_view'),
]