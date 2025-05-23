# Generated by Django 5.2 on 2025-05-11 14:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classes", "0003_alter_fitnessclassimage_fitness_class"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fitnessclassimage",
            name="fitness_class",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="classes.fitnessclass",
            ),
        ),
    ]
