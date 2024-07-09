from django.urls import path
from .import views
from .views import *

app_name = 'board'

urlpatterns = [
    path('', post_list),
    path('<int:post_id>/', post_detail),
    path('<int:post_id>/comment/', about_comment),
    # path('<int:post_id>/comment/', about_comment),
    path('<int:post_id>/comment/<int:comment_id>/', delete_comment),
]