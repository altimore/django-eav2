# Generated by Django 5.1.2 on 2024-11-20 10:52

from django.db import connection, migrations


def set_enumvalue_id_sequence(apps, schema_editor):
    with connection.cursor() as cursor:
        if connection.vendor == "postgresql":
            cursor.execute(
                "SELECT setval(pg_get_serial_sequence('eav_enumvalue', 'id'), 100, false);"
            )


class Migration(migrations.Migration):

    dependencies = [
        ("eav", "0013_alter_enumvalue_id"),
    ]

    operations = [
        migrations.RunPython(set_enumvalue_id_sequence),
    ]
