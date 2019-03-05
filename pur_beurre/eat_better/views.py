from django.http import HttpResponse


def index(request):
    message = "Hello"
    return HttpResponse(message)
