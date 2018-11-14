from django.db import models
from django.utils import timezone


class Website(models.Model):
    url = models.URLField(max_length=1000)
    time_cached = models.DateTimeField()

    # Only allow HTML version to be 5, 4, or unknown
    HTML5 = "5"
    HTML4 = "4"
    HMTL_UNKNOWN = "Unknown"
    HTML_VERSION_CHOICES = (
        (HTML5, "HTML5"),
        (HTML4, "HTML 4.01 Strict"),
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
        return self.time_cached >= timezone.now() - datetime.timedelta(days=1)





