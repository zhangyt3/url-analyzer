from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.forms.models import model_to_dict
from django.utils import timezone

from analyze.models import Website

import json
from urllib.parse import urlparse

from .utils import validate_url, get_html, analyze_html


def index(request):
    """
    Handles GET and POST requests.
    On GET, displays a simple form (text field and submit button).
    On POST, analyzes the given URL.
    """
    try:
        url = request.POST['url']

        # If the URL is not valid, return an error response
        if not validate_url(url):
            return HttpResponse(json.dumps({
                'reason': 'URL given is not valid.'
            }), status=422, content_type='application/json')

        # Extract the base URL
        parsed = urlparse(url)
        base_url = parsed.scheme + "://" + parsed.netloc

        site = None

        # Check DB for cached results
        if Website.objects.filter(url=url).exists():
            site = Website.objects.get(url=url)

            if site.is_recent():
                # If the results are from the past 24 hours, just use them
                site_data = model_to_dict(site)
                
                # But don't return id, URL, or time cached to the user
                site_data.pop('id', None)
                site_data.pop('url', None)
                site_data.pop('time_cached', None)
            else:
                # If cached analysis is stale, delete it
                site.delete()
        
        # If not cached or the cached results are old, we will
        # retrieve the HTML and analyze it
        if site is None:
            html = get_html(url)      
            site_data = analyze_html(html, base_url)
            
            # Cache analysis in DB
            site = Website(**site_data)
            site.url = url
            site.time_cached = timezone.now()
            site.save()

        return HttpResponse(json.dumps(site_data), content_type='application/json')
    except KeyError:
        return render(request, 'analyze/index.html')

        
    
