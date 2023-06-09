

from django.contrib import admin
from .models import TweetModel, TweetComment

# Register your models here.
admin.site.register(TweetModel)  # 나의 TweetModel을 Admin에 추가 해 줍니다
admin.site.register(TweetComment)  # 나의 TweetComment을 Admin에 추가 해 줍니다
