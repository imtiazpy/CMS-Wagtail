from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

class SimpleInformation(blocks.StructBlock):
    info_type = blocks.ChoiceBlock(
        choices=[('text', 'Text'), ('contact_number', 'Contact Number'), ('email', 'Email')], 
        required=False, 
        default='text', 
        help_text='Select what type of info you are adding'
    )
    info = blocks.CharBlock(label="Info", max_length=200, required=False)

    class Meta:
        label = "Simple Information Item"
        label_format = "{label}"


class SimpleInformationWithImageBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Heading", max_length=200, required=False)
    information = blocks.ListBlock(SimpleInformation(required=False))
    image = ImageChooserBlock(required=False)

    class Meta:
        template = "streams/info/simple_information_with_image_block.html"
        icon = "info-circle"
        label = "Simple Information With Image"
        label_format = "{label}"

class SimpleInformationBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Heading", max_length=200, required=False)
    information = blocks.ListBlock(SimpleInformation(required=False))

    class Meta:
        template = "streams/info/simple_information_block.html"
        icon = "info-circle"
        label = "Simple Information"
        label_format = "{label}"






class SubInfo(blocks.StructBlock):
    info = blocks.CharBlock(label="Info", max_length=200, required=False)

    class Meta:
        label = "Sub Info"
        label_format = "{label}"

class TimelineInformation(blocks.StructBlock):
    timeline = blocks.CharBlock(label="Timeline", max_length=15, required=False)
    heading_info = blocks.CharBlock(label="Heading Info", max_length=200, required=False)
    sub_info = blocks.ListBlock(SubInfo(required=False))

    class Meta:
        label = "Timeline Information Item"
        label_format = "{label}"


class TimelineInformationBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Heading", max_length=200, required=False)

    information = blocks.ListBlock(TimelineInformation(required=False))

    class Meta:
        template= "streams/info/timeline_information_block.html"
        icon = "info-circle"
        label = "Timeline Information"
        label_format = "{label}"



