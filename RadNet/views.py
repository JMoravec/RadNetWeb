from django.template import RequestContext
from django.shortcuts import render_to_response
# Create your views here.


def home(request):
    context = RequestContext(request)

    return render_to_response('RadNet/index.html', {}, context)
