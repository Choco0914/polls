from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
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
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published question."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name= 'polls/results.html'

    """
    각 제너릭 뷰는 어떤 모델이 적용될 것인지 알아야한다 이것은 model 속성을 사용해
    제공한다 DetailView 제너릭 뷰는 URL에서 캡쳐 된 기본 값이 pk\ 라고 기대하기
    때문에 'question_id'를 제너릭 뷰를 위해 pk로 변경했다
    기본적으로 DEtailView 제너릭 뷰는 <app name>/<model name>_detail.html템플릿을
    사용한다 우리의 경우 polls/question_detail.html 템플릿을 사용한다
    template_name 속성은 Django에게 자동 생성 된 기본 템플릿 이름 대신 뷰가
    렌더링 될 때 서로 다른 모습을 갖도록 한다 이들이 둘다 동일한 DetailView를
    사용하고 있더라도 말이다
    마찬가지로 ListView 제너릭 뷰는<app name>/<model name>_list.html 템플릿을
    기본으로 사용한다 이미 있는 polls/index.html 템플릿을 사용하기 위해
    LiveView에 template_name을 전달했다
    """
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
