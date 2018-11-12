from django.shortcuts import render
from django.http import HttpResponse, Http404

import json
from urllib.parse import urlparse

from .utils import get_html, analyze_html

# Create your views here.
def index(request):
    """
    TODO: documentation
    """
    try:
        url = request.POST['url']
        parsed = urlparse(url)
        prefix = parsed.scheme + "://" + parsed.netloc

        # TODO: Check DB for cached results

        # Retrieve HTML and analyze it
        html = get_html(url)      
        data = analyze_html(html, prefix)

        # TODO: Cache in DB

        return HttpResponse(json.dumps(data), content_type='application/json')
    except KeyError:
        return render(request, 'analyze/index.html')

        
    
