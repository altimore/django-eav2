# Generated by Django 5.1.2 on 2024-11-20 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eav", "0012_alter_attribute_id_alter_enumgroup_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="enumvalue",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
