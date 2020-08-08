from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuser', '0002_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
