from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='logout'),
    path('setting/', settings, name='settings'),
    path('upload', upload, name='upload'),
    path('like', like, name='like'),
    path('comment', comment, name='comment'),
    path('delete_comment', delete_comment, name='delete_comment'),
    path('delete_post', delete_post, name='delete_post'),
    path('add_remove_friend', add_remove_friend, name='add_friend'),
]
