import urllib.request
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def get_html(url):
    """Retrieve the HTML for the URL specified."""
    with urllib.request.urlopen(url) as f:
        f_bytes = f.read()
        return f_bytes.decode('ISO-8859-1')


def get_html_version(html):
    """Returns the HTML version of the HTML given."""
    if html.lower().startswith("<!doctype html>"):
        return "HTML5"
    elif html.startswith('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd>'):
        return "HTML 4.01 Strict"
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
    if parsed.scheme + "://" + parsed.netloc == base_url\
       or parsed.netloc == '':
        return True
    else:
        return False


def is_accessible(link):
    request = requests.head(link)
    return int(request.status_code) < 400


def analyze_links(links, base_url):
    """Counts the number of internal, external, and inaccessible links."""
    num_internal = 0
    num_external = 0
    num_inaccessible = 0
    for link in links:
        new_link = link
        if is_internal_link(link, base_url):
            num_internal += 1

            # If internal, append the domain so that we can check for accessibility later
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
    res['internal_links'] = num_internal
    res['external_links'] = num_external
    res['num_inaccessible'] = num_inaccessible

    # Is there a login form?
    res['has_login'] = has_login_form(soup)

    return res
