from django.db import migrations


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.RunSQL(
            sql="CREATE SCHEMA IF NOT EXISTS proxy_service;",
            reverse_sql="DROP SCHEMA IF EXISTS proxy_service CASCADE;",
        ),
    ]