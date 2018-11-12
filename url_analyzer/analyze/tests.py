from django.test import TestCase

from .utils import get_html_version, has_login_form, is_internal_link


class GetHTMLVersionTests(TestCase):
    def test_get_html_version_with_html5(self):
        html = "<!doctype html>\nHello World!"
        version = get_html_version(html)
        self.assertEqual(version, "HTML5")
    
    def test_get_html_version_with_html4(self):
        html = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd>\nHello World!'
        version = get_html_version(html)
        self.assertEqual(version, "HTML 4.01 Strict")
    
    def test_get_html_version_with_unknown(self):
        html = "ASKJDHJWIUADew8r73249r423rdzsd"
        version = get_html_version(html)
        self.assertEqual(version, "Unknown")



