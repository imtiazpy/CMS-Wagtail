from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from .common import LinkStructValue, BaseLinkBlock


class RandomQuoteItem(blocks.StructBlock):
    quote = blocks.TextBlock(label="Quote", max_length=1000, required=False)
    author = blocks.CharBlock(label="Author", max_length=100, required=False)

    class Meta:
        label = "Random Quote Item"
        label_format = "{label}"


class RandomQuoteBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Heading", max_length=200, required=False, help_text="Heading for the quote section")
    items = blocks.ListBlock(RandomQuoteItem(required=False))

    class Meta:
        template = "streams/quotes/random_quote_block.html"
        icon = "openquote"
        label = "Random Quote"
        label_format = "{label}"



class PersonQuoteBlock(BaseLinkBlock):
    quote = blocks.TextBlock(label="Quote", max_length=1000, required=False)
    author_photo = ImageChooserBlock(required=False)
    author_name = blocks.CharBlock(label="Author name", max_length=100, required=False)
    author_speciality = blocks.CharBlock(label="Author specialty", max_length=100, required=False)
    contact = blocks.CharBlock(label="Contact", max_length=20, required=False)
    btn_label = blocks.CharBlock(max_length=20, required=False, help_text="Text to show on button")

    class Meta:
        template = "streams/quotes/person_quote_block.html"
        icon = "openquote"
        label = "Person Quote"
        value_class = LinkStructValue
        label_format = "{label}"