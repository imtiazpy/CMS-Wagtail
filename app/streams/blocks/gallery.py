from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from .common import BaseWidthBlock, BaseLinkBlock, LinkStructValue

class GalleryImage(blocks.StructBlock):
    """image for Gallery block"""
    image = ImageChooserBlock(required=False)
    title = blocks.CharBlock(label="Title", max_length=100, required=False)
    caption = blocks.CharBlock(label="Caption", max_length=150, required=False)

    class Meta:
        label = "Gallery Image"
        label_format = "{label}"


class GalleryBlock(BaseWidthBlock, BaseLinkBlock):
    """Image gallery for pages"""
    heading = blocks.CharBlock(label="Heading", max_length=200, required=False)
    gallery_mode = blocks.ChoiceBlock(
        choices=[('grid', 'Grid'), ('slider', 'Slider'), ('split', 'Split')],
        default='grid',
        required=False,
        help_text="Choose the layout for the gallery"
    )
    content = blocks.TextBlock(label="Content", required=False, help_text="Add content for the Split gallery mode")
    btn_label = blocks.CharBlock(label="Label", max_length=20, required=False, help_text="Text to show on the button")
    images = blocks.ListBlock(GalleryImage(required=False))

    class Meta:
        icon = "image"
        label = "Gallery"
        value_class = LinkStructValue
        label_format = "{label}"

    def render(self, value, context=None):
        if value['gallery_mode'] == 'grid':
            template = "streams/gallery/grid_gallery_block.html"
        elif value['gallery_mode'] == 'slider':
            template = "streams/gallery/slider_gallery_block.html"
        elif value['gallery_mode'] == 'split':
            template = "streams/gallery/split_gallery_block.html"
        
        template_context = self.get_context(value, parent_context=context)
        return mark_safe(render_to_string(template, template_context))