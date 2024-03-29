from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


import urllib.request
from urllib.parse import urlparse
from urllib3 import PoolManager
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from bs4 import BeautifulSoup


def validate_url(url):
    validate = URLValidator()
    try:
        validate(url)
        return True
    except ValidationError:
        return False


def get_html(url):
    """Retrieve the HTML for the URL specified."""
    with urllib.request.urlopen(url) as f:
        f_bytes = f.read()
        return f_bytes.decode('ISO-8859-1')
    

def get_html_version(html):
    """Returns the HTML version of the HTML given."""
    html = html.lower()
    if html.startswith("<!doctype html>"):
        return "HTML5"
    elif html.startswith('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"'.lower()):
        return "HTML 4.01 Strict"
    elif html.startswith('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"'.lower()):
        return "HTML 4.01 Transitional"
    elif html.startswith('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN"'.lower()):
        return "HTML 4.01 Frameset"
    elif html.startswith('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"'.lower()):
        return "XHTML 1.0 Strict"
    elif html.startswith('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"'.lower()):
        return "XHTML 1.0 Transitional"
    elif html.startswith('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN"'.lower()):
        return "XHTML 1.0 Frameset"
    elif html.startswith('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"'.lower()):
        return "XHTML 1.1"
    else:
        return "Unknown"


def has_login_form(soup):
    """Returns True if there is an input field with type password."""
    inputs = soup.find_all('input')
    for inp in inputs:
        if inp.get('type') == 'password':
            return True
    return False


def is_internal_link(link, base_url):
    """Returns True if the link has the same base URL as the webpage
    we are analyzing or if the link has no base URL.
    """
    parsed = urlparse(link)
    if str(parsed.scheme) + "://" + str(parsed.netloc) == base_url\
       or parsed.netloc == '':
        return True
    else:
        return False


def is_accessible(link):
    if not validate_url(link):
        return False

    try:
        sess = requests.Session()
        retry = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504],
                    raise_on_status=False,
                    raise_on_redirect=False)
        sess.mount('http://', HTTPAdapter(max_retries=retry))        
        response = sess.head(link)
        return int(response.status_code) < 400
    except:
        return False


def analyze_links(links, base_url):
    """Counts the number of internal, external, and inaccessible links."""
    num_internal = 0
    num_external = 0
    num_inaccessible = 0
    for link in links:
        if link is None:
            continue

        new_link = link
        if is_internal_link(link, base_url):
            num_internal += 1

            # If internal, append the domain so that we can check for accessibility later
            if not link.startswith(base_url):
                new_link = base_url + link
        else:
            num_external += 1

        if not is_accessible(new_link):
            num_inaccessible += 1
    
    return num_internal, num_external, num_inaccessible

def analyze_html(html, base_url):
    """Analyze the HTML passed in.
    Information retrieved:
      - HTML version
      - Page title
      - # of occurrences of each heading level (h1, h1, ...)
      - # of internal links
      - # of external links
      - # of inaccessible links
      - Is there a login form?
    """
    res = dict()
    soup = BeautifulSoup(html, 'html.parser')

    # Extract HTML version
    res['html_version'] = get_html_version(html)

    # Extract title
    res['title'] = soup.title.string

    # Find # of occurrences of each heading level
    for level in range(1, 7):
        tag = "h{}".format(level)
        header_tags = soup.find_all(tag)
        res['{}s'.format(tag)] = len(header_tags)

    # Links
    links = [a.get('href') for a in soup.find_all('a')]
    num_internal, num_external, num_inaccessible = analyze_links(links, base_url)
    res['links_internal'] = num_internal
    res['links_external'] = num_external
    res['links_inaccessible'] = num_inaccessible

    # Is there a login form?
    res['has_login'] = has_login_form(soup)

    return res
