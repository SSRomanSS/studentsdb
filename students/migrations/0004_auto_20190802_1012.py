# Generated by Django 2.2.2 on 2019-08-02 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_student_student_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['last_name'], 'verbose_name': 'Студент', 'verbose_name_plural': 'Студенти'},
        ),
    ]