# Generated by Django 5.2 on 2025-04-13 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_feedback_feedback_type_like_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
