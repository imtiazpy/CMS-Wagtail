import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    BlockElementHandler,
    InlineStyleElementHandler,
)
from wagtail.admin.rich_text.editors.draftail.features import InlineStyleFeature


def register_block_feature(
    features,
    feature_name,
    description,
    type_,
    css_class,
    element="div",
    label=None,
    icon=None,
    editor_style=None,
):
    control = {
        "type": type_,
        "description": description,
        "element": element,
    }
    if label:
        control["label"] = label
    elif icon:
        control["icon"] = icon
    else:
        control["label"] = description
    if editor_style:
        control["style"] = editor_style

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.BlockFeature(
            control, css={"all": ["css/admin/draftail-editor.css"]}),
    )

    features.register_converter_rule(
        "contentstate",
        feature_name,
        {
            "from_database_format": {
                f"{element}[class={css_class}]": BlockElementHandler(type_)
            },
            "to_database_format": {
                "block_map": {
                    type_: {"element": element, "props": {"class": css_class}}
                }
            },
        },
    )
