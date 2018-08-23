from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
# 뷰에 request가 오게되면 view에서 HttpResponse를 반환하게된다
