from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class ContentBlock(blocks.StructBlock):
    """Content block for pages"""
    heading = blocks.CharBlock(label="Heading", max_length=200, required=False)
    subheading = blocks.TextBlock(
        label="Sub heading", max_length=400, required=False)
    content = blocks.RichTextBlock(editor="default")

    class Meta:
        template = "streams/contents/content_block.html"
        icon = "draft"
        label = "Content"
        label_format = "{label}"


class TabContentItem(blocks.StructBlock):
    """block for items in the Tab Content block"""
    title = blocks.CharBlock(label="Title", max_length=100, required=False)
    text = blocks.TextBlock(label="Text", max_length=1000, required=False)
    image = ImageChooserBlock(required=False)

    def clean(self, value):
        cleaned = super().clean(value)
        if cleaned.get('title'):
            cleaned['title'] = cleaned['title'].replace(" ", "-")
        return cleaned

    class Meta:
        icon = "draft"
        label = "Content"
        label_format = "Content Item of Tab Content Block"


class TabContentBlock(blocks.StructBlock):
    """Tab Content block for Pages"""
    heading = blocks.CharBlock(label="Heading", max_length=200,
                               required=False, help_text="Main heading of tab section")
    content = blocks.ListBlock(TabContentItem(required=False), label="Content")

    class Meta:
        template = "streams/contents/tab_content_block.html"
        icon = "draft"
        label = "Tab Content"
        label_format = "{label}"


class AccordionItemBlock(blocks.StructBlock):
    """block for content list in Accordion Block"""
    title = blocks.CharBlock(label="Title", max_length=200, required=False)
    text = blocks.TextBlock(label="Text", required=False)
    image = ImageChooserBlock(required=False)

    class Meta:
        label = "Accordion Item"
        label_format = "Item Block of Accordion"


class AccordionBlock(blocks.StructBlock):
    """Accordion Block"""
    heading = blocks.CharBlock(max_length=200, required=False, help_text="Main Tab Heading")
    content = blocks.ListBlock(AccordionItemBlock(required=False))

    class Meta:
        template = "streams/contents/accordion_block.html"
        icon = "arrow-down"
        label = "Accordion"
        label_format = "{label}"
