from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
# StackedInline 대신에 TavularINline을 사용하면, 관련된 객체는 좀 더 조밀하고
# 테이블 기반 형식으로 표시된다
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['colllapse']
        }),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
"""
기본적으로 Django는 각 객체의 str()을 표시한다 그러나 개별 필드를 표시 할 수 있는
경우 가끔 도움이 될수 있다 이렇게 하려면 list_display admin옵션을 사용한다
이 옵션은 객체의 변경 목록 페이지에서 열로 표시 할 필드 이름들의 튜플이다
"""
admin.site.register(Question, QuestionAdmin,)

"""
Question 모델을 admin.site.register에 등록함으로서, Django는 디폴트 폼 표현을
구성 할 수있었다. 관리 폼이 보이고 작동하는 방법을 커스터마이징 하려는 경우가 있다
객체를 등록 할 때 Django에 원하는 옵션을 알려주면 커스터마이징 할 수 있다
모델의 관리자 옵션을 변경해야 할 때마다 이 패턴 - 모델 어드민 클래스를 만든 다음,
admin.site.register()에 두 번째 인수로 전달한다
fieldsets의 각 튜플의 첫 번째 요소는 fieldset의 제목이다
"""
