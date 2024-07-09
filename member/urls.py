from django.urls import path
from .import views
from .views import *

app_name = 'member'

urlpatterns = [
    path('signup/', sign_up),
    path('login/', log_in),
    path('info/', user_info),
    path('post/', user_post),
]