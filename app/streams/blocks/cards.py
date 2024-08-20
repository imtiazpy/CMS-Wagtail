from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from news.models import News
from .common import LinkStructValue, BaseWidthBlock, BaseLinkBlock


"""
1. News Card
2. Classic Card
3. Sliding Card
"""


class NewsCardItem(blocks.StructBlock):
    page = blocks.PageChooserBlock(page_type=News, required=False)

    class Meta:
        label = "Card Item"
        label_format = "{label}"

class NewsCardBlock(BaseWidthBlock):
    heading = blocks.CharBlock(
        label="Heading", 
        max_length=200, 
        required=False, 
    )
    cards = blocks.ListBlock(NewsCardItem(required=False))

    class Meta:
        template = "streams/cards/news_card_block.html"
        icon = "info-circle"
        label = "News card"
        label_format = "{label}"




class ClassicCardItem(BaseLinkBlock):
    banner_image = ImageChooserBlock(required=False)
    heading = blocks.CharBlock(label="Heading", max_length=100, required=False)
    text = blocks.TextBlock(label="Text", max_length=400, required=False)
    
    class Meta:
        value_class = LinkStructValue
        label = "Classic Card Item"
        label_format = "{label}"

class ClassicCardBlock(BaseWidthBlock):
    cards = blocks.ListBlock(ClassicCardItem(required=False))

    class Meta:
        template = "streams/cards/classic_card_block.html"
        icon = "folder-inverse"
        label = "Classic Card"
        label_format = "{label}"




class SlidingCardItem(BaseLinkBlock):
    """For body of the card block"""
    image = ImageChooserBlock(required=False)
    title = blocks.CharBlock(label="Title", max_length=200, required=False)
    content = blocks.TextBlock(required=False, help_text="Content of the card")

    class Meta:
        value_class = LinkStructValue
        label = "Sliding Card Item"
        label_format = "{label}"

class SlidingCardBlock(BaseWidthBlock):
    """Slide up card block"""

    body = blocks.ListBlock(SlidingCardItem(required=False))

    class Meta:
        template = "streams/cards/sliding_card_block.html"
        icon = "link-external"
        label = "Sliding Card"
        label_format = "{label}"