from django.shortcuts import get_object_or_404, render
"""
template 에 context를 채워 표현한 결과를 HttpResponse 객체와 함께 돌려주는 구문은
자주 쓰인다 따라서 Django는 이런 표현을 쉽게 표현할수 있도록 단축 기능(shortcuts)을
제공한다 그래서 임포트했던 loader와 HttpREsponse를 더이상 이용하지 않고
render를 이용하자
* 만약 객체가 존재하지 않을때 get()을 사용하여 Http404 예외를 발생시키는 것은 자주
사용되는 용법이다 django에서는 이기능에 대한 단축을 제공한다
"""
# HttpREsponse는 사용자가 원하는 페이지의 요청을 반환해주는 역할을해준다
from .models import Question
# 데이터베이스의 레코드를 읽기위해 models의 Question클래스를 임포트했다
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
    """
    render()함수는 request객체를 첫번째 인수로 받고, template이름을
    두번째 인수로받으며, context 사전형 객체를 세번째 선택적(optional)인수로 받는다
    인수로 지정된 context 로 표현된 template 의 HttpResponse 객체가 반환된다
    """

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # view는 요청된 질문의 Id 가 없을 경우 Http404 예외를 발생시킨다
    """
    get_object_or_404함수는 Django 모델을 첫번째 인자로 받고, 몇개의 키워드
    인수를 모델 관리자의 get()함수에 넘긴다 만약 객체가 존재하지 않을 경우,
    Http404 예외가 발생한다
    """    
    return render(request, 'polls/detail.html', {'question': question})
"""
detail(request=<HttpRequest object>, question_id=34)
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
