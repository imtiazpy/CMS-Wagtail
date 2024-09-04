from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import get_language
from django import forms
from django.db.models import Q
from wagtail.models import Page, TranslatableMixin, Locale
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from core.translations import TranslatablePageMixin



class NewsIndex(TranslatablePageMixin, Page):

	parent_page_types = [
    	'home.HomePage',
			'home.UniversalPage'
  	]

	subpage_types = [
		'news.News'
	]

	template = 'news/news_index.html'

	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request)
		current_language = get_language()
		current_locale = Locale.objects.get(language_code = current_language)
		categories = NewsCategory.objects.filter(locale=current_locale)

		news = News.objects.child_of(self).live()
		# Get the selected category from the request (if any)
		selected_category = request.GET.get('category')
		search_query = request.GET.get('search')

		if selected_category:
			if selected_category == 'all':
				pass
			else:
				try:
					category = NewsCategory.objects.get(name=selected_category)
					news = category.category_news.filter(locale=current_locale)
				except NewsCategory.DoesNotExist:
					news = NewsCategory
		
		if search_query:
			try:
				news = news.filter(
        	Q(headline__icontains=search_query) | Q(content__icontains=search_query),
					locale=current_locale
    		).distinct()
			except News.DoesNotExist:
				news = News.objects.none()
		
		context['news'] = news
		context['categories'] = categories
		context['selected_category'] = selected_category
		return context

@register_snippet
class NewsCategory(TranslatableMixin):
	name = models.CharField(_("Name"), max_length=100, unique=True)
  
	panels = [
		FieldPanel('name')
	]

	def __str__(self):
		return self.name

	class Meta(TranslatableMixin.Meta):
		verbose_name_plural = 'News Categories'


class News(TranslatablePageMixin, Page):
	parent_page_types = [
		'news.NewsIndex'
	]
	subpage_types = []
	template = 'news/news.html'

	headline = models.CharField(_("Headline"), max_length=500)
	banner_image = models.ForeignKey(
		'wagtailimages.Image',
		on_delete=models.SET_NULL,
		null=True,
		related_name='+'
	)
	created_at = models.DateField(_("Created at"), auto_now=True)
	content = RichTextField(_("Content"), blank=True, null=True)
	categories = ParentalManyToManyField(
		NewsCategory, 
		blank=True, 
		related_name="category_news",
		help_text="Select any category or create one from the snippet"
	)

	content_panels = Page.content_panels + [
		FieldPanel('headline'),
		FieldPanel('banner_image'),
		FieldPanel('content'),
		FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
	]

	class Meta:
		verbose_name = 'News'
		verbose_name_plural = 'News'
