import datetime
# datetime은 Python의 표준 모델인 datetime 모듈이다 표준 시간대에 대한 지원이
# 활성화 되면 장고는 데이터베이스에 UTC로 datetime정보를 저장하고 표준 시간대를
# 인식하는 datetime 객체를 내부적으로 사용하며 이를 템플릿 및 양식의 최종 사용자
# 시간대로 변환한다
from django.db import models
from django.utils import timezone
# timezone은 Django의 시간대 관련 유틸리티인 django.utils.timezone을 의미한다
# timezone에 의해 settings.py 에 기본 시간대에서 실행 되도록 환경변수를 설정하면
# 표준 시간대가 활성화 되지않았을때 datetime을 이용하지못해
# 이를 대신 이용해 시간을 표시해준다
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    # Charfield는 문자필드를 표현
    pub_date = models.DateTimeField('date published')
    # DateTimeField는 날짜와 시간 필드를 표현한다
    #각 필드가 어떤 자료형을 가질수 있는지를 Django에게 알려준다
    def __str__(self):
        return self.question_text
    # __str__() 메소드를 추가하는것은 객체의 표현을 대화식 프롬프트에서 편하게
    # 보려는 이유 말고도, Django가 자동으로 생성하는 관리 사이트 에서도 표현이
    # 사용되기 때문이다
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    # ForeignKey는 각각의 Choice 가 하나의 Question에 관계된다는 것을
    # Django에게 알려준다
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    # Field는 다양한 선택적 인수를 가질수 있는데 default를 이용하여 vote의
    # 기본값을 0으로 설정하였다
    def __str__(self):
        return self.choice_text
        # __str__() 메소드를 추가하는것은 객체의 표현을 대화식 프롬프트에서 편하게
        # 보려는 이유 말고도, Django가 자동으로 생성하는 관리 사이트 에서도 표현이
        # 사용되기 때문이다
# 각 모델은 django.db.models.Model 이라는 클래스의 서브클래스로 표현한다
# 각각의 클래스 변수들은 모델의 데이터베이스 필드를 나타낸다
