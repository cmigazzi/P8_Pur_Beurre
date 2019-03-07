from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(request=request))


def legals(request):
    template = loader.get_template('mentions-legales.html')
    return HttpResponse(template.render(request=request))