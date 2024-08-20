from django.http import JsonResponse
from django.views import View
from wagtail.contrib.forms.views import FormPagesListView

from contact.models import ContactPage



class ContactPageView(FormPagesListView):
    """It's in use now"""
    page_class = ContactPage