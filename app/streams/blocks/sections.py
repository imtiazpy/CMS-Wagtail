from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from .common import LinkStructValue, BaseWidthBlock, BaseLinkBlock

class FlexBlock(BaseWidthBlock, BaseLinkBlock):
    """Flex block for pages"""
    heading = blocks.CharBlock(label="Heading", max_length=200, required=False)
    subheading = blocks.TextBlock(label="Subheading", max_length=400, required=False)
    content = blocks.RichTextBlock(label="Content", required=False)
    image = ImageChooserBlock(required=False)
    image_position = blocks.ChoiceBlock(
        choices=[('left', 'Left'), ('right', 'Right')], 
        required=False, 
        default='left', 
        help_text="Image rendering position, left or right"
    )
    content_display_mode = blocks.ChoiceBlock(
        choices=[('normal', 'Normal'), ('overlay', 'Overlay')],
        required=False,
        default='normal',
        help_text="Choose Overlay for showing the content over the image, default:Normal"
    )
    btn_label = blocks.CharBlock(label="Label", max_length=20, required=False, help_text="Text to show on the button")

    class Meta:
        template = "streams/sections/flex_block.html"
        icon = "folder"
        label = "Flex Block"
        value_class = LinkStructValue
        label_format = "{label}"



class BlueSectionBlock(BaseWidthBlock, BaseLinkBlock):
    """A section block with blue background"""
    image = ImageChooserBlock(required=False)
    heading = blocks.CharBlock(label="Heading", max_length=200, required=False)
    subheading = blocks.TextBlock(label="Subheading", max_length=400, required=False)
    btn_label = blocks.CharBlock(label="Label", max_length=20, required=False, help_text="Text to show on the button")

    class Meta:
        template = "streams/sections/blue_section_block.html"
        icon = "mobile-alt"
        label = "Blue Section"
        value_class = LinkStructValue
        label_format = "{label}"



class LogoItem(BaseLinkBlock):
    logo = ImageChooserBlock(required=False)

    class Meta:
        icon = "image"
        label = "Logo"
        value_class = LinkStructValue
        label_format = "{label}"

class LogoSectionBlock(BaseWidthBlock):
    grayscale = blocks.BooleanBlock(label="Grayscale", default=False, required=False, help_text="To show the logo in grayscale or black and white")
    logo_items = blocks.ListBlock(LogoItem(required=False))

    class Meta:
        template = "streams/sections/logo_section_block.html"
        icon = "info-circle"
        label = "Logo Section"
        label_format = "{label}"