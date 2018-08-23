from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
# include()함수는 다른 URlconf 들을 참도할 수 있도록 도와준다 Django가
# includE()함수르 만나게 되면, URL 의 그 시점까지 일치하는 부분을 잘라내고,
# 남은 문자열 부분을 후속 처리를 위해 include 된 URlconf 로 전달한다
