# Generated by Django 3.0.5 on 2020-04-07 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deal_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.IntegerField(choices=[(0, 'Кто исполнительный орган'), (1, 'Период действия исполнительного органа')])),
                ('answer', models.TextField()),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deal_api.Document')),
            ],
        ),
    ]
