import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler
from wagtail import hooks

from .draftail_extensions import register_block_feature


@hooks.register('register_rich_text_features')
def register_button_primary(features):
    register_block_feature(
        features=features,
        feature_name='buttons',
        type_='BUTTONS',
        description='Buttons',
        css_class='buttons-block',
        element='p',
        icon='tag',
    )
