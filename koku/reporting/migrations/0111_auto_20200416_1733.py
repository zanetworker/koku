# Generated by Django 2.2.11 on 2020-04-16 17:33
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("reporting", "0110_summary_indexes")]

    operations = [
        migrations.AddField(
            model_name="ocpawscostlineitemprojectdailysummary",
            name="markup_cost",
            field=models.DecimalField(decimal_places=15, max_digits=30, null=True),
        ),
        migrations.AddField(
            model_name="ocpazurecostlineitemprojectdailysummary",
            name="markup_cost",
            field=models.DecimalField(decimal_places=9, max_digits=17, null=True),
        ),
    ]
