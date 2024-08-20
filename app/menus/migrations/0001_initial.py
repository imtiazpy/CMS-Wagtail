# Generated by Django 5.0 on 2024-05-19 13:31

import django.db.models.deletion
import modelcluster.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0091_remove_revision_submitted_for_moderation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translation_key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('menu_type', models.CharField(choices=[('main', 'Main Menu'), ('footer', 'Footer Menu'), ('bottom', 'Bottom Menu')], default='main', help_text='Select the type of menu', max_length=10)),
                ('language', models.CharField(choices=[('en', 'English'), ('de', 'German')], default='en', help_text='Enter the language code', max_length=5)),
                ('locale', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.locale')),
            ],
            options={
                'abstract': False,
                'unique_together': {('translation_key', 'locale')},
            },
        ),
        migrations.CreateModel(
            name='QuickMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translation_key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('language', models.CharField(choices=[('en', 'English'), ('de', 'German')], default='en', help_text='Enter the language code', max_length=5)),
                ('locale', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.locale')),
            ],
            options={
                'abstract': False,
                'unique_together': {('translation_key', 'locale')},
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_title', models.CharField(blank=True, max_length=50, null=True)),
                ('link_url', models.CharField(blank=True, max_length=500)),
                ('open_in_new_tab', models.BooleanField(blank=True, default=False)),
                ('is_hovered', models.BooleanField(blank=True, default=False)),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.page')),
                ('page', modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='menus.menu')),
                ('quick_page', modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quick_menu_items', to='menus.quickmenu')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubMenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_title', models.CharField(max_length=100)),
                ('link_url', models.CharField(blank=True, max_length=500, null=True)),
                ('open_in_new_tab', models.BooleanField(blank=True, default=False)),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.page')),
                ('parent_menu_item', modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_menu_items', to='menus.menuitem')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
