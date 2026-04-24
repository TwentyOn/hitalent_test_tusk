from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.RunSQL(
            sql=f"CREATE SCHEMA IF NOT EXISTS {settings.DB_SCHEMA_NAME};",
            reverse_sql=f"DROP SCHEMA IF EXISTS {settings.DB_SCHEMA_NAME} CASCADE;",
        ),
    ]