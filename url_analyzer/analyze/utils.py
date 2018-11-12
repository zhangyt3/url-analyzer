import urllib.request


def get_html(url):
    """Retrieve the HTML for the URL specified."""
    with urllib.request.urlopen(url) as f:
        f_bytes = f.read()
        return f_bytes.decode('ISO-8859-1')