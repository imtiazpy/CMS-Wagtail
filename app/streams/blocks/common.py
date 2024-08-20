from wagtail import blocks

class BaseWidthBlock(blocks.StructBlock):
    block_width = blocks.ChoiceBlock(
        choices=[('fluid', 'Fluid'), ('container', 'Container')], 
        required=False, 
        default='fluid', 
        help_text='Selecting container will add space around the section, Fluid will fit the section to the horizontal edges'
    )


class BaseLinkBlock(blocks.StructBlock):
    link_page = blocks.PageChooserBlock(required=False)
    link_url = blocks.URLBlock(label="external URL", required=False)


class LinkStructValue(blocks.StructValue):
    """For adding as value_class in blocks with link_url and link_page fields"""

    def url(self):
        link_url = self.get('link_url')
        link_page = self.get('link_page')

        return {
            'src': link_page.url if link_page else link_url or '#',
            'open_in_new': bool(link_url) and not link_page
        }
