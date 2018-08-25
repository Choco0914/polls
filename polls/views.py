from django.http import HttpResponse
# HttpREsponse는 사용자가 원하는 페이지의 요청을 반환해주는 역할을해준다
from django.template import loader
"""
Django는 project의 TEMPLATES설정에 의해 template을 어떻게 불러오고 렌더링할지
알고있다
"""
from .models import Question
# 데이터베이스의 레코드를 읽기위해 models의 Question클래스를 임포트했다
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
    """
    polls/index.html template 을 불러온 후, context를 전달한다 context는
    template 에서 쓰이는 변수명과, Python 의 객체를 연결하는 사전형 값이다
    """

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
"""
detail(request=<HttpREquest object>, question_id=34)
question_id=34 부분은 <int:question_id>에서 왔다 괄호를 사용하여 URL의 일부를
"캡쳐"하고, 해당 내용을 keyward 인수로서 view함수로 전달한다 문자열의:question_id>
부분은 일치되는 패턴을 구별하기 위해 정의한 이름이며, <int:부분은 어느 패턴이
해당 URL 경로에 일치되어야 하는지를 결정하는 컨버터 이다
"""
def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
