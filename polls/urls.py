from django.urls import path
# view를 호출하려면 이와 연결된 URL이 있어야 하는데, 이를 위해 URLconf가 사용된다
# polls 디렉토리에서 URlconf를 생성하려면 urls.py라는 파일이 있어야한다
from . import views

app_name = 'polls'
"""
실제 Django의 project는 app이 몇개라도 올수있다 만약 blog라는 app이 있을 경우
Django 는 이름공간(namespace)을 추가하여 이를 구별할수 있게 역할을해준다
app_name을 추가하여 app의 이름공간을 설정할수있다 
"""
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # name 값은 {% url %} template tag에 의해 불러올수있다
    path('<int:question_id>', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
"""
사용자가 웹사이트의 페이지를 요청할 때, 예로 /"polls/34/"를 요청했다 하면,
Django는 mysite.urls 파이썬 모듈을 불러오게 된다 ROOT_URLCONF 설정에 의해 해당
모듀을 바라보도록 지정되어 있기 때문이다 mysite.urls에서 urlpatterns라는 변수를
찾고, 순서대로 패턴을 따라간다 'polls/'를 찾은 후엔, 일치하는 텍스트("polls/")를
버리고, 남은 텍스트인 "34/"를 'polls.urls'URLconf로 전달하여 남은처리를 진행한다
거기에 '<int:question_id>/'와 일치하여, 결과적으로 detail()view함수를 호출한다
-다음은 views.py detail 함수부분의 주석을 참고-
"""
