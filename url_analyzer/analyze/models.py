from django.db import models
from django.utils import timezone

import datetime


class Website(models.Model):
    url = models.URLField(max_length=1000)
    time_cached = models.DateTimeField()

    # Only allow these common DOCTYPE declarations
    HTML5 = "5"
    HTML4_STRICT = "4S"
    HTML4_TRANSITIONAL = "4T"
    HTML4_FRAMESET = "4F"
    XHTML1_STRICT = "X1S"
    XHTML1_TRANSITIONAL = "X1T"
    XHTML1_FRAMESET = "X1F"
    XHTML1_1 = "X1_1"
    HMTL_UNKNOWN = "Unknown"

    HTML_VERSION_CHOICES = (
        (HTML5, "HTML5"),
        (HTML4_STRICT, "HTML 4.01 Strict"),
        (HTML4_TRANSITIONAL, "HTML 4.01 Transitional"),
        (HTML4_FRAMESET, "HTML 4.01 Frameset"),
        (XHTML1_STRICT, "XHTML 1.0 Strict"),
        (XHTML1_TRANSITIONAL, "HTML 1.0 Transitional"),
        (XHTML1_FRAMESET, "XHTML 1.0 Frameset"),
        (XHTML1_1, "XHTML 1.1"),
        (HMTL_UNKNOWN, "Unknown"),
    )
    html_version = models.CharField(
        max_length=7,
        choices=HTML_VERSION_CHOICES,
        default=HMTL_UNKNOWN,
    )

    title = models.CharField(max_length=1000)

    h1s = models.PositiveIntegerField()
    h2s = models.PositiveIntegerField()
    h3s = models.PositiveIntegerField()
    h4s = models.PositiveIntegerField()
    h5s = models.PositiveIntegerField()
    h6s = models.PositiveIntegerField()

    links_internal = models.PositiveIntegerField()
    links_external = models.PositiveIntegerField()
    links_inaccessible = models.PositiveIntegerField()

    has_login = models.BooleanField()

    def is_recent(self):
        """Returns true if the website analysis was cached in the
        past 24 hours."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.time_cached <= now





