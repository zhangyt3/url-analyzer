from django.shortcuts import render
from django.http import HttpResponse, Http404

import json

from .utils import get_html

# Create your views here.
def index(request):
    """
    TODO: documentation
    """
    try:
        url = request.POST['url']

        # TODO: Check DB for cached results

        # TODO: Get the webpage HTML
        html = get_html(url)
        data = {
            "html": html
        }
        

        # TODO: Process the HTML

        # TODO: Cache in DB

        return HttpResponse(json.dumps(data), content_type='application/json')
    except KeyError:
        return render(request, 'analyze/index.html')

        
    
