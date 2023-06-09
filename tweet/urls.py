from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tweet/', views.tweet, name='tweet'),
    path('tweet/delete/<int:id>', views.delete_tweet, name='delete-tweet'), # 게시글 삭제
    path('tweet/<int:id>', views.detail_tweet, name='detail-tweet'), # 게시글 디테일 뷰

    path('tweet/comment/<int:id>', views.write_comment, name='write-comment'), # 댓글 쓰기
    path('tweet/comment/delete/<int:id>', views.delete_comment, name='delete-comment'), #댓글 삭제

    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'),
    path('tag/<str:tag>/', views.TaggedObjectLV.as_view(), name='tagged_object_list'),
]
