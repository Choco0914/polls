from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
"""
template 에 context를 채워 표현한 결과를 HttpResponse 객체와 함께 돌려주는 구문은
자주 쓰인다 따라서 Django는 이런 표현을 쉽게 표현할수 있도록 단축 기능(shortcuts)을
제공한다 그래서 임포트했던 loader와 HttpREsponse를 더이상 이용하지 않고
render를 이용하자
* 만약 객체가 존재하지 않을때 get()을 사용하여 Http404 예외를 발생시키는 것은 자주
사용되는 용법이다 django에서는 이기능에 대한 단축을 제공한다
"""
# HttpREsponse는 사용자가 원하는 페이지의 요청을 반환해주는 역할을해준다
from .models import Choice, Question
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
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    # request는 Httprequest의 개체이다
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        # request.POST 는 키로 전송된 자료에 접근할수 있또록 하는 사전과 같은객체
        # request.POST['choice']는 선택된 설문의 ID를 문자열로 반환한다
        # Django는 request.get도 제공하지만 POST요청을 통해서만 자료가 수정되게
        # 하기위해서 ,명시적으로 코드에 request.POST를 사용한다
        # 만약 POST자료에 chocie가 없으면, request.POST['choice']는 KeyError
        # 가 일어나게 된다
    except (KeyError, Choice.DoesNotExist):
        # KeyError 를 체크하고, choice가 주어지지 않은 경우에는 에러메시지와 함께
        # 설문조사 폼을 다시 보여준다
        return render(request, 'polls/detail.html', {
            'question' : question,
            'error_message' : "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # 설문지의 수가 증가한 이후에, 코드는 일바 HttpResponse가 아닌
        # HttpResponseRedirect를 반환하고, HttpresponseREdirect는 하나의 인수를
        # 그 인수는 사용자가 재전송될 URL이다.
        # POST데이터를 성공적으로 ㅓ리 한 후에 항상 HttpResponseRedirect 를
        # 반환해야 한다 이팁은 Django에서만 국한되는것이 아닌 웹개발의 권장사항이다
        # 우리는 HttpResponseRedirect 생성자 안에서 reverse()함수를 사용하고 있다
        # 이 함수는 뷰 함수에서 URL을 하드 코딩하지 않도록 도와준다. 제어를 전달하기
        # 원하는 뷰의 이름을, URLㅍ턴의 변수부분을 조합해서 해당 뷰를 가리킨다
        # 여기서 우리는 설정했던 URLconf를 사용하였으며, 이 reverse() 호출은
        # '/polls/3/result/'와 같은 문자열을 반환하게 된다
