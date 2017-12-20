from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
