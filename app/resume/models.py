from django.db import models
from django.utils.translation import gettext as _
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from streams.blocks.info import SimpleInformationBlock, SimpleInformationWithImageBlock, TimelineInformationBlock


class ResumePage(Page):
    """Page model for a resume page"""

    parent_page_types = [
        'home.HomePage',
        'home.UniversalPage'
    ]

    name = models.CharField(_("Name"), max_length=100, blank=True, null=True)

    content = StreamField(
        [
            ("simple_information", SimpleInformationBlock()),
            ("simple_information_with_image", SimpleInformationWithImageBlock()),
            ("timeline_information", TimelineInformationBlock())
        ],
        null=True,
        blank=True,
        use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('content')
    ]

    class Meta:
        verbose_name = "Resume page"
        verbose_name_plural = "Resume pages"

    
