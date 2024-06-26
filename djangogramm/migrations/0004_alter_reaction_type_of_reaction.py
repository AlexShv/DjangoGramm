# Generated by Django 4.2.5 on 2023-09-29 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangogramm', '0003_rename_followed_user_id_follow_followed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reaction',
            name='type_of_reaction',
            field=models.PositiveIntegerField(choices=[(1, '👍'), (2, '👎'), (3, '💖'), (4, '😠'), (5, '🤢'), (6, '👽'), (7, '🌝')], help_text='Reaction for the post'),
        ),
    ]
