import os
from django.db import models
from django.utils.translation import gettext as _
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import (
    FieldPanel,
    TabbedInterface,
    TitleFieldPanel,
    ObjectList
)

from streams.blocks.cards import NewsCardBlock, ClassicCardBlock, SlidingCardBlock
from streams.blocks.contents import ContentBlock, TabContentBlock, AccordionBlock
from streams.blocks.sections import FlexBlock, BlueSectionBlock, LogoSectionBlock
from streams.blocks.quotes import RandomQuoteBlock, PersonQuoteBlock
from streams.blocks.banners import BannerCaptionBlock, HeaderCarouselBlock
from streams.blocks.gallery import GalleryBlock
from core.translations import TranslatablePageMixin

class HomePage(TranslatablePageMixin, Page):
    """Home page Definition for the Root of the site, all pages will be under this page"""
    
    max_count = 1
    header_carousel = StreamField(
        [('carousel', HeaderCarouselBlock()),],
        block_counts = {
            'carousel': {'max_num': 1}
        },
        null=True,
        blank=True
    )
    banner_caption = StreamField(
        [("banner_caption", BannerCaptionBlock())],
        block_counts = {
            'banner_caption': {'max_num': 1}
        },
        null=True,
        blank=True,
        use_json_field=True
    )
    content = StreamField(
        [
            ("content", ContentBlock()),
            ("tab_content", TabContentBlock()),
            ("news_card", NewsCardBlock()),
            ('classic_card', ClassicCardBlock()),
            ("sliding_card", SlidingCardBlock()),
            ("flex", FlexBlock()),
            ("blue_section", BlueSectionBlock()),
            ("image_gallery", GalleryBlock()),
            ("accordion", AccordionBlock()),
            ("random_quote", RandomQuoteBlock()),
            ('logo_section', LogoSectionBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True
    )

    person_quote = StreamField(
        [("person_quote", PersonQuoteBlock()),],
        block_counts = {
            'person_quote': {'max_num': 1}
        },
        null=True,
        blank=True
    )

    content_panels = [
        TitleFieldPanel('title', classname='title'),
        FieldPanel('content'),
        FieldPanel('person_quote')
    ]

    banner_panels = [
        FieldPanel('header_carousel'),
        FieldPanel('banner_caption')
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Content"),
        ObjectList(banner_panels, heading="Banner"),
        ObjectList(Page.promote_panels, heading="Publication")
    ])

    class Meta:
        verbose_name = "Home page"
        verbose_name_plural = "Home pages"


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        context['PID'] = os.getpid()
        return context



class UniversalPage(TranslatablePageMixin, Page):
    """Model for universal page"""
    parent_page_types = [
        'home.HomePage',
        'home.UniversalPage'
    ]

    subpage_types = [
        'home.UniversalPage',
        'resume.ResumePage',
        'contact.ContactPage',
        'news.NewsIndex',
    ]

    template = "home/universal_page.html"

    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )

    banner_caption = StreamField(
        [("banner_caption", BannerCaptionBlock())],
        block_counts = {
            'banner_caption': {'max_num': 1}
        },
        null=True,
        blank=True,
        use_json_field=True
    )

    content = StreamField(
        [
            ("content_block", ContentBlock()),
            ("news_card", NewsCardBlock()),
            ('classic_card', ClassicCardBlock()),
            ("sliding_card", SlidingCardBlock()),
            ("flex", FlexBlock()),
            ("blue_section", BlueSectionBlock()),
            ("tab_content", TabContentBlock()),
            ("image_gallery", GalleryBlock()),
            ("accordion", AccordionBlock()),
            ("random_quote", RandomQuoteBlock()),
            ('logo_section', LogoSectionBlock()),
        ],
        blank=True,
        null=True,
        use_json_field=True
    )

    person_quote = StreamField(
        [("person_quote", PersonQuoteBlock()),],
        block_counts = {
            'person_quote': {'max_num': 1}
        },
        null=True,
        blank=True
    )

    content_panels = [
        TitleFieldPanel('title', classname='title'),
        FieldPanel('content'),
        FieldPanel('person_quote')
    ]

    banner_panels = [
        FieldPanel('banner_image'),
        FieldPanel('banner_caption')
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Content"),
        ObjectList(banner_panels, heading="Banner"),
        ObjectList(Page.promote_panels, heading="Publication")
    ])


    class Meta:
        verbose_name = "Universal page"
        verbose_name_plural = "Universal pages"



