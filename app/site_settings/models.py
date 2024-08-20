from django.db import models
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.snippets.models import register_snippet
from wagtail.models import BootstrapTranslatableMixin, TranslatableMixin
from wagtail.models import Orderable
from wagtail.fields import RichTextField
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)
from wagtail.admin.panels import FieldPanel, InlinePanel


@register_setting(icon="doc-full")
class CompanySettings(BaseGenericSetting):

    header_logo = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        help_text='Please upload an image with dimensions 250x50 pixels'
    )
        
    footer_logo = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        help_text='Please upload an image with dimensions 250x50 pixels'
    )
    footer_bg = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )

    address = RichTextField(features=['h2', 'h3', 'link'], blank=True, null=True)
    phone = models.CharField(_("Phone"), max_length=20, blank=True, null=True)
    email = models.CharField(_("Email"), max_length=100, blank=True, null=True)
    copyright = models.CharField(_("Copy Right"), max_length=100, blank=True, null=True)
    site_by = models.CharField(_("Site By"), max_length=100, blank=True, null=True)
    site_by_url = models.URLField(_("Site Creator's URL"), blank=True, null=True)


    panels = [
        FieldPanel("header_logo"),
        FieldPanel("footer_logo"),
        FieldPanel("footer_bg"),
        FieldPanel("address"),
        FieldPanel("phone"),
        FieldPanel("email"),
        FieldPanel("copyright"),
        FieldPanel("site_by"),
        FieldPanel("site_by_url")
    ]


@register_setting(icon="globe")
class SocialMediaSettings(ClusterableModel, BaseGenericSetting):
	panels = [
		InlinePanel('social_media_links', label="Social Media Links"),
	]

class SocialMediaLink(Orderable):
    setting = ParentalKey(
        SocialMediaSettings, on_delete=models.CASCADE, related_name='social_media_links')
    name = models.CharField(_("Name"), max_length=100)
    link = models.URLField(_("Link"), max_length=500)
    
    def save(self, *args, **kwargs):
        # Convert the 'name' field to lowercase
        self.name = self.name.lower()

        super(SocialMediaLink, self).save(*args, **kwargs)

    panels = [
        FieldPanel('name'),
        FieldPanel('link'),
    ]

@register_snippet
class CookieConsentSettings(TranslatableMixin):

    LANGUAGES = (
        ('en', 'English'),
        ('de', 'German')
	)

    content = RichTextField(blank=True, null=True)
    accept_btn_label = models.CharField(max_length=20, blank=True, null=True)
    reject_btn_label = models.CharField(max_length=20, blank=True, null=True)
    language = models.CharField(max_length=5, choices=LANGUAGES, default='en', help_text="Enter the language code")
    show_cookie_bar = models.BooleanField(default=True)

    panels = [
        FieldPanel('content'),
        FieldPanel('accept_btn_label'),
        FieldPanel('reject_btn_label'),
        FieldPanel("language"),
        FieldPanel('show_cookie_bar')
    ]

    def clean(self):
		# Check if a setting with the same language already exists
        existing_setting = CookieConsentSettings.objects.filter(language=self.language).exclude(pk=self.pk).first()
        if existing_setting:
            raise ValidationError(f"A Setting with language '{self.language}' already exists.")

    def __str__(self):
        return f"Cookie Consent-{self.language}"
    
    class Meta:
         verbose_name = "Cookie Consent Settings"
         verbose_name_plural = "Cookie Consent Settings"
         unique_together = ('translation_key', 'locale')