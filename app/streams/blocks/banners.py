from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.snippets.blocks import SnippetChooserBlock


from .common import LinkStructValue, BaseLinkBlock
from streams.models import CarouselVideo


class BannerCaptionBlock(BaseLinkBlock):
    """Fixed Caption block for pages"""

    title = blocks.CharBlock(label="Title", max_length=100, required=False)
    text = blocks.TextBlock(label="Text", max_length=200, required=False)
    btn_label = blocks.CharBlock(label="Btn label", max_length=20, required=False, help_text="Text to show on button")

    class Meta:
        template = "streams/banners/banner_caption_block.html"
        icon = "link-external"
        label = "Banner Caption"
        value_class = LinkStructValue
        label_format = "{label}"



class CarouselImage(blocks.StructBlock):
    image = ImageChooserBlock(required=True)

    class Meta:
        icon = "image"
        label = "Image"
        label_format = "{label}"


class CarouselVideoEmbedBlock(blocks.StructBlock):
    """Video embed for the header carousel"""
    video = EmbedBlock(max_width=1920, max_height=697)
    class Meta:
        icon = "media"
        label = "Embed"
        label_format = "{label}"



class CarouselVideoBlock(blocks.StructBlock):
    """Video upload for the header carousel"""
    video = SnippetChooserBlock(target_model=CarouselVideo, required=False)

    class Meta:
        label = "Video"
        label_format = "{label}"


class HeaderCarouselBlock(blocks.StructBlock):
    carousel_items = blocks.StreamBlock(
        [
            ('image', CarouselImage(required=False)),
            ('embed', CarouselVideoEmbedBlock(required=False)),
            ('media', CarouselVideoBlock(required=False)),
        ]
    )

    class Meta:
        template = "streams/banners/header_carousel_block.html"
        icon = "media"
        label = "Header Carousel"
        label_format = "{label}"