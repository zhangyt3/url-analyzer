from django.test import TestCase

from bs4 import BeautifulSoup

from .utils import get_html_version, has_login_form, is_internal_link


class GetHTMLVersionTests(TestCase):
    def test_get_html_version_html5(self):
        html = "<!doctype html>\nHello World!"
        version = get_html_version(html)
        self.assertEqual(version, "HTML5")
    
    def test_get_html_version_html4(self):
        html = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd>\nHello World!'
        version = get_html_version(html)
        self.assertEqual(version, "HTML 4.01 Strict")
    
    def test_get_html_version_unknown(self):
        html = "ASKJDHJWIUADew8r73249r423rdzsd"
        version = get_html_version(html)
        self.assertEqual(version, "Unknown")


class HasLoginFormTests(TestCase):
    def test_has_login_form_no_form(self):
        html = "<!doctype html>\nHello World!"
        soup = BeautifulSoup(html, 'html.parser')
        self.assertFalse(has_login_form(soup))
    
    def test_has_login_form_yes_form(self):
        html = """<!doctype html>
        <form action="http://example.com" method="post">
            <input type="text", name="username">
            <input type="password", name="password">
            <input type="submit", value="Login">
        </form>
        """
        soup = BeautifulSoup(html, 'html.parser')
        self.assertTrue(has_login_form(soup))
    
    def test_has_login_form_has_textfield(self):
        html = """<!doctype html>
        <form action="http://example.com" method="post">
            <input type="text", name="question">
            <input type="submit", value="Submit">
        </form>
        """
        soup = BeautifulSoup(html, 'html.parser')
        self.assertFalse(has_login_form(soup))


class IsInternalLinkTests(TestCase):
    def test_is_internal_link_relative(self):
        link = "/faq"
        base_url = "http://example.com"
        self.assertTrue(is_internal_link(link, base_url)) 
    
    def test_is_internal_link_absolute_internal(self):
        link = "http://example.com/faq"
        base_url = "http://example.com"
        self.assertTrue(is_internal_link(link, base_url))
    
    def test_is_internal_link_external(self):
        link = "http://notinternal.com"
        base_url = "http://example.com"
        self.assertFalse(is_internal_link(link, base_url))

