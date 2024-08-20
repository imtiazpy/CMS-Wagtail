from django.db import models
from wagtail.snippets.models import register_snippet

@register_snippet
class CarouselVideo(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    video = models.FileField(upload_to="video")

    def __str__(self):
        return f"{self.title}"

    