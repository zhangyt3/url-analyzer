# Generated by Django 2.1.3 on 2018-11-14 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0004_auto_20181114_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='html_version',
            field=models.CharField(choices=[('5', 'HTML5'), ('4S', 'HTML 4.01 Strict'), ('4T', 'HTML 4.01 Transitional'), ('4F', 'HTML 4.01 Frameset'), ('X1S', 'XHTML 1.0 Strict'), ('X1T', 'XHTML 1.0 Transitional'), ('X1F', 'XHTML 1.0 Frameset'), ('X1_1', 'XHTML 1.1'), ('Unknown', 'Unknown')], default='Unknown', max_length=7),
        ),
    ]