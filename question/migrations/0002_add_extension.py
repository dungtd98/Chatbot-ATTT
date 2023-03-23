from django.contrib.postgres.operations import CreateExtension
from django.db import migrations
class Migration(migrations.Migration):
    # initial = True
    dependencies = [
        ('question', '0001_initial'),
    ]
    operations = [
        CreateExtension(name='pg_trgm'),
        
    ]