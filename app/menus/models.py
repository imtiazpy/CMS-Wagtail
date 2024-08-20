from django.db import models
from django.core.exceptions import ValidationError
from wagtail.models import Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.snippets.models import register_snippet
from wagtail.models import BootstrapTranslatableMixin, TranslatableMixin


class SubMenuItem(Orderable):
    """Sub menu item for the Menu Item"""
    link_title = models.CharField(max_length=100)
    link_url = models.CharField(max_length=500, blank=True, null=True)
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
    )
    open_in_new_tab = models.BooleanField(default=False, blank=True)
    
    parent_menu_item = ParentalKey("MenuItem", related_name="sub_menu_items", on_delete=models.CASCADE, blank=True, null=True)

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        FieldPanel("link_page"),
        FieldPanel("open_in_new_tab"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return '#'

    @property
    def title(self):
        return self.link_title
    

class MenuItem(ClusterableModel):

    link_title = models.CharField(
        blank=True,
        null=True,
        max_length=50
    )
    link_url = models.CharField(
        max_length=500,
        blank=True
    )
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
    )
    open_in_new_tab = models.BooleanField(default=False, blank=True)
    is_hovered = models.BooleanField(default=False, blank=True)
    position = models.PositiveIntegerField(default=0)

    page = ParentalKey("Menu", related_name="menu_items", on_delete=models.CASCADE, blank=True, null=True)
    quick_page = ParentalKey("QuickMenu", related_name="quick_menu_items", on_delete=models.CASCADE, blank=True, null=True)

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        FieldPanel("link_page"),
        FieldPanel("open_in_new_tab"),
        FieldPanel("is_hovered"),
        FieldPanel("position"),
        InlinePanel("sub_menu_items", label="Sub Menu Items"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return '#'

    @property
    def title(self):
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return 'Missing Title'
    



@register_snippet
class Menu(TranslatableMixin, ClusterableModel):
    """The main menu clusterable model."""
    
    MENU_TYPES = (
		('main', 'Main Menu'),
		('footer', 'Footer Menu'),
        ('bottom', 'Bottom Menu')
	)
    LANGUAGES = (
        ('en', 'English'),
        ('de', 'German')
	)

    menu_type = models.CharField(max_length=10, choices=MENU_TYPES, default='main', help_text="Select the type of menu")
    language = models.CharField(max_length=5, choices=LANGUAGES, default='en', help_text="Enter the language code")

    panels = [
        MultiFieldPanel([
            FieldPanel("menu_type"),
            FieldPanel("language")
        ], heading="Menu"),
        InlinePanel("menu_items", label="Menu Item")
    ]
    
    def clean(self):
		# Check if a menu with the same type and language already exists
        existing_menu = Menu.objects.filter(menu_type=self.menu_type, language=self.language).exclude(pk=self.pk).first()
        if existing_menu:
            raise ValidationError(f"A menu with type '{self.menu_type}' and language '{self.language}' already exists.")

    def __str__(self):
        return f"{self.menu_type}-{self.language}"
    
# ==============================Quick Menu Specific==============================

@register_snippet
class QuickMenu(TranslatableMixin, ClusterableModel):
    """Quick Menu clusterable model"""
    LANGUAGES = (
        ('en', 'English'),
        ('de', 'German')
	)
    language = models.CharField(max_length=5, choices=LANGUAGES, default='en', help_text="Enter the language code")

    panels = [
        FieldPanel('language'),
        InlinePanel("quick_menu_items", label="Quick Menu Item")
    ]

    def clean(self):
		# Check if a menu with the same type and language already exists
        existing_menu = QuickMenu.objects.filter(language=self.language).exclude(pk=self.pk).first()
        if existing_menu:
            raise ValidationError(f"A menu with language '{self.language}' already exists.")

    def __str__(self):
        return f"Quick Menu-{self.language}"
