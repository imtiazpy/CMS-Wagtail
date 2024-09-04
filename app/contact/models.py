from os.path import splitext
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.html import format_html
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.translation import get_language
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.forms import FileField
from wagtail.models import Collection, TranslatableMixin
from wagtail.snippets.models import register_snippet
from wagtail.fields import StreamField
from wagtail.images.fields import WagtailImageField
from wagtail.images import get_image_model
from wagtail.documents import get_document_model
from wagtail.admin.panels import (
    InlinePanel,
    FieldPanel,
)

from wagtailcaptcha.models import WagtailCaptchaForm
from wagtailcaptcha.forms import WagtailCaptchaFormBuilder
from wagtail.contrib.forms.models import AbstractFormField, FORM_FIELD_CHOICES
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.views import SubmissionsListView
from modelcluster.fields import ParentalKey

from streams.blocks.banners import BannerCaptionBlock
from streams.blocks.contents import ContentBlock, TabContentBlock, AccordionBlock
from streams.blocks.gallery import GalleryBlock
from core.translations import TranslatablePageMixin


class ExtendedFormBuilder(WagtailCaptchaFormBuilder):
    def create_image_field(self, field, options):
        return WagtailImageField(**options)

    def create_document_field(self, field, options):
        return FileField(**options)
    

class CustomSubmissionsListView(SubmissionsListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.is_export:
            # generate a list of field types, the first being the injected 'submission date'
            field_types = ['submission_date'] + [field.field_type for field in self.form_page.get_form_fields()]
            data_rows = context['data_rows']

            ImageModel = get_image_model()
            DocumentModel = get_document_model()

            for data_row in data_rows:

                fields = data_row['fields']

                for idx, (value, field_type) in enumerate(zip(fields, field_types)):
                    if field_type == 'image' and value:
                        image = ImageModel.objects.get(pk=value)
                        rendition = image.get_rendition('fill-100x75|jpegquality-40')
                        preview_url = rendition.url
                        url = reverse('wagtailimages:edit', args=(image.id,))
                        # build up a link to the image, using the image title & id
                        fields[idx] = format_html(
                            "<a href='{}'><img alt='Uploaded image - {}' src='{}' />{} ({})</a>",
                            url,
                            image.title,
                            preview_url,
                            image.title,
                            value
                        )
                    elif field_type == 'document' and value:
                        document = DocumentModel.objects.get(pk=value)
                        document_url = document.url
                        document_title = document.title
                        fields[idx] = format_html(
                            "<a href='{}'>{}</a>",
                            document_url,
                            document_title
                        )


        return context



class ContactPage(TranslatablePageMixin, WagtailCaptchaForm):
    parent_page_types = [
        'home.HomePage',
        'home.UniversalPage'
    ]

    subpage_types = []

    form_builder = ExtendedFormBuilder
    submissions_list_view_class = CustomSubmissionsListView

    template = 'contact/contact_page.html'

    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )

    banner_caption = StreamField(
        [("BannerCaption", BannerCaptionBlock())],
        null=True,
        blank=True,
        use_json_field=True
    )

    content = StreamField(
        [("content", ContentBlock())],
        null=True,
        blank=True,
        use_json_field=True
    )

    tab_content = StreamField(
        [("tab_content", TabContentBlock())],
        blank=True,
        null=True,
        use_json_field=True
    )

    image_gallery = StreamField(
        [
            ("image_gallery", GalleryBlock())
        ],
        null=True,
        blank=True,
        use_json_field=True
    )

    accordion = StreamField(
        [
            ("accordion", AccordionBlock())
        ],
        null=True,
        blank=True,
        use_json_field=True
    )

    uploaded_image_collection = models.ForeignKey(
        'wagtailcore.Collection',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    contact_form_title = models.CharField(max_length=20, blank=True, null=True)

    content_panels = WagtailCaptchaForm.content_panels + [
        FieldPanel('banner_image'),
        FieldPanel('banner_caption'),
        FieldPanel('content'),
        FieldPanel('tab_content'),
        FieldPanel('image_gallery'),
        FieldPanel('accordion'),
        FieldPanel('contact_form_title'),
        InlinePanel('form_fields', label='Form Fields For Contact')
    ]

    settings_panels = WagtailCaptchaForm.settings_panels + [
        FieldPanel('uploaded_image_collection')
    ]


    @staticmethod
    def get_file_title(filename):
        if filename:
            result = splitext(filename)[0]
            result = result.replace('-', ' ').replace('_', ' ')
            return result.title()
        return ''

    def get_uploaded_image_collection(self):
        collection = self.uploaded_image_collection
        return collection or Collection.get_first_root_node()

    def process_form_submission(self, form):

        cleaned_data = form.cleaned_data

        for name, field in form.fields.items():
            if isinstance(field, WagtailImageField):
                image_file_data = cleaned_data[name]
                if image_file_data:
                    ImageModel = get_image_model()

                    kwargs = {
                        'file': cleaned_data[name],
                        'title': self.get_file_title(cleaned_data[name].name),
                        'collection': self.get_uploaded_image_collection(),
                    }

                    if form.user and not form.user.is_anonymous:
                        kwargs['uploaded_by_user'] = form.user

                    image = ImageModel(**kwargs)
                    image.save()
                    cleaned_data.update({name: image.pk})
                else:
                    del cleaned_data[name]

            elif isinstance(field, FileField):
                file_data = cleaned_data[name]
                if file_data:
                    DocumentModel = get_document_model()
                    kwargs = {
                        'file': cleaned_data[name],
                        'title': self.get_file_title(cleaned_data[name].name),
                        # 'collection': self.get_uploaded_image_collection(),
                    }

                    if form.user and not form.user.is_anonymous:
                        kwargs['uploaded_by_user'] = form.user

                    document = DocumentModel(**kwargs)
                    document.save()
                    cleaned_data.update({name: document.pk})
                else:
                    del cleaned_data[name]


        submission = self.get_submission_class().objects.create(
            form_data=form.cleaned_data,
            page=self,
        )

        html_message = render_to_string('contact/email_template.html', {'form_data': cleaned_data})
        send_mail(
            'Contact Form: New Submission',
            strip_tags(html_message),
            settings.FROM_EMAIL,
            settings.RECIPIENT_LIST,
            html_message=html_message,
            fail_silently=False,
        )

        return submission
    
    class Meta:
        verbose_name = "Contact Page"
        verbose_name_plural = "Contact pages"


class ContactForm(AbstractFormField):
    """Fields to render in the Contact form"""
    FORM_FIELD_CHOICES = list(FORM_FIELD_CHOICES) + [('image', 'Upload Image'), ('document', 'Upload Document')]
    field_type = models.CharField(verbose_name=_('field type'), max_length=16, choices=FORM_FIELD_CHOICES)

    page = ParentalKey(ContactPage, on_delete=models.CASCADE, related_name='form_fields')


@register_snippet
class StickyContactLink(TranslatableMixin):
    """
    Snippet to add a sticky contact link floating on the page
    sticky contact link can be created for all the languages available
    """

    LANGUAGES = (
        ('en', 'English'),
        ('de', 'German')
    )
    page = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="+"
    )
    language = models.CharField(max_length=5, choices=LANGUAGES, default='en', help_text="Enter the language code")

    panels = [
        FieldPanel('page'),
        FieldPanel('language')
    ]

    def clean(self):
        # Check if a Sticky Link with the same language already exists
        existing_sticky_link = StickyContactLink.objects.filter(language=self.language).exclude(pk=self.pk).first()
        if existing_sticky_link:
            raise ValidationError(f"A Sticky Link with language '{self.language}' already exists.")

    def __str__(self):
        return f"{self.page.title}-{self.language}"
