from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.forms.models import model_to_dict
from django.utils import timezone

from analyze.models import Website

import json
from urllib.parse import urlparse

from .utils import get_html, analyze_html

# Create your views here.
def index(request):
    """
    Handles GET and POST requests.
    On GET, displays a simple form (text field and submit button).
    On POST, analyzes the given URL.
    """
    try:
        url = request.POST['url']
        parsed = urlparse(url)
        prefix = parsed.scheme + "://" + parsed.netloc

        # Check DB for cached results
        if Website.objects.filter(url=url).exists():
            print("Found website in cache!")

            # Just return the cached result
            site_model = Website.get(url=url)
            site_data = model_to_dict(site_model)
            
            # Don't return URL and time cached to the user
            site_data.pop('url', None)
            site_data.pop('time_cached', None)
        else:
            print("Website not cached, fetching HTML")

            # If not cached, retrieve HTML and analyze it
            html = get_html(url)      
            site_data = analyze_html(html, prefix)
            
            # Cache analysis in DB
            site_model = Website(**site_data)
            site_model.url = url
            site_model.time_cached = timezone.now()
            site_model.save()
                
        # TODO: Delete old (not accessed in past 24 hours) results

        return HttpResponse(json.dumps(site_data), content_type='application/json')
    except KeyError:
        return render(request, 'analyze/index.html')

        
    
